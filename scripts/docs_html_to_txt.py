from bs4 import BeautifulSoup
from pathlib import Path

input_dir = Path("../aws_docs_saves/raw")
output_dir = Path("../aws_docs_saves/clean")
output_dir.mkdir(parents=True, exist_ok=True)


def clean_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # remove junk
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # clean extra blank lines
    lines = [line.strip() for line in text.splitlines()]
    clean_text = "\n".join(line for line in lines if line)

    return clean_text


for html_file in input_dir.glob("*.html"):
    cleaned = clean_html(html_file)

    out_file = output_dir / (html_file.stem + ".txt")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"Cleaned: {html_file.name} → {out_file.name}")

print("Done cleaning all files")
