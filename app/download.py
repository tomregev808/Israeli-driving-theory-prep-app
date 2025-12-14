
import argparse
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
import requests

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
    p = argparse.ArgumentParser(description="Download a single URL to disk (test).")
    p.add_argument("--url", "-u", required=True, help="The URL to download")
    p.add_argument("--outdir", "-o", default="./downloads", help="Output directory")
    p.add_argument("--timeout", type=int, default=20, help="Request timeout (seconds)")
    p.add_argument("--no-verify", action="store_true", help="Disable SSL cert verification (not recommended)")
    args = p.parse_args()

    result = download_one(args.url, outdir=args.outdir, timeout=args.timeout, verify_ssl=not args.no_verify)
    if not result.get("ok"):
        print("Download failed:", result.get("error") or result.get("status_code"))
        if result.get("snippet"):
            print("Response snippet (first 500 chars):")
            print(result["snippet"])
    else:
        print("Done.")

if __name__ == "__main__":
    main()

