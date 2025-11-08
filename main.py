import gzip
import json

import requests

DUMP_FILE = "https://anime-titles.dat.gz"
OUTPUT_JSON = "anidb_titles.json"


def download_and_extract_data(url):
    response = requests.get(url)
    response.raise_for_status()
    compressed_data = response.content
    return gzip.decompress(compressed_data).decode("utf-8")


def parse_data(data):
    anime_map = {}
    lines = data.splitlines()

    for line in lines[3:]:
        parts = line.split("|")
        if len(parts) != 4:
            continue

        aid, title_type, language, title = parts
        aid = int(aid)
        title_type = int(title_type)
        anime_map.setdefault(aid, {"id": aid, "titles": []})
        anime_map[aid]["titles"].append(
            {"type": title_type, "language": language, "title": title}
        )

    return list(anime_map.values())


if __name__ == "__main__":
    extracted_data = download_and_extract_data(DUMP_FILE)
    parsed_data = parse_data(extracted_data)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(parsed_data, json_file, ensure_ascii=False, indent=2)
    print(f"Data has been written to {OUTPUT_JSON}")
