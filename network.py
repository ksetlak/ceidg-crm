import json
import requests


def get_new_companies(config, date_text):
    headers = {'Authorization': f'Bearer {config.TOKEN}'}
    url = config.BASE_URL + "/firmy"
    url += "?" + f"dataod={date_text}"
    request = requests.get(url, headers=headers)
    print(f"get_new_companies: Request to CEiDG API done with the following status: {request.status_code}.")
    companies = json.loads(request.content)
    return companies


def get_company_id(token, nip):
    pass
