import json
from typing import Optional


def get_data(file_path: str, film_id: Optional[int] = None) -> list[dict]:
    with open(file_path, "r") as fp:
        data = json.load(fp)

        if film_id != None and film_id<len(data):
            return data[film_id]
        return data
