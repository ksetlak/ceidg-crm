import json
import requests

def construct_headers(config):
    return {'Authorization': f'Bearer {config.TOKEN}'}



def get_new_companies(config, date_text):
    url = config.BASE_URL + "/firmy"
    url += "?" + f"dataod={date_text}"
    request = requests.get(url, headers=construct_headers(config))
    print(f"get_new_companies: Request to CEiDG API done with the following status: {request.status_code}.")
    companies = json.loads(request.content)["firmy"]
    return companies


def get_company_details(config, nip):
    URL = config.BASE_URL + "/firma"
    nip = str(nip)
    URL += "?" + "nip=" + nip
    request = requests.get(URL, headers=construct_headers(config))
    print(f"Request to CEiDG API done with the following status: {request.status_code}.")
    details = json.loads(request.content)["firma"][0]
    return details

