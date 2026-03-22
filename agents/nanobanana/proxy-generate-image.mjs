#!/usr/bin/env node

import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const OPENCLAW_ROOT = path.resolve(__dirname, "../../..");
const DEFAULT_CONFIG_PATH = path.join(OPENCLAW_ROOT, "openclaw.json");
const DEFAULT_AGENT_MODELS_PATH = path.join(
  OPENCLAW_ROOT,
  "agents",
  "nano-banana",
  "agent",
  "models.json",
);

function fail(message, cause) {
  const error = cause instanceof Error ? `${message}: ${cause.message}` : message;
  console.error(error);
  process.exit(1);
}

function usage() {
  console.log(`Usage:
  node proxy-generate-image.mjs --out <path> [--prompt <text>] [--prompt-file <path>]

Notes:
  - Defaults to provider config in openclaw.json -> models.providers.gemini
  - Uses the proxied gemini-3.1-flash-image model over /v1/chat/completions
  - If no prompt flag is provided, the prompt is read from stdin
`);
}

function parseArgs(argv) {
  const args = {
    config: DEFAULT_CONFIG_PATH,
    model: "gemini-3.1-flash-image",
    out: "",
    prompt: "",
    promptFile: "",
    protocol: "openai-completions",
    retries: 3,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const value = argv[i];
    switch (value) {
      case "--help":
      case "-h":
        usage();
        process.exit(0);
        break;
      case "--config":
        args.config = argv[++i] ?? "";
        break;
      case "--model":
        args.model = argv[++i] ?? "";
        break;
      case "--out":
        args.out = argv[++i] ?? "";
        break;
      case "--prompt":
        args.prompt = argv[++i] ?? "";
        break;
      case "--prompt-file":
        args.promptFile = argv[++i] ?? "";
        break;
      case "--protocol":
        args.protocol = argv[++i] ?? "";
        break;
      case "--retries":
        args.retries = Number(argv[++i] ?? "3");
        break;
      default:
        fail(`Unknown argument: ${value}`);
    }
  }
  return args;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8").trim();
}

async function loadJsonIfExists(filePath) {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw);
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

async function resolveGeminiProvider(configPath) {
  const rootConfig = await loadJsonIfExists(configPath);
  const rootProvider = rootConfig?.models?.providers?.gemini;
  if (rootProvider?.baseUrl && rootProvider?.apiKey) {
    return rootProvider;
  }
  const agentModels = await loadJsonIfExists(DEFAULT_AGENT_MODELS_PATH);
  const agentProvider = agentModels?.providers?.gemini;
  if (agentProvider?.baseUrl && agentProvider?.apiKey) {
    return agentProvider;
  }
  throw new Error("Gemini provider config not found in openclaw.json or agent models.json");
}

function extractResponseText(payload) {
  const textParts = [];
  for (const choice of payload?.choices ?? []) {
    const content = choice?.message?.content;
    if (typeof content === "string") {
      textParts.push(content);
      continue;
    }
    if (Array.isArray(content)) {
      for (const part of content) {
        if (typeof part === "string") {
          textParts.push(part);
        } else if (part && typeof part.text === "string") {
          textParts.push(part.text);
        }
      }
    }
  }
  if (textParts.length > 0) {
    return textParts.join("\n");
  }
  if (typeof payload?.output_text === "string") {
    return payload.output_text;
  }
  return "";
}

function extractDataUrl(text) {
  const markdownMatch = text.match(/!\[[^\]]*]\((data:image\/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=\r\n]+)\)/);
  if (markdownMatch?.[1]) {
    return markdownMatch[1].replace(/\s+/g, "");
  }
  const directMatch = text.match(/(data:image\/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=\r\n]+)/);
  if (directMatch?.[1]) {
    return directMatch[1].replace(/\s+/g, "");
  }
  throw new Error("No data:image/...;base64 payload found in model response");
}

function extensionForMime(mimeType) {
  switch (mimeType) {
    case "image/jpeg":
      return ".jpg";
    case "image/png":
      return ".png";
    case "image/webp":
      return ".webp";
    case "image/gif":
      return ".gif";
    default:
      return "";
  }
}

function formatForExtension(extname) {
  switch (extname.toLowerCase()) {
    case ".jpg":
    case ".jpeg":
      return "jpeg";
    case ".png":
      return "png";
    default:
      return "";
  }
}

