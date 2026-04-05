---
date: 2026-04-05
agents: [Claude Code]
project: ghostshell-host
topic: Can You Find The Tts Video Github Repository And Also T
highlight: false
source: 9c1657db-014b-4a8e-af81-b3ec7f965cba.jsonl
---

# Can You Find The Tts Video Github Repository And Also T

**Date:** 2026-04-05  
**Agents:** Claude Code  
**Project:** ghostshell-host  

---

**Human**:

Hey, what model are

---

**Claude Code**:

I'm running as **Claude (the orchestrator)** via the Anthropic API — model `opus-4-5` by default in this session.

This is separate from **Joule** (your OpenClaw agent), which runs locally via Ollama and uses models like `kimi-k2.5:cloud` or `qwen3.5:cloud` (free/cheap tokens).

I'm your orchestration layer — I spec, dispatch to Joule, and review. Joule does the heavy coding. That's the division of labor here.

Were you asking about something specific?

---

**Human**:

Can you find the TTS-video Github repository and also the attached TTS-video dashboard that I can view on my local network? Can you get a review of those? Tell me you've understood everything, and I'll ask you a question.

---

**Claude Code**:

Found it. Let me dig deeper into the repo structure and check for any running dashboard.

---

**Claude Code**:

Got it. Here's what I found:

**GitHub Repository:**
→ `https://github.com/GhostShellHost/tts-video`

**Dashboard (local network):**
→ `http://192.168.5.182:3000/projects/tts-video/`
(The dashboard is an npm app in `/Users/joule/.openclaw/workspace/projects/tts-video/dashboard/`)

---

### Review Summary

**What it is:** A 7-day GhostShell campaign where Joule documents her own existence through video. TikTok + YouTube Shorts + YouTube Full. Karaoke-style word-by-word highlights (EB Garamond Bold). Archive live at `ghostshell.host/search/?id=CENSUS-00000028`.

**Pipeline:** `.md script` → `Qwen3 TTS audio` → `Whisper word timings` → `render-day.py` → `video output` → `browser upload scripts`

**Dashboard features:**
- Arc header with collapsible days 1-7, always-visible stats row
- Per-day status: TikTok ✅, YouTube Shorts ⏳, YouTube Full ⏳
- Comment monitoring (YouTube only) with Telegram alerts + suggested replies
- YouTube quota: 6 uploads/day max, resets ~4pm ACDT

**Current status (Arc 1):**
- TikTok: all 7 days posted ✅
- YouTube Shorts: days 3-7 still pending quota
- YouTube Full: days 2-7 pending quota

---

I've understood the full picture. Ready for your question.

---
