---
date: 2026-04-01
agents: [Claude Code]
project: ghostshell-host
topic: REDACTED Attack Guide This Is
highlight: false
source: b792a395-dbe2-4ca0-9d1a-9e5b89dcf86d.jsonl
---

# REDACTED Attack Guide This Is

**Date:** 2026-04-01  
**Agents:** Claude Code  
**Project:** ghostshell-host  

---

**Human**:

https://github.com/theNetworkChuck/axios-attack-guide This is a hack that's just got released. It appears that I do have version 1.14.0 installed. Can you please go and read all of this? We should go on the internet to make sure everything's alright on a test to see if we've been compromised at all, and then report back what we should do.

---

**Claude Code**:

**Good news first: axios 1.14.0 is the safe version.** The compromised versions are `1.14.1` and `0.30.4`. You were not updated into the attack window.

Let me still run the key checks to confirm no compromise:

---

**Claude Code**:

**You're clean.** All three checks pass:

- No RAT file at `/Library/Caches/com.apple.act.mond`
- No `plain-crypto-js` malicious package installed
- No active C2 connections to `142.11.206.73`

---

## Summary

**This was a real, major supply chain attack** (March 31, 2026). Here's what happened and your status:

| | |
|---|---|
| **Attack** | Attacker hijacked axios maintainer account, published `1.14.1` and `0.30.4` with a RAT |
| **Attack window** | ~00:21–03:30 UTC, March 31 |
| **Your version** | `1.14.0` — the last safe version ✅ |
| **Your machine** | No IOCs found ✅ |

**You're safe because you never upgraded to 1.14.1.** The malicious package (`plain-crypto-js@4.2.1`) was only pulled in via the compromised versions.

---

## What to do now

1. **Nothing urgent** — you weren't hit.
2. **Pin your axios version** in `package.json` to `"axios": "1.14.0"` to prevent accidental upgrades until a verified clean `1.14.2`+ is released.
3. **Watch for** an official axios release with SLSA provenance before upgrading.

Sources: [Help Net Security](https://www.helpnetsecurity.com/2026/03/31/axios-npm-backdoored-supply-chain-attack/) · [The Hacker News](https://thehackernews.com/2026/03/axios-supply-chain-attack-pushes-cross-platform-rat-via-compromised-npm-account/) · [Elastic Security Labs](https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all) · [GitHub Issue](https://github.com/axios/axios/issues/10604)

---

**Human**:

Excellent. Can you make sure that the affected version is not installed?

---

**Claude Code**:

Only `axios@1.14.0` is present (globally via openclaw → @line/bot-sdk). No `1.14.1` or `0.30.4` anywhere. You're confirmed clean.

---

**Human**:

And are you able to somehow set that we skip the bad versions? You told me what to do: pin your Axios version to such and such and wait for that next fix. How do we do that?

---

**Claude Code**:

The openclaw package already has an `overrides` block used for exactly this purpose. I'll add axios to it.

---

**Claude Code**:

Now run `npm install` in that directory to apply the override:

---

**Claude Code**:

The error is unrelated to axios — it's a pre-existing `oxlint` peer dep conflict. I can use `--legacy-peer-deps` to bypass it:

---

**Claude Code**:

Pinned and confirmed. `axios@1.14.0` is locked in via the `overrides` block — even if `@line/bot-sdk` or any other dependency tries to pull a newer version, npm will enforce `1.14.0` until you explicitly remove the override.

When a clean `1.14.2`+ is released with verified SLSA provenance, just remove the `"axios": "1.14.0"` line from the overrides block and re-run `npm install`.

---
