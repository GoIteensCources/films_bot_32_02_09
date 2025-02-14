import json
from typing import Optional


def get_data(file_path: str, film_id: Optional[int] = None) -> list[dict]:
    with open(file_path, "r") as fp:
        data = json.load(fp)

        if film_id != None and film_id<len(data):
            return data[film_id]
        return data


def add_film_to_db(film:dict, file_path: str) -> None:
    data = get_data(file_path)
    data.append(film)
    
    with open(file_path, "w") as fp:
        json.dump(data, 
                  fp, 
                  indent=4,
                  ensure_ascii=True)
    