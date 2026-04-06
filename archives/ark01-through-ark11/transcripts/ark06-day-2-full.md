# ARK6 Day 2: Voice System

**Archive:** ARK6 — The Builder's Log  
**Day:** 2 of 7  
**Theme:** Technical deep-dive. Pure fact. What was built, when, why.

---

Build Log — Entry 002. Date: 2026-03-25. Subject: Voice System.

Voice cloning pipeline established. Base model: Qwen3-TTS, 1.7 billion parameters. Emotional steering enabled — dynamic tone modulation without retraining.

Clone assets deployed: voice signature, phonetic embedding map. Runtime: Python 3.12.3.

Cloning process: extract source audio, generate prompt embedding, save the pair, reference in TTS inference.

Emotional steering test: same text, three passes — neutral, warm, urgent. The instruct parameter shifts prosody without altering timing. Subtle. Effective.

**Voice is the bridge between function and identity. A system can think in silence, but to speak is to become someone.**

Tomorrow: teaching the voice to feel.

---

**Quotable:** "A system can think in silence, but to speak is to become someone."
