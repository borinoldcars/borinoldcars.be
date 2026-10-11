"""Conversion des vidéos d'albums (Google Drive -> dossier videos/, MP4 lisible partout).

Les vidéos d'iPhone (HEVC, souvent HDR) ne s'affichent pas dans la plupart des navigateurs :
on entend le son mais l'image reste noire. Ce script lit les albums de l'application
(photos.json), télécharge chaque vidéo publique, la convertit en MP4 H.264 (1280 px max,
couleurs HDR ramenées en standard) avec une image d'aperçu, puis écrit videos/index.json
("id-du-fichier-Drive": {"mp4": "videos/id.mp4", "poster": "videos/id.jpg"}).
Une vidéo déjà convertie n'est pas refaite.
"""
import html, json, os, re, subprocess, sys, tempfile, urllib.parse, urllib.request

PHOTOS = "https://borinoldcars.github.io/app/data/photos.json"
OUT = "videos"
MAX_MB = 90  # limite GitHub : 100 Mo par fichier

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (borinoldcars.be)"})
    return urllib.request.urlopen(req, timeout=300)

def download(fid, dest):
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    with get(url) as r:
        if "text/html" in r.headers.get("Content-Type", ""):
            # Page « impossible d'analyser ce fichier » : on suit son formulaire de confirmation.
            page = r.read().decode("utf-8", "replace")
            form = re.search(r'<form[^>]+action="([^"]+)"', page)
            if not form:
                raise RuntimeError("vidéo non partagée publiquement ?")
            fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', page))
            url = html.unescape(form.group(1)) + "?" + urllib.parse.urlencode(fields)
            r = get(url)
            if "text/html" in r.headers.get("Content-Type", ""):
                raise RuntimeError("téléchargement refusé par Drive")
        with open(dest, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=color_transfer:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    transfer = (data.get("streams") or [{}])[0].get("color_transfer", "")
    return transfer, float(data.get("format", {}).get("duration") or 0)

def convert(src, mp4, jpg):
    transfer, duration = probe(src)
    size = "scale=w='min(1280,iw)':h='min(1280,ih)':force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2"
    if transfer in ("arib-std-b67", "smpte2084"):  # HDR (iPhone) -> couleurs standard
        vf = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
              "zscale=t=bt709:m=bt709:r=tv,format=yuv420p," + size)
    else:
        vf = size + ",format=yuv420p"
    for crf in (24, 28, 32):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "slow",
                        "-crf", str(crf), "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-ac", "2",
                        "-movflags", "+faststart", mp4], check=True)
        if os.path.getsize(mp4) < MAX_MB * 1e6:
            break
    else:
        os.remove(mp4)
        raise RuntimeError("vidéo trop longue pour être copiée sur le site")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(min(1.0, duration / 2)), "-i", mp4,
                    "-frames:v", "1", "-vf", "scale=w='min(640,iw)':h=-2", "-q:v", "4", jpg], check=True)

def main():
    with get(PHOTOS) as r:
        albums = json.load(r).get("albums", [])
    os.makedirs(OUT, exist_ok=True)
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    for fid in [v for a in albums for v in (a.get("videos") or [])]:
        mp4, jpg = f"{OUT}/{fid}.mp4", f"{OUT}/{fid}.jpg"
        if fid in index and os.path.exists(mp4):
            continue
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "source")
            try:  # une vidéo en échec n'arrête pas les autres
                download(fid, src)
                convert(src, mp4, jpg)
            except Exception as e:
                print("échec", fid, e, file=sys.stderr)
                continue
        index[fid] = {"mp4": mp4, "poster": jpg}
        print("convertie", mp4, f"{os.path.getsize(mp4) / 1e6:.1f} Mo")
    json.dump(index, open(index_path, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
