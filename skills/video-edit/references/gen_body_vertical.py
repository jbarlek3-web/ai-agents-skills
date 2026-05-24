# Hebrew body caption generator — generates compositions/components/caption-body.html
# from transcript.json. RTL Hebrew with liquid-glass pills, rotating editorial/matrix.
# Shifted right of frame center to clear the bottom-LEFT webcam PiP in this video.
import json, re, io

BODY_START = 0.0          # body pill captions span the entire speech (including the outro head)
BODY_END_GUESS = 179.5
RUN_LEN = 3               # groups per style run
MAX_WORDS = 4

# Hebrew corrections — fix common Whisper mishears (especially the Claude brand).
CORRECTIONS = {
    "קלוט": "קלוד",
    "לקלוט": "לקלוד",
    "מקלוט": "מקלוד",
    "המאמם": "המהמם",
    "התירוף": "הטירוף",
    "מהתחלס": "מהתחלה",
    "מזגיר": "מזכיר",
    "אשמחים": "אשמח",
    "ערב": "ערך",
    "אישות": "שוט",
    "מהמדהים": "המהמם",
    "החתונה": "תחתונה",
    "הרגע": "האריה",
    "מודי": "דפי",
}

# Common Hebrew stop tokens (longest-non-stopword heuristic for emphasis).
STOP = set(
    "של את על אם כי לא מה זה יש אין גם רק אני אתה הוא היא הם הן אנחנו ואז אבל או הזה הזאת אנו כך איך למה איפה מתי שם פה כאן עוד היה היא הייתי להיות יהיה תהיה ה ש ל ב מ ו כ".split()
)


def correct(tok):
    m = re.match(r"^(\S+?)([.,!?]*)$", tok)
    core, tail = (m.group(1), m.group(2)) if m else (tok, "")
    if core in CORRECTIONS:
        core = CORRECTIONS[core]
    return core + tail


def load_words():
    data = json.load(open("transcript.json", encoding="utf-8"))
    words = []
    for si, seg in enumerate(data):
        for w in seg["words"]:
            t = correct(w["word"].strip())
            if not t:
                continue
            words.append({"t": t, "s": w["start"], "e": w["end"], "seg": si})
    body = [w for w in words if BODY_START <= w["s"] < BODY_END_GUESS]
    return body


def group_words(words):
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["s"] - w["e"]) if nxt else 99
        seg_change = bool(nxt and nxt["seg"] != w["seg"])
        ends_sentence = bool(re.search(r"[.?!]$", w["t"]))
        if ends_sentence or seg_change or len(cur) >= MAX_WORDS or gap > 0.34 or nxt is None:
            groups.append(cur)
            cur = []
    merged = []
    for g in groups:
        if len(g) == 1 and merged and len(merged[-1]) < 5:
            merged[-1].extend(g)
        else:
            merged.append(g)
    return merged


def emph_index(g):
    best, bi = -1, 0
    for i, w in enumerate(g):
        core = re.sub(r"[^֐-׿\w]", "", w["t"])  # Hebrew letters + word chars
        score = len(core) + (3 if core not in STOP else 0)
        if score > best:
            best, bi = score, i
    return bi


def build():
    words = load_words()
    if not words:
        raise SystemExit("no words in body range — check transcript")
    groups = group_words(words)
    data = []
    for gi, g in enumerate(groups):
        style = "ed" if (gi // RUN_LEN) % 2 == 0 else "mx"
        ei = emph_index(g) if style == "ed" else -1
        s = round(g[0]["s"] - BODY_START - 0.05, 3)
        if s < 0:
            s = 0.0
        data.append(
            {
                "s": s,
                "raw_e": round(g[-1]["e"] - BODY_START, 3),
                "st": style,
                "words": [{"t": w["t"], "emph": (i == ei)} for i, w in enumerate(g)],
            }
        )
    for i, d in enumerate(data):
        d["e"] = data[i + 1]["s"] if i + 1 < len(data) else round(d["raw_e"] + 0.6, 3)
        del d["raw_e"]
    duration = round(data[-1]["e"] + 0.15, 2)
    return data, duration


DATA, DURATION = build()
ed = sum(1 for d in DATA if d["st"] == "ed")
print(f"{len(DATA)} body groups ({ed} editorial / {len(DATA)-ed} matrix), duration {DURATION}s")

DATA_JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))

