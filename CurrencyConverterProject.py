from requests import get
from pprint import PrettyPrinter

API_KEY = "562ddaf40c95f5d58108" 
BASE_URL = "https://free.currconv.com/"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    request_url = BASE_URL + endpoint

    data = get(request_url).json()

    printer.pprint(data)

get_currencies()

