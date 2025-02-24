from pprint import pprint

from app.database import get_data

DATABASE = "data.json"

pprint(get_data(DATABASE))
