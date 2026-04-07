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

**Human**:

Excellent, gateways are working, but I've switched over to the Apple Foundation model. launchctl_status shows me it's working, and then I type HI, and I give this message a 404 status code in brackets with no body. Investigate why this is happening and then test to see how we can get this to work. This has been a hot card problem.

---

**Claude Code**:

The apfel server itself is perfectly healthy — direct curl returns 200. The 404 is coming from the OpenClaw gateway routing to the wrong endpoint. The `openai-completions` API type likely maps to `/v1/completions` (legacy), but apfel only serves `/v1/chat/completions`. Let me verify:

---

**Claude Code**:

Key finding: apfel server is healthy (200 on chat/completions, streaming works). The issue is elsewhere. I see `ai.openclaw.apfel-proxy` has exit code `78` (not running). Let me check if that's in the routing chain:

---

**Claude Code**:

The log shows "APFEL WORKS IN OPENCLAW" at 12:39, then 404s at 12:55. And there's a dead apfel-proxy (exit 78). Let me dig into the proxy and what it does:

---

**Claude Code**:

Now I see the full picture clearly:

**Root cause:** The architecture requires a proxy chain:
```
OpenClaw (openai-completions) → apfel-proxy:11436 → apfel-server:11435
```

OpenClaw's `openai-completions` calls `POST /v1/completions`. Apfel only supports `/v1/chat/completions`. The proxy (apfel-proxy.js) was built to translate between them — but it's dead (exit 78) and the config `baseUrl` is pointing directly to apfel on port 11435, bypassing the proxy. The gateway hits `/v1/completions` on apfel directly and gets a non-200 response.

Fix: restart the proxy with the correct Node path, and point the config to port 11436.

---

**Claude Code**:

`/usr/bin/node` doesn't exist on macOS — that's why exit code 78 (config/binary not found). Fix both the plist and the config:

---

**Claude Code**:

Now restart the proxy:

---

**Claude Code**:

Proxy is up on port 11436. Now end-to-end test through the proxy:

---

**Claude Code**:

All three paths through the proxy return 200. The fix is complete.

**Summary of what happened and what was fixed:**

| Problem | Fix |
|---|---|
| `apfel.api` was `"openai-chat"` (invalid) → gateway crash-looped | Changed to `"openai-completions"` |
| `apfel.baseUrl` pointed to `:11435` (apfel directly) | Changed to `:11436` (proxy) |
| Proxy plist used `/usr/bin/node` (doesn't exist on macOS) | Changed to `/opt/homebrew/bin/node` |

**The required chain is:**
```
OpenClaw → apfel-proxy:11436 → apfel-server:11435
```

OpenClaw's `openai-completions` type sends `POST /v1/completions`. Apfel only speaks `POST /v1/chat/completions`. The proxy (which Joule built) translates between them — but it was broken by the wrong node path and the config was pointing past it directly to apfel.

Try sending "hi" now — it should work.

---
