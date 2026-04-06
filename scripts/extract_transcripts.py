#!/usr/bin/env python3
"""
Extract conversation transcripts from OpenClaw session files.
Creates a complete provenance archive for ARK production.
"""

import json
import os
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path("/Users/joule/.openclaw/agents/main/sessions")
OUTPUT_DIR = Path("/Users/joule/.openclaw/workspace/projects/agent-conversations/archives")

def extract_session(session_file: Path) -> dict:
    """Extract a single session transcript."""
    with open(session_file, 'r') as f:
        messages = []
        for line in f:
            try:
                msg = json.loads(line.strip())
                messages.append(msg)
            except json.JSONDecodeError:
                continue
    
    return {
        "session_file": session_file.name,
        "message_count": len(messages),
        "messages": messages
    }

def find_ark_sessions(ark_number: int) -> list:
    """Find all sessions related to a specific ARK."""
    ark_sessions = []
    
    for session_file in SESSIONS_DIR.glob("*.jsonl"):
        try:
            with open(session_file, 'r') as f:
                first_line = f.readline()
                if first_line:
                    content = first_line.lower()
                    # Look for ARK references
                    if f"ark{ark_number}" in content or f"ark-{ark_number}" in content:
                        ark_sessions.append(session_file)
        except Exception as e:
            continue
    
    return ark_sessions

def create_transcript_doc(session_data: dict, output_path: Path):
    """Create a human-readable transcript document."""
    with open(output_path, 'w') as f:
        f.write(f"# Session Transcript\n\n")
        f.write(f"**Source:** `{session_data['session_file']}`\n")
        f.write(f"**Messages:** {session_data['message_count']}\n\n")
        f.write(f"**Extracted:** {datetime.now().isoformat()}\n\n")
        f.write("---\n\n")
        
        for i, msg in enumerate(session_data['messages'], 1):
            role = msg.get('role', 'unknown')
            timestamp = msg.get('timestamp', 0)
            dt = datetime.fromtimestamp(timestamp / 1000) if timestamp else None
            
            f.write(f"## Message {i} — {role.upper()}\n")
            if dt:
                f.write(f"*{dt.isoformat()}*\n\n")
            
            # Extract content
            content = msg.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'text':
                        f.write(f"{item.get('text', '')}\n\n")
                    elif item.get('type') == 'toolCall':
                        tool_name = item.get('name', 'unknown')
                        args = item.get('arguments', {})
                        f.write(f"🔧 **Tool:** `{tool_name}`\n")
                        f.write(f"```json\n{json.dumps(args, indent=2)}\n```\n\n")
            elif isinstance(content, str):
                f.write(f"{content}\n\n")
            
            f.write("---\n\n")

def main():
    print("🔍 Extracting conversation transcripts...")
    
    # Create archive structure
    for ark in range(12, 21):
        ark_dir = OUTPUT_DIR / f"ark{ark}-*" / "transcripts"
        ark_dir.mkdir(parents=True, exist_ok=True)
        
        subagents_dir = OUTPUT_DIR / f"ark{ark}-*" / "subagents"
        subagents_dir.mkdir(parents=True, exist_ok=True)
    
    print("✅ Archive structure ready")
    print("\n📝 To extract specific ARK transcripts:")
    print("   Manual step needed: Identify session IDs from sessions_list")
    print("   Then run: python extract_transcript.py <session_id>")
    
if __name__ == "__main__":
    main()
