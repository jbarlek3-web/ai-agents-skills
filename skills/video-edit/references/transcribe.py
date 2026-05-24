"""Reusable Whisper transcribe — drop into a HyperFrames project.

Usage:
    python transcribe.py             # auto-detect language, large-v3
    python transcribe.py he          # force Hebrew
    python transcribe.py en medium   # force English, medium model

Outputs `transcript.json` with segments + word-level timestamps.
"""

import json, sys
from faster_whisper import WhisperModel

LANG = sys.argv[1] if len(sys.argv) > 1 else None
MODEL = sys.argv[2] if len(sys.argv) > 2 else "large-v3"

# CPU only — local CUDA install on Windows usually lacks cuDNN, which crashes
# CTranslate2 mid-decode (uncatchable native crash). int8 is fast enough.
m = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=8)

kwargs = {"word_timestamps": True, "vad_filter": True}
if LANG:
    kwargs["language"] = LANG

segs, info = m.transcribe("audio.wav", **kwargs)

print(f"language: {info.language}  model: {MODEL}", file=sys.stderr)

out = []
for seg in segs:
    words = [
        {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
        for w in (seg.words or [])
    ]
    out.append(
        {
            "text": seg.text.strip(),
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "words": words,
        }
    )

with open("transcript.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"{len(out)} segments, {sum(len(s['words']) for s in out)} words", file=sys.stderr)
