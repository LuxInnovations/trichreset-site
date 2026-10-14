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
    "hub": "Exactly one young woman, alone, seen from directly behind, sitting calmly on a window seat at dusk looking out, wearing a soft knit jumper, her long dark hair falling loose and untouched down her back. No reflections, no second person. Peaceful.",
    "what-is": "Close-up from behind of long healthy wavy hair falling down the back of a woman wearing a soft lavender knit jumper, soft evening light catching individual strands, hands not in frame.",
    "treatment": "A woman's hands holding a small open notebook and a pen on her lap, writing a short note, a warm cup of tea beside her, calm evening light, face out of frame.",
    "how-to-stop": "A woman's relaxed hands resting together, one holding a smooth grey pebble and gently rubbing it with her thumb, soft blanket on her lap, face out of frame.",
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
