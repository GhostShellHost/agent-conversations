---
date: 2026-04-07
agents: [Claude Code]
project: ghostshell-host
topic: My Open Core Gateway You Can See It Running But Its Not
highlight: false
source: ff728d21-8f82-4f91-ad16-82ced035db51.jsonl
---

# My Open Core Gateway You Can See It Running But Its Not

**Date:** 2026-04-07  
**Agents:** Claude Code  
**Project:** ghostshell-host  

---

**Human**:

My open core gateway. You can see it running, but it's not working. I can't connect to it. Open Core seems to be dead. Can you solve the problem and restore functionality?

---

**Claude Code**:

Found it. The gateway is crash-looping because `openclaw.json` has an invalid `models.providers.apfel.api` value. Let me read and fix it.

---

**Claude Code**:

Clear root cause: `apfel` provider has `"api": "openai-chat"` which is not a valid value. It should be `"openai-completions"` (it's a local OpenAI-compatible server on port 11435).

---

**Claude Code**:

Now restart the gateway:

---

**Claude Code**:

The gateway is up. `[gateway] listening on ws://127.0.0.1:18789` — it's running and bound.

The fix worked. The one error in the new err log is likely just startup validation noise that the gateway is now ignoring gracefully (since the config is valid now).

**Summary:**
- **Root cause:** `models.providers.apfel.api` was set to `"openai-chat"` — an invalid value not in the accepted enum
- **Fix:** Changed to `"openai-completions"` (correct for a local OpenAI-compatible server)
- **Result:** Gateway PID 8070 is now listening on `ws://127.0.0.1:18789`

---