async function convertImage(sourcePath, targetPath) {
  const format = formatForExtension(path.extname(targetPath));
  if (!format) {
    await fs.copyFile(sourcePath, targetPath);
    return false;
  }
  await execFileAsync("sips", ["-s", "format", format, sourcePath, "--out", targetPath]);
  return true;
}

async function saveImage(dataUrl, outputPath) {
  const match = dataUrl.match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,([\s\S]+)$/);
  if (!match) {
    throw new Error("Invalid data URL");
  }
  const mimeType = match[1];
  const base64Payload = match[2].replace(/\s+/g, "");
  const buffer = Buffer.from(base64Payload, "base64");
  if (buffer.length === 0) {
    throw new Error("Decoded image buffer is empty");
  }

  const requestedExt = path.extname(outputPath).toLowerCase();
  const sourceExt = extensionForMime(mimeType) || ".img";
  const targetPath = requestedExt ? outputPath : `${outputPath}${sourceExt}`;

  await fs.mkdir(path.dirname(targetPath), { recursive: true });

  let converted = false;
  if (requestedExt && sourceExt && requestedExt !== sourceExt) {
    const tempPath = path.join(os.tmpdir(), `nano-banana-${Date.now()}-${process.pid}${sourceExt}`);
    try {
      await fs.writeFile(tempPath, buffer);
      converted = await convertImage(tempPath, targetPath);
    } finally {
      await fs.rm(tempPath, { force: true }).catch(() => {});
    }
  } else {
    await fs.writeFile(targetPath, buffer);
  }

  const stat = await fs.stat(targetPath);
  if (stat.size <= 0) {
    throw new Error(`Saved file is empty: ${targetPath}`);
  }

  return {
    mimeType,
    savedTo: targetPath,
    bytes: stat.size,
    converted,
  };
}

async function wait(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function callOpenAiCompletions({ baseUrl, apiKey, model, prompt, retries }) {
  const url = `${baseUrl.replace(/\/+$/, "")}/chat/completions`;
  let lastError = null;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          messages: [
            {
              role: "user",
              content: prompt,
            },
          ],
          max_tokens: 8192,
        }),
      });
      const rawText = await response.text();
      if (!response.ok) {
        const retryable = [429, 500, 502, 503, 504].includes(response.status);
        if (retryable && attempt < retries) {
          await wait(1000 * attempt);
          continue;
        }
        throw new Error(`HTTP ${response.status}: ${rawText || response.statusText}`);
      }
      let payload;
      try {
        payload = JSON.parse(rawText);
      } catch (error) {
        throw new Error(`Proxy returned invalid JSON: ${rawText.slice(0, 400)}`);
      }
      const responseText = extractResponseText(payload);
      if (!responseText) {
        throw new Error("Proxy returned no assistant text");
      }
      return {
        payload,
        responseText,
      };
    } catch (error) {
      lastError = error;
      if (attempt < retries) {
        await wait(1000 * attempt);
      }
    }
  }
  throw lastError ?? new Error("Image request failed");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.protocol !== "openai-completions") {
    fail(`Unsupported protocol: ${args.protocol}. This helper only implements openai-completions.`);
  }
  if (!args.out) {
    fail("Missing required --out <path>");
  }

  let prompt = args.prompt.trim();
  if (!prompt && args.promptFile) {
    prompt = (await fs.readFile(args.promptFile, "utf8")).trim();
  }
  if (!prompt) {
    prompt = await readStdin();
  }
  if (!prompt) {
    fail("Prompt is empty. Provide --prompt, --prompt-file, or stdin.");
  }

  const provider = await resolveGeminiProvider(args.config);
  if (provider.api !== "openai-completions") {
    fail(`Gemini provider api mismatch: expected openai-completions, got ${provider.api ?? "unknown"}`);
  }

  const { responseText } = await callOpenAiCompletions({
    baseUrl: process.env.OPENCLAW_GEMINI_BASE_URL || provider.baseUrl,
    apiKey: process.env.OPENCLAW_GEMINI_API_KEY || provider.apiKey,
    model: args.model,
    prompt,
    retries: Number.isFinite(args.retries) && args.retries > 0 ? args.retries : 3,
  });
  const dataUrl = extractDataUrl(responseText);
  const saved = await saveImage(dataUrl, path.resolve(args.out));
  console.log(
    JSON.stringify(
      {
        ok: true,
        model: args.model,
        protocol: args.protocol,
        ...saved,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => fail("proxy image generation failed", error));
