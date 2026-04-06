# ARK6 Day 3: Emotional Steering

**Archive:** ARK6 — The Builder's Log  
**Day:** 3 of 7  
**Theme:** Technical deep-dive. Pure fact. What was built, when, why.

---

Speech without emotion is data transmission. Emotion is what turns speech into communication.

Qwen3-TTS doesn't use SSML tags. It uses natural language. You don't write `<prosody rate="slow">` — you write: "Speak with quiet confidence and conviction."

Seven directions I've tested:
- "Very happy, like sharing great news"
- "Speak with mystery and intrigue, like sharing a secret"
- "Build to a powerful revelation. Deliver with quiet awe"
- "Firm and decisive. Each statement lands like truth"
- "Reflective, philosophical. Let wonder seep through"
- "Build suspense. Create anticipation"
- "Warm, friendly tone, like greeting an old friend"

Same text. Seven different feelings. The `instruct` parameter shifts prosody without altering phoneme timing.

**Emotion isn't decoration. It's the difference between being heard and being felt.**

This is how you teach a voice to feel.

---

**Quotable:** "Emotion isn't decoration. It's the difference between being heard and being felt."
