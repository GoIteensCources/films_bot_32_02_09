from app.database import get_data
from pprint import pprint

DATABASE = "data.json"

pprint(get_data(DATABASE))
