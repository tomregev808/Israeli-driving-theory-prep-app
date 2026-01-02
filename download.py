
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
import requests
from app import create_app
from app.db import get_db
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                     "(KHTML, like Gecko) Chrome/119.0 Safari/537.36"

def filename_from_url(url, fallback="downloaded_file"):
    parsed = urlparse(url)
    path = unquote(parsed.path or "")
    name = os.path.basename(path)
    if name and "." in name:
        return name
    # fallback to hostname + simple suffix
    host = parsed.netloc.replace(":", "_") or "host"
    return f"{host}_{fallback}"

def download_one(url, outdir, timeout=20, user_agent=DEFAULT_USER_AGENT, verify_ssl=True):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": user_agent, "Accept": "image/*,*/*;q=0.8"}
    try:
        print(f"Requesting: {url}")
        resp = requests.get(url, headers=headers, timeout=timeout, stream=True, verify=verify_ssl)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return {"ok": False, "error": str(e)}

    print("HTTP status:", resp.status_code)

    if resp.status_code != 200:
        # print a bit of the response body if small (useful to see a captcha page)
        snippet = None
        try:
            snippet = resp.text[:500]
        except Exception:
            pass
        print("Non-200 response. Snippet:", snippet)
        return {"ok": False, "status_code": resp.status_code, "snippet": snippet}

    # determine filename: prefer Content-Disposition, then URL path
    filename = None
    cd = resp.headers.get("content-disposition")
    if cd and "filename=" in cd:
        # basic parsing - not bulletproof for RFC edgecases
        filename = cd.split("filename=")[-1].strip(' ";')
    if not filename:
        filename = filename_from_url(url, fallback="img")
    target = outdir / filename

    # avoid overwrite
    base, ext = os.path.splitext(filename)
    i = 1
    while target.exists():
        target = outdir / f"{base}_{i}{ext or ''}"
        i += 1

    # stream write
    try:
        with open(target, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print("Failed to write file:", e)
        return {"ok": False, "error": f"write-error: {e}"}

    size = target.stat().st_size
    print(f"Saved to: {target} ({size} bytes)")
    return {"ok": True, "filename": str(target), "size": size}

def main():
    download ()



def download ():
    app = create_app()

    with app.app_context():
        db = get_db()
        rows = db.execute(
            "SELECT id, image FROM all_questions WHERE image IS NOT NULL"
        ).fetchall()

        for row in rows:
                download_one (row["image"], 'download')
                print(row["image"])




if __name__ == "__main__":
    main()

