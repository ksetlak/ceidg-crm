import json
import requests


def construct_headers(config):
    return {'Authorization': f'Bearer {config.TOKEN}'}

def error_logging_request(url, headers):
    request = requests.get(url, headers=headers)
    if request.status_code != 200:
        print(f"Request to CEiDG API failed with the following status: {request.status_code}.")
        print(f"URL: {url}")
        print("Response content:")
        print(request.content)
    return request

def get_new_companies(config, date_text, page):
    url = config.BASE_URL + "/firmy"
    url += "?" + f"dataod={date_text}" + "&" + f"page={page}"
    request = error_logging_request(url=url, headers=construct_headers(config))
    print(f"get_new_companies: Request to CEiDG API done with the following status: {request.status_code}.")
    companies = json.loads(request.content)["firmy"]
    last_page = int(json.loads(request.content)["links"]["last"].split("&")[-1].split("=")[-1])
    return companies, last_page


def get_company_details(config, nip):
    url = config.BASE_URL + "/firma"
    nip = str(nip)
    url += "?" + "nip=" + nip
    request = error_logging_request(url=url, headers=construct_headers(config))
    print(f"Request to CEiDG API done with the following status: {request.status_code}.")
    details = json.loads(request.content)["firma"][0]
    return details
