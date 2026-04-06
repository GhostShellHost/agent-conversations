#!/usr/bin/env python3
"""Extract transcripts from JSONL session files to markdown format."""

import json
import os
import sys
from datetime import datetime

def extract_messages(jsonl_path):
    """Extract user and assistant messages from JSONL."""
    messages = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get('type') != 'message':
                    continue
                msg = data.get('message', {})
                role = msg.get('role')
                content_parts = msg.get('content', [])
                timestamp = data.get('timestamp', '')
                
                if role not in ('user', 'assistant'):
                    continue
                
                # Extract text from content
                texts = []
                for part in content_parts:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        texts.append(part.get('text', ''))
                    elif isinstance(part, str):
                        texts.append(part)
                
                text = ' '.join(texts).strip()
                if not text:
                    continue
                
                # Skip bootstrap messages
                if any(skip in text for skip in [
                    'A new session was started via /new or /reset',
                    'Bootstrap truncation warning',
                    'Some workspace bootstrap files were truncated',
                    'Read the required files before responding',
                    'Current time:',
                    'Fresh session, all context loaded'
                ]):
                    continue
                
                messages.append({
                    'role': role,
                    'text': text,
                    'timestamp': timestamp
                })
            except (json.JSONDecodeError, Exception):
                continue
    return messages

def clean_user_message(text):
    """Clean up user message to remove metadata."""
    # Remove conversation info blocks
    if 'Conversation info (untrusted metadata):' in text:
        # Find the actual message after the metadata blocks
        lines = text.split('\n')
        actual_msg = []
        in_json = False
        for line in lines:
            if '```json' in line:
                in_json = True
                continue
            if '```' in line and in_json:
                in_json = False
                continue
            if in_json:
                continue
            actual_msg.append(line)
        text = '\n'.join(actual_msg).strip()
    
    # Remove subagent context markers
    if '[Subagent Context]' in text:
        lines = text.split('\n')
        # Find the first line after the context block that isn't empty
        past_context = False
        result = []
        for line in lines:
            if past_context and line.strip():
                result.append(line)
            elif '[Subagent Task]:' in line or past_context:
                past_context = True
                if line.strip() and '[Subagent' not in line:
                    result.append(line)
        text = '\n'.join(result).strip()
    
    return text

def format_transcript(messages, session_id):
    """Format messages into markdown."""
    lines = []
    
    # Header
    lines.append(f'# Session Transcript: {session_id}')
    lines.append('')
    
    # Timestamp
    if messages and messages[0].get('timestamp'):
        try:
            ts = messages[0]['timestamp']
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            lines.append(f'**Date:** {dt.strftime("%Y-%m-%d")}')
            lines.append(f'**Time:** {dt.strftime("%H:%M")} UTC')
            lines.append('')
        except:
            pass
    
    lines.append('---')
    lines.append('')
    
    # Messages
    for msg in messages:
        role = msg['role']
        text = msg['text']
        
        if role == 'user':
            text = clean_user_message(text)
            if text and text not in ['hi', 'hello', 'hey', 'ok', 'thanks']:
                lines.append(f'**User:** {text}')
                lines.append('')
        elif role == 'assistant':
            # Truncate very long responses
            if len(text) > 5000:
                text = text[:5000] + '\n\n[... content truncated ...]'
            lines.append(f'**Joule:** {text}')
            lines.append('')
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <input.jsonl> <output.md>')
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f'Error: File not found: {input_path}')
        sys.exit(1)
    
    session_id = os.path.basename(input_path).replace('.jsonl', '')
    messages = extract_messages(input_path)
    
    if not messages:
        print(f'Warning: No messages extracted from {input_path}')
        # Write empty file with note
        with open(output_path, 'w') as f:
            f.write(f'# Session: {session_id}\n\n_No conversation content found._\n')
        return
    
    output = format_transcript(messages, session_id)
    
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f'Extracted {len(messages)} messages to {output_path}')

if __name__ == '__main__':
    main()
