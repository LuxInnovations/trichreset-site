"""Make the Learn page images with Gemini: about trichotillomania, in the brand palette.

  python tools/learn_art.py [name ...]     (no names = all)

Writes assets/img/learn/<name>.jpg + .webp at 720px. The meditation covers are the palette reference.
Rules: show hair, hands and calming tools, never pulling, bald patches or a recognisable face
(images of pulling can trigger readers). Brand-only: never Victoria.
"""
import base64, io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "assets", "img", "learn")
REFS = [os.path.join(SITE, "assets", "img", "covers", f + ".jpg") for f in ("hands_at_rest", "calm_hands_kind_mind", "the_quiet_hour")]
MODEL = "gemini-3-pro-image"

STYLE = ("Square editorial photograph for a calm, trustworthy website about trichotillomania (hair pulling disorder). "
         "Use the colour mood of the reference images: deep navy, soft lavender and pale pink light, gentle and hopeful. "
         "Real photography, natural skin, soft window or evening light, shallow depth of field, uncluttered. "
         "Never show hair being pulled, fingers gripping or twisting hair, plucked hairs, bald patches or tweezers. "
         "No visible face. No text, no logos, no borders.")

ART = {
    # v2 (15 Oct): things only people with trich recognise, instead of generic wellness stock.
    "hub-v2": "Top-down flat lay on a soft lavender knit blanket: a trich toolkit neatly arranged, a textured fidget ring, a squishy stress ball, a soft beanie, thin cotton gloves, a scrunchie, a smooth worry stone, a hairbrush and a phone with a dark calm screen. Soft evening light, tidy, gentle.",
    "what-is-v2": "Late at night in bed in a dark bedroom, seen from behind and above the pillow, a woman lying on her side with long hair spread loose on the pillow, her phone glowing softly in one hand, her other hand resting flat on the duvet away from her hair. Quiet, relatable, the moment pulling usually starts. No face visible.",
    "treatment-v2": "Close-up of an open notebook used as an urge log: the page shows only a ruled grid and rows of small simple tally marks in pencil, no words or letters at all, a pen resting on it, a smooth worry stone beside the notebook, warm cup of tea at the edge, shallow depth of field.",
    "adhd": "A cosy study desk at night lit by a small warm lamp: an open laptop with a dark screen, an open textbook, a few blank sticky notes, a half-finished cup of tea, and one hand resting on the desk turning a textured fidget cube. A soft knitted beanie sits on the chair back. Calm, relatable, a busy mind at rest. No face visible.",
    "how-to-stop-v2": "A small bathroom vanity mirror with a soft lavender towel draped over it so the glass is covered, a satin scrunchie and a simple fidget spinner resting on the sink below, calm soft evening light. No person.",
}


def gen(name):
    parts = [{"text": "Reference images for colour and mood only:"}]
    for r in REFS:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(open(r, "rb").read()).decode()}})
    parts.append({"text": f"{STYLE}\n\nSubject: {ART[name]}"})
    body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    img = next(p["inlineData"]["data"] for p in d["candidates"][0]["content"]["parts"] if "inlineData" in p)
    im = Image.open(io.BytesIO(base64.b64decode(img))).convert("RGB").resize((720, 720), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{name}.jpg"), quality=82, optimize=True, progressive=True)
    im.save(os.path.join(OUT, f"{name}.webp"), quality=80, method=6)
    print("made", name, flush=True)


def safe(name):
    try:
        gen(name)
    except Exception as e:
        print("FAILED", name, e, flush=True)


with ThreadPoolExecutor(4) as ex:
    list(ex.map(safe, sys.argv[1:] or list(ART)))
