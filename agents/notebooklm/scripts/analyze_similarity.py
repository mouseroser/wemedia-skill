#!/usr/bin/env python3
"""
Analyze content similarity and identify repeated sections
"""

import re
from pathlib import Path
from collections import Counter, defaultdict
from difflib import SequenceMatcher

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

def extract_sections(content):
    """Extract markdown sections (headers + content)"""
    sections = []
    lines = content.split('\n')
    current_section = []
    
    for line in lines:
        if line.startswith('#'):
            if current_section:
                sections.append('\n'.join(current_section).strip())
            current_section = [line]
        else:
            current_section.append(line)
    
    if current_section:
        sections.append('\n'.join(current_section).strip())
    
    return sections

def similarity_ratio(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, text1, text2).ratio()

def find_repeated_sections(docs, threshold=0.85):
    """Find sections that appear in multiple documents"""
    all_sections = []
    
    for doc in docs:
        sections = extract_sections(doc['content'])
        for section in sections:
            if len(section) > 100:  # Only consider substantial sections
                all_sections.append({
                    'doc': doc['path'],
                    'content': section
                })
    
    print(f"Analyzing {len(all_sections)} sections...")
    
    # Find similar sections
    similar_groups = []
    processed = set()
    
    for i, sec1 in enumerate(all_sections):
        if i in processed:
            continue
        
        group = [sec1]
        for j, sec2 in enumerate(all_sections[i+1:], i+1):
            if j in processed:
                continue
            
            ratio = similarity_ratio(sec1['content'], sec2['content'])
            if ratio >= threshold:
                group.append(sec2)
                processed.add(j)
        
        if len(group) > 1:
            similar_groups.append(group)
            processed.add(i)
    
    return similar_groups

def analyze_code_blocks(docs):
    """Find repeated code blocks"""
    code_blocks = defaultdict(list)
    
    for doc in docs:
        blocks = re.findall(r'```[\s\S]*?```', doc['content'])
        for block in blocks:
            if len(block) > 50:
                code_blocks[block].append(doc['path'])
    
    repeated = {k: v for k, v in code_blocks.items() if len(v) > 1}
    return repeated

def main():
    input_file = Path.home() / '.openclaw/workspace/agents/notebooklm/docs/openclaw_docs_en_20260307.md'
    
    print(f"Reading {input_file}...")
    content = input_file.read_text(encoding='utf-8')
    
    print("Parsing documents...")
    docs = parse_markdown_file(content)
    print(f"Found {len(docs)} documents\n")
    
    # Analyze repeated code blocks
    print("=== Analyzing repeated code blocks ===")
    repeated_code = analyze_code_blocks(docs)
    print(f"Found {len(repeated_code)} repeated code blocks")
    
    if repeated_code:
        print("\nTop 5 most repeated code blocks:")
        sorted_code = sorted(repeated_code.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        for i, (block, files) in enumerate(sorted_code, 1):
            print(f"\n{i}. Appears in {len(files)} files:")
            print(f"   {block[:100]}...")
            print(f"   Files: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
    
    # Analyze similar sections
    print("\n=== Analyzing similar sections (threshold=0.85) ===")
    similar_groups = find_repeated_sections(docs, threshold=0.85)
    print(f"Found {len(similar_groups)} groups of similar sections")
    
    if similar_groups:
        print("\nTop 5 largest groups:")
        sorted_groups = sorted(similar_groups, key=lambda g: len(g), reverse=True)[:5]
        for i, group in enumerate(sorted_groups, 1):
            print(f"\n{i}. Group with {len(group)} similar sections:")
            print(f"   Preview: {group[0]['content'][:100]}...")
            print(f"   Files: {', '.join([s['doc'] for s in group[:3]])}{'...' if len(group) > 3 else ''}")

if __name__ == '__main__':
    main()
