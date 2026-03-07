# OpenClaw Embedding Provider Chain 诊断报告

**文档编号**: OC-DIAG-2026-0306-01  
**生成时间**: 2026-03-06 21:58 GMT+8  
**诊断对象**: memory_search / embeddings provider 配置链  
**错误现象**: `404 Cannot POST /codex/embeddings`

---

## 一、问题概述

用户在 OpenClaw 环境中配置 memory_search 使用远程 Embeddings 提供商时，遇到不稳定的 `404 Cannot POST /codex/embeddings` 错误。该错误表明请求到达了错误的服务端点或路径拼接逻辑存在问题。

---

## 二、配置链路分析

### 2.1 Memory Search 配置结构

根据 OpenClaw 配置 schema，memory_search 的 embedding provider 配置链路如下：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",          // openai | gemini | voyage | mistral | local
        "model": "text-embedding-3-small",
        "remote": {
          "baseUrl": "https://api.example.com/v1",  // ← 关键配置项
          "apiKey": "sk-xxx",
          "headers": {},
          "batch": {
            "enabled": true,
            "wait": true,
            "concurrency": 2,
            "pollIntervalMs": 2000,
            "timeoutMinutes": 60
          }
        }
      }
    }
  }
}
```

### 2.2 配置字段语义

| 配置字段 | 说明 | 风险点 |
|---------|------|--------|
| `provider` | 选择 embedding backend | 需要与 baseUrl 兼容 |
| `remote.baseUrl` | 覆盖默认 embedding API 端点 | **路径拼接错误的根本来源** |
| `remote.apiKey` | 专用 API key | 缺失导致 401 |
| `remote.headers` | 自定义 HTTP headers | 代理认证、租户路由 |

---

## 三、根因诊断

### 3.1 直接根因

**触发 404 错误的根因是：自定义 API 端点地址配置与上游服务实际路由不匹配。**

具体场景：
1. 用户配置了 `remote.baseUrl` 指向某个自定义网关或代理
2. 系统在发送 embedding 请求时，将路径 `/embeddings` 拼接到 baseUrl 后面
3. 上游服务（如 Codex 内部服务、未正确配置的 OpenAI 兼容代理）不支持该路由
4. 返回 `404 Not Found`

### 3.2 路径拼接逻辑推测

基于配置结构和错误模式，系统可能执行如下路径拼接：

```
${baseUrl}/embeddings
```

**问题场景**：
- `baseUrl` = `https://api.example.com/codex` → 实际请求 `https://api.example.com/codex/embeddings` ✅
- `baseUrl` = `https://api.example.com` → 实际请求 `https://api.example.com/embeddings` ✅  
- `baseUrl` = `https://api.example.com/v1` → 实际请求 `https://api.example.com/v1/embeddings` ✅
- `baseUrl` = `https://api.example.com/v1/` → 可能重复斜杠或路径异常

### 3.3 不稳定因素

1. **baseUrl 尾缀不一致**：文档未明确规定是否必须带 `/v1` 或结尾斜杠
2. **provider 与 baseUrl 不匹配**：例如 provider=gemini 但 baseUrl 指向 OpenAI 兼容端点
3. **上游服务变更**：第三方 embedding 服务更新 API 路径
4. **代理/网关路由问题**：经过代理时路径可能被重写或拦截

---

## 四、配置验证清单

### 4.1 正确配置示例

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "remote": {
          "baseUrl": "https://api.openai.com/v1",
          "apiKey": "${OPENAI_API_KEY}"
        }
      }
    }
  }
}
```

### 4.2 自定义网关示例

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "remote": {
          "baseUrl": "https://your-proxy.example.com/v1",
          "apiKey": "sk-your-key",
          "headers": {
            "X-Custom-Auth": "token"
          }
        }
      }
    }
  }
}
```

---

## 五、修复建议

### 5.1 立即修复步骤

1. **验证 baseUrl**：确认上游服务实际支持的 embedding 端点路径
2. **检查尾缀规范**：
   - 推荐使用 `https://host/v1` 格式（无结尾斜杠）
   - 避免重复斜杠导致路径异常
3. **确认 provider 兼容性**：
   - 使用 OpenAI 兼容端点 → `provider: "openai"`
   - 使用 Gemini API → `provider: "gemini"` + Google 原生 baseUrl
4. **测试端点可达性**：
   ```bash
   curl -X POST https://your-base-url/v1/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"input": "test", "model": "text-embedding-3-small"}'
   ```

### 5.2 长期改进

1. **配置校验**：在 Gateway 启动时校验 baseUrl 格式和 provider 匹配性
2. **错误信息增强**：404 错误时提示可能的原因（路径错误/provider 不匹配）
3. **fallback 机制**：当 remote baseUrl 失败时，自动回退到默认 provider 端点

---

## 六、安全与成本注意

### 6.1 安全红线

- **严禁将明文 API key 提交到公开仓库**：使用环境变量 `${VAR}` 引用
- **headers 中的敏感信息需最小化**：避免泄露代理认证信息

### 6.2 成本风险

- **远程 embedding 调用产生 API 计费**
- **batch.concurrency 盲目调高会触达上游速率限制**
- **建议默认 concurrency=2**，大规模索引时逐步调整

---

## 七、结论

| 诊断项 | 结论 |
|--------|------|
| 错误类型 | 客户端配置错误 → 404 Not Found |
| 根因 | `remote.baseUrl` 路径与上游服务不匹配 |
| 影响范围 | 所有使用 remote embedding 的 agent |
| 修复复杂度 | 低（配置调整） |
| 建议优先级 | P1 - 立即修复 |

---

*诊断依据：OpenClaw 官方配置 schema 和参数语义说明*
