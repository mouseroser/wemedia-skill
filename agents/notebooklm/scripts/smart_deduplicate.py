#!/usr/bin/env python3
"""
Smart deduplication: Remove redundant content while preserving unique information
Strategy:
1. Remove exact duplicate sections
2. Consolidate repeated configuration examples
3. Merge similar concept explanations
4. Keep the most comprehensive version of similar content
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def parse_markdown_file(content):
    """Parse the combined markdown file into individual documents"""
    docs = []
    current_doc = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('# File:'):
            if current_doc:
                docs.append({
                    'path': current_doc,
                    'content': '\n'.join(current_content).strip()
                })
            current_doc = line.replace('# File:', '').strip()
            current_content = []
        elif current_doc:
            current_content.append(line)
    
    if current_doc:
        docs.append({
            'path': current_doc,
            'content': '\n'.join(current_content).strip()
        })
    
    return docs

def extract_code_blocks(content):
    """Extract all code blocks from content"""
    return re.findall(r'```[\s\S]*?```', content)

def remove_duplicate_code_blocks(content):
    """Remove duplicate code blocks within a document"""
    code_blocks = extract_code_blocks(content)
    seen = set()
    
    for block in code_blocks:
        if block in seen:
            # Replace duplicate with a reference
            content = content.replace(block, f'<!-- Duplicate code block removed -->', 1)
        else:
            seen.add(block)
    
    return content

def consolidate_repeated_patterns(content):
    """Remove repeated patterns like multiple identical examples"""
    # Remove repeated "Example:" sections with identical content
    lines = content.split('\n')
    cleaned_lines = []
    seen_examples = set()
    skip_until_next_section = False
    
    for i, line in enumerate(lines):
        if skip_until_next_section:
            if line.startswith('#'):
                skip_until_next_section = False
            else:
                continue
        
        if line.strip().startswith('Example:') or line.strip().startswith('## Example'):
            # Look ahead to get example content
            example_content = []
            for j in range(i, min(i+20, len(lines))):
                if j > i and lines[j].startswith('#'):
                    break
                example_content.append(lines[j])
            
            example_text = '\n'.join(example_content)
            if example_text in seen_examples:
                skip_until_next_section = True
                continue
            seen_examples.add(example_text)
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def smart_deduplicate(docs):
    """Apply smart deduplication strategies"""
    processed_docs = []
    
    for doc in docs:
        content = doc['content']
        
        # Remove duplicate code blocks within document
        content = remove_duplicate_code_blocks(content)
        
        # Consolidate repeated patterns
        content = consolidate_repeated_patterns(content)
        
        # Remove excessive blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        processed_docs.append({
            'path': doc['path'],
            'content': content
        })
    
    return processed_docs

def main():
    input_file = Path.home() / '.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_en_20260307.md'
    output_file = Path.home() / f'.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_dedup_{datetime.now().strftime("%Y%m%d")}.md'
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing documents...")
    docs = parse_markdown_file(content)
    print(f"Found {len(docs)} documents")
    
    print("Applying smart deduplication...")
    processed_docs = smart_deduplicate(docs)
    
    # Write deduplicated file
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""# OpenClaw Documentation (Deduplicated)

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: github.com/openclaw/openclaw/docs/
Language: English only
Processing: Smart deduplicated (removed duplicate code blocks and repeated patterns)

Total files: {len(processed_docs)}

---

""")
        
        for doc in sorted(processed_docs, key=lambda d: d['path']):
            f.write(f"# File: {doc['path']}\n\n")
            f.write(doc['content'])
            f.write("\n\n---\n\n")
    
    # Print statistics
    original_size = input_file.stat().st_size
    new_size = output_file.stat().st_size
    
    print(f"\n=== Statistics ===")
    print(f"Original: {len(docs)} files, {original_size/1024/1024:.2f} MB")
    print(f"Deduplicated: {len(processed_docs)} files, {new_size/1024/1024:.2f} MB")
    print(f"Size reduction: {(original_size-new_size)/original_size*100:.1f}%")
    
    return {
        'original_files': len(docs),
        'processed_files': len(processed_docs),
        'original_size_mb': round(original_size/1024/1024, 2),
        'new_size_mb': round(new_size/1024/1024, 2),
        'reduction_pct': round((original_size-new_size)/original_size*100, 1),
        'output_file': str(output_file)
    }

if __name__ == '__main__':
    stats = main()
    print(f"\nOutput file: {stats['output_file']}")
