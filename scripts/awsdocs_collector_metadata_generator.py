from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path
import requests
import json

# -------------------------
# PATHS
# -------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
URL_FILE = BASE_DIR / "aws_docs_saves/aws_doc_urls.txt"

RAW_DIR = BASE_DIR / "aws_docs_saves/raw"
CLEAN_DIR = BASE_DIR / "aws_docs_saves/clean"

METADATA_FILE = BASE_DIR / "aws_docs_saves/metadata.json"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------
# LOAD URLS
# -------------------------

with open(URL_FILE, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Found {len(urls)} URLs")


# -------------------------
# HELPERS
# -------------------------


def generate_filename(url: str) -> str:
    path_parts = [p for p in urlparse(url).path.split("/") if p]

    filename = "_".join(path_parts)

    if not filename.endswith(".html"):
        filename += ".html"

    return filename


def clean_html(html_text: str) -> tuple[str, str]:

    soup = BeautifulSoup(html_text, "html.parser")

    # Remove junk tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Extract title
    title = soup.title.string.strip() if soup.title else "Untitled"  # type: ignore

    # Extract clean text
    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]

    clean_text = "\n".join(line for line in lines if line)

    return clean_text, title


# -------------------------
# METADATA STORAGE
# -------------------------

metadata = {}


# -------------------------
# MAIN LOOP
# -------------------------

for i, url in enumerate(urls, start=1):

    try:
        print(f"[{i}/{len(urls)}] Processing {url}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        html_content = response.text

        # -------------------------
        # SAVE RAW HTML
        # -------------------------

        html_filename = generate_filename(url)

        raw_path = RAW_DIR / html_filename

        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # -------------------------
        # CLEAN HTML
        # -------------------------

        clean_text, title = clean_html(html_content)

        txt_filename = raw_path.stem + ".txt"

        clean_path = CLEAN_DIR / txt_filename

        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(clean_text)

        # -------------------------
        # STORE METADATA
        # -------------------------

        metadata[txt_filename] = {"title": title, "url": url}

        print(f"Saved: {txt_filename}")

    except Exception as e:
        print(f"Failed: {url}")
        print(e)


# -------------------------
# SAVE METADATA.JSON
# -------------------------

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print("Done.")
print(f"Metadata saved to: {METADATA_FILE}")
