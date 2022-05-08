import json

from typing import Dict


class SLData:
    @staticmethod
    def write_html(data) -> None:
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(data)

    @staticmethod
    def read_html() -> str:
        with open('index.html', encoding='utf-8') as file:
            src = file.read()
        return src

    @staticmethod
    def save_json(links: Dict) -> None:
        with open(f"all_links", "w", encoding='utf-8') as file:
            json.dump(links, file, indent=4, ensure_ascii=False)