TEMPLATE = r"""<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Body Captions — Hebrew (Vertical)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;700;900&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *, *::before, *::after { box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; margin: 0; overflow: hidden; background: transparent; }
      #caption-body {
        position: relative; width: 1080px; height: 1920px;
        overflow: hidden; background: transparent; pointer-events: none;
      }
      #cb-stage { position: absolute; inset: 0; }
      .cg {
        position: absolute; left: 540px; bottom: 340px;
        transform: translateX(-50%); transform-origin: 50% 100%;
        opacity: 0; will-change: transform, opacity;
      }
      /* liquid-glass pill — RTL for Hebrew */
      .pill {
        position: relative; direction: rtl;
        display: flex; flex-wrap: nowrap; align-items: baseline; justify-content: center;
        gap: 0 18px; max-width: 980px; white-space: nowrap;
        background: linear-gradient(
          168deg,
          rgba(52, 54, 78, 0.78) 0%,
          rgba(18, 19, 30, 0.83) 54%,
          rgba(9, 10, 17, 0.87) 100%
        );
        border: 1.6px solid rgba(255, 255, 255, 0.22);
        border-radius: 30px; padding: 20px 46px;
        box-shadow:
          0 30px 72px rgba(0, 0, 0, 0.55),
          inset 0 2px 0 rgba(255, 255, 255, 0.42),
          inset 0 -18px 36px rgba(0, 0, 0, 0.46);
        overflow: hidden;
      }
      .pill::before {
        content: "";
        position: absolute; left: 0; right: 0; top: 0; height: 52%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0));
        pointer-events: none;
      }
      .pill::after {
        content: "";
        position: absolute; inset: 0; border-radius: 30px;
        box-shadow: inset 0 0 26px rgba(255, 255, 255, 0.07);
        pointer-events: none;
      }
      .pill.mx {
        border-color: rgba(0, 255, 120, 0.42);
        box-shadow:
          0 30px 72px rgba(0, 0, 0, 0.55),
          0 0 54px rgba(0, 255, 90, 0.22),
          inset 0 2px 0 rgba(170, 255, 205, 0.42),
          inset 0 -18px 36px rgba(0, 0, 0, 0.46);
      }
      .w { display: inline-block; opacity: 0; line-height: 1.05; font-family: "Rubik", sans-serif; }
      .w-ed { font-weight: 700; font-size: 72px; color: #f5f0d0; }
      .w-ed-emph { font-weight: 900; font-size: 92px; color: #ffffff; }
      .w-mx {
        font-weight: 800; font-size: 64px; color: #00ff41;
        letter-spacing: 0.01em;
        text-shadow: 0 0 22px rgba(0, 255, 65, 0.5);
      }
      .sc, .rl { display: none; }
    </style>
  </head>
  <body>
    <div
      id="caption-body"
      data-composition-id="caption-body"
      data-timeline-locked
      data-start="0"
      data-duration="__DURATION__"
      data-fps="30"
      data-width="1080"
      data-height="1920"
    >
      <div id="cb-stage"></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};
        function mulberry32(a) {
          return function () {
            a |= 0; a = (a + 0x6d2b79f5) | 0;
            var t = Math.imul(a ^ (a >>> 15), 1 | a);
            t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
          };
        }
        // Hebrew alphabet for the matrix scramble.
        var GLYPH = "אבגדהוזחטיכלמנסעפצקרשתאבגדהוזחטיכ";
        function scr(seed, n) {
          var r = mulberry32(seed), s = "";
          for (var i = 0; i < n; i++) s += GLYPH[Math.floor(r() * GLYPH.length)];
          return s;
        }
        function fit(text, weight, max) {
          var c = fit._c || (fit._c = document.createElement("canvas").getContext("2d"));
          var size = 60, min = 30;
          while (size > min) { c.font = weight + " " + size + "px Rubik"; if (c.measureText(text).width <= max) break; size -= 2; }
          return size;
        }

        var DATA = __DATA__;
        var stage = document.getElementById("cb-stage");
        var tl = gsap.timeline({ paused: true });

        DATA.forEach(function (g, gi) {
          var cg = document.createElement("div");
          cg.className = "cg"; cg.id = "cg-" + gi;
          var pill = document.createElement("div");
          pill.className = "pill" + (g.st === "mx" ? " mx" : "");
          var joined = g.words.map(function (w) { return w.t; }).join(" ");
          var weight = g.st === "mx" ? "800" : "700";
          var fs = fit(joined, weight, 900);
          g.words.forEach(function (w, wi) {
            var sp = document.createElement("span");
            sp.id = "w-" + gi + "-" + wi;
            if (g.st === "mx") {
              sp.className = "w w-mx"; sp.style.fontSize = fs + "px";
              var letters = w.t.replace(/[^֐-׿]/g, "");
              var n = Math.max(2, Math.min(7, letters.length || w.t.length));
              var rl = document.createElement("span"); rl.className = "rl"; rl.id = "rl-" + gi + "-" + wi; rl.textContent = w.t;
              var s0 = document.createElement("span"); s0.className = "sc"; s0.id = "s0-" + gi + "-" + wi; s0.textContent = scr(gi * 97 + wi, n);
              var s1 = document.createElement("span"); s1.className = "sc"; s1.id = "s1-" + gi + "-" + wi; s1.textContent = scr(gi * 97 + wi + 5000, n);
              sp.appendChild(rl); sp.appendChild(s0); sp.appendChild(s1);
            } else {
              sp.className = "w " + (w.emph ? "w-ed-emph" : "w-ed");
              if (!w.emph) sp.style.fontSize = fs + "px";
              else sp.style.fontSize = Math.round(fs * 1.26) + "px";
              sp.textContent = w.t;
            }
            pill.appendChild(sp);
          });
          cg.appendChild(pill); stage.appendChild(cg);
        });

        DATA.forEach(function (g, gi) {
          var cg = document.getElementById("cg-" + gi);
          tl.fromTo(
            cg,
            { opacity: 0, y: 32, scaleX: 1.16, scaleY: 0.72 },
            { opacity: 1, y: 0, scaleX: 1, scaleY: 1, duration: 0.46, ease: "elastic.out(1, 0.78)" },
            g.s,
          );
          g.words.forEach(function (w, wi) {
            var el = document.getElementById("w-" + gi + "-" + wi);
            var wt = g.s + 0.05 + wi * 0.07;
            if (g.st === "mx") {
              var rl = document.getElementById("rl-" + gi + "-" + wi);
              var s0 = document.getElementById("s0-" + gi + "-" + wi);
              var s1 = document.getElementById("s1-" + gi + "-" + wi);
              tl.set(el, { opacity: 1 }, wt);
              tl.set(s0, { display: "inline" }, wt);
              tl.set(s0, { display: "none" }, wt + 0.09);
              tl.set(s1, { display: "inline" }, wt + 0.09);
              tl.set(s1, { display: "none" }, wt + 0.18);
              tl.set(rl, { display: "inline" }, wt + 0.18);
            } else {
              tl.fromTo(el, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }, wt);
            }
          });
          var outAt = g.e;
          tl.to(cg, { opacity: 0, y: -20, scaleY: 0.8, duration: 0.18, ease: "power2.in" }, outAt - 0.18);
          tl.set(cg, { opacity: 0, visibility: "hidden" }, outAt);
        });

        window.__timelines["caption-body"] = tl;
      })();
    </script>
  </body>
</html>
"""

html = TEMPLATE.replace("__DURATION__", str(DURATION)).replace("__DATA__", DATA_JSON)
with io.open("compositions/components/caption-body.html", "w", encoding="utf-8") as f:
    f.write(html)
print("wrote compositions/components/caption-body.html")
