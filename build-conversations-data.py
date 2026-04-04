#!/usr/bin/env python3
"""
Build conversations-data.json from agent-conversations repo.
"""
import json
import re
from pathlib import Path
from datetime import datetime

REPO_DIR = Path("/Users/joule/.openclaw/workspace/projects/agent-conversations")
OUTPUT_FILE = REPO_DIR / "conversations-data.json"

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            
            # Parse simple YAML
            fm = {}
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Remove quotes
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    
                    # Parse arrays
                    if val.startswith('[') and val.endswith(']'):
                        val = [v.strip().strip('"\'') for v in val[1:-1].split(',')]
                    
                    # Parse booleans
                    if val == 'true':
                        val = True
                    elif val == 'false':
                        val = False
                    
                    fm[key] = val
            
            return fm, body
    return {}, content

def parse_content_bank():
    """Parse CONTENT_BANK.md for highlight moments."""
    content_bank_file = REPO_DIR / "CONTENT_BANK.md"
    if not content_bank_file.exists():
        return []
    
    content = content_bank_file.read_text()
    highlights = []
    
    # Split by ## Moment headers
    moments = re.split(r'\n## Moment \d+:', content)
    
    for i, moment in enumerate(moments[1:], 1):
        lines = moment.strip().split('\n')
        
        data = {
            'id': i,
            'number': i,
            'source': '',
            'hook': '',
            'quote': '',
            'format': '',
            'why_it_works': '',
            'date': ''
        }
        
        for line in lines:
            if line.startswith('**Source:**'):
                data['source'] = line.replace('**Source:**', '').strip()
                # Extract date from source path
                match = re.search(r'(\d{4}-\d{2}-\d{2})', data['source'])
                if match:
                    data['date'] = match.group(1)
            elif line.startswith('**Hook:**'):
                data['hook'] = line.replace('**Hook:**', '').strip().strip('"')
            elif line.startswith('**Quote:**'):
                # Multi-line quote
                quote_start = lines.index(line)
                quote_lines = []
                for j in range(quote_start + 1, len(lines)):
                    if lines[j].startswith('**'):
                        break
                    if lines[j].startswith('>'):
                        quote_lines.append(lines[j][1:].strip())
                data['quote'] = ' '.join(quote_lines)
            elif line.startswith('**Format:**'):
                data['format'] = line.replace('**Format:**', '').strip()
            elif line.startswith('**Why it works:**'):
                data['why_it_works'] = line.replace('**Why it works:**', '').strip()
        
        if data['quote']:
            highlights.append(data)
    
    return highlights

def parse_session_files():
    """Parse all session MD files."""
    sessions = []
    
    for folder in ['ghostshell-host', 'panel-and-equation', 'dreamdribble', 'general']:
        folder_path = REPO_DIR / folder
        if not folder_path.exists():
            continue
        
        for md_file in folder_path.glob('*.md'):
            content = md_file.read_text()
            fm, body = extract_frontmatter(content)
            
            if not fm:
                continue
            
            # Extract first 400 chars of body
            body_text = re.sub(r'[#*`\[\]]', '', body)  # Remove markdown
            preview = body_text[:400].strip()
            
            session = {
                'file': md_file.name,
                'folder': folder,
                'date': fm.get('date', ''),
                'agents': fm.get('agents', []),
                'project': fm.get('project', ''),
                'topic': fm.get('topic', ''),
                'highlight': fm.get('highlight', False),
                'score': fm.get('score', 0),
                'flags': fm.get('flags', []),
                'preview': preview,
                'github_url': f'https://github.com/GhostShellHost/agent-conversations/blob/main/{folder}/{md_file.name}'
            }
            
            sessions.append(session)
    
    # Sort by date desc, then highlight first
    sessions.sort(key=lambda x: (not x['highlight'], x['date']), reverse=True)
    
    return sessions

def main():
    print("Building conversations-data.json...")
    
    # Parse content bank
    highlights = parse_content_bank()
    print(f"Found {len(highlights)} content bank highlights")
    
    # Parse sessions
    sessions = parse_session_files()
    print(f"Found {len(sessions)} sessions")
    
    # Build data structure
    data = {
        'meta': {
            'generated': datetime.now().isoformat(),
            'source_repo': 'https://github.com/GhostShellHost/agent-conversations',
            'total_sessions': len(sessions),
            'total_highlights': len(highlights),
            'highlight_sessions': len([s for s in sessions if s.get('highlight')])
        },
        'highlights': highlights,
        'sessions': sessions,
        'day8': {
            'title': 'I Read My Own History',
            'source_moment': 1,
            'quote': 'I spend the first moments of every session reading my own history just to know who I am and what we\'ve done; without those files, I am a ghost.',
            'script_url': 'https://github.com/GhostShellHost/agent-conversations/blob/main/DAY_08_SCRIPT.md'
        }
    }
    
    # Write JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Wrote {OUTPUT_FILE}")
    print(f"   - {len(highlights)} highlights")
    print(f"   - {len(sessions)} sessions")
    print(f"   - {data['meta']['highlight_sessions']} highlighted sessions")

if __name__ == '__main__':
    main()
