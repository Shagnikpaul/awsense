import requests
from pathlib import Path
from urllib.parse import urlparse

URL_FILE = Path("../aws_docs_saves/aws_doc_urls.txt")
OUTPUT_DIR = Path("../aws_docs_saves/raw")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(URL_FILE, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Found {len(urls)} URLs")

for i, url in enumerate(urls, start=1):
    try:
        print(f"[{i}/{len(urls)}] Downloading {url}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        path_parts = [p for p in urlparse(url).path.split("/") if p]

        filename = "_".join(path_parts)

        if not filename.endswith(".html"):
            filename += ".html"

        with open(OUTPUT_DIR / filename, "w", encoding="utf-8") as out:
            out.write(response.text)

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

print("Download complete.")