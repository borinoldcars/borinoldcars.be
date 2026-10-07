"""Copie locale des affiches de l'agenda (Google Drive -> dossier affiches/).

Lit l'agenda de l'application (events.json), télécharge chaque affiche Google Drive en taille
moyenne et écrit affiches/index.json ("id-du-fichier-Drive": "affiches/fichier").
Le site affiche ces copies : il ne dépend plus de l'affichage direct depuis Drive.
"""
import json, os, re, urllib.request

EVENTS = "https://borinoldcars.github.io/app/data/events.json"
OUT = "affiches"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (borinoldcars.be)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get("Content-Type", "")

def main():
    events = json.loads(get(EVENTS)[0]).get("events", [])
    os.makedirs(OUT, exist_ok=True)
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    for ev in events:
        m = re.search(r"[?&]id=([\w-]+)|/d/([\w-]+)", ev.get("image") or "")
        if not m:
            continue
        fid = m.group(1) or m.group(2)
        try:
            data, ctype = get(f"https://drive.google.com/thumbnail?id={fid}&sz=w1200")
        except Exception as e:  # une affiche indisponible n'arrête pas les autres
            print("échec", fid, e)
            continue
        if not ctype.startswith("image/") or len(data) < 1000:
            print("pas une image", fid, ctype)
            continue
        ext = ".png" if "png" in ctype else ".jpg"
        name = f"{OUT}/{fid}{ext}"
        if not os.path.exists(name) or open(name, "rb").read() != data:
            open(name, "wb").write(data)
            print("mise à jour", name)
        index[fid] = name
    json.dump(index, open(index_path, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
