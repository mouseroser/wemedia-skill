#!/usr/bin/env python3
"""
OpenClaw Documentation Deduplicator
Removes duplicate content while preserving unique core documentation
"""

import hashlib
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
    
    # Add last document
    if current_doc:
        docs.append({
            'path': current_doc,
            'content': '\n'.join(current_content).strip()
        })
    
    return docs

def content_hash(text):
    """Generate hash for content comparison"""
    # Normalize whitespace for comparison
    normalized = re.sub(r'\s+', ' ', text.strip())
    return hashlib.sha256(normalized.encode()).hexdigest()

def deduplicate_docs(docs):
    """Remove duplicate documents based on content hash"""
    hash_to_docs = defaultdict(list)
    
    # Group documents by content hash
    for doc in docs:
        h = content_hash(doc['content'])
        hash_to_docs[h].append(doc)
    
    # Keep only one document per hash (prefer shorter paths)
    unique_docs = []
    duplicates = []
    
    for h, doc_list in hash_to_docs.items():
        if len(doc_list) > 1:
            # Sort by path length, keep shortest
            doc_list.sort(key=lambda d: len(d['path']))
            unique_docs.append(doc_list[0])
            duplicates.extend(doc_list[1:])
        else:
            unique_docs.append(doc_list[0])
    
    return unique_docs, duplicates

def main():
    input_file = Path.home() / '.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_en_20260307.md'
    output_file = Path.home() / f'.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_dedup_{datetime.now().strftime("%Y%m%d")}.md'
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing documents...")
    docs = parse_markdown_file(content)
    print(f"Found {len(docs)} documents")
    
    print("Deduplicating...")
    unique_docs, duplicates = deduplicate_docs(docs)
    
    print(f"Unique documents: {len(unique_docs)}")
    print(f"Duplicate documents removed: {len(duplicates)}")
    
    # Write deduplicated file
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""# OpenClaw Documentation (Deduplicated)

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: github.com/openclaw/openclaw/docs/
Language: English only
Processing: Deduplicated (removed duplicate content)

Original files: {len(docs)}
Unique files: {len(unique_docs)}
Duplicates removed: {len(duplicates)}
Deduplication ratio: {len(duplicates)/len(docs)*100:.1f}%

---

""")
        
        for doc in sorted(unique_docs, key=lambda d: d['path']):
            f.write(f"# File: {doc['path']}\n\n")
            f.write(doc['content'])
            f.write("\n\n---\n\n")
    
    # Print statistics
    original_size = input_file.stat().st_size
    new_size = output_file.stat().st_size
    
    print(f"\n=== Statistics ===")
    print(f"Original: {len(docs)} files, {original_size/1024/1024:.2f} MB")
    print(f"Deduplicated: {len(unique_docs)} files, {new_size/1024/1024:.2f} MB")
    print(f"Reduction: {(original_size-new_size)/original_size*100:.1f}%")
    
    return {
        'original_files': len(docs),
        'unique_files': len(unique_docs),
        'duplicates_removed': len(duplicates),
        'original_size_mb': original_size/1024/1024,
        'new_size_mb': new_size/1024/1024,
        'reduction_pct': (original_size-new_size)/original_size*100,
        'output_file': str(output_file)
    }

if __name__ == '__main__':
    stats = main()
