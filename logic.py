import json
import models
import network
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime as dt


def get_all_companies(db_engine):
    session = Session(db_engine)
    query_results = select(models.Company)
    companies = [company for company in session.scalars(query_results)] 
    return companies

def update_database(db_engine):
    pass
    # network.get_new_companies(config, date_text)
    
    # i = 0
    # for firma in firmy["firmy"][:10]:  # DEBUG
    #     company_id = firma["id"]
    #     URL = config.BASE_URL + "/firma"
    #     URL += f"/{company_id}"
    #     request = requests.get(URL, headers=headers)
    #     print(f"Request to CEiDG API done with the following status: {request.status_code}.")
    #     # print(request.content)  # DEBUG
    #     payload = json.loads(request.content.decode('utf-8'))
    #     company = payload["firma"][0]
    #     filtered = dict()
    #     if "telefon" in company:
    #         filtered["telefon"] = company["telefon"]
    #     if "email" in company:
    #         filtered["email"] = company["email"]
    #     if filtered:
    #         print("HIT!")  # DEBUG
    #         filtered["nip"] = company["wlasciciel"]["nip"]
    #         filtered["nazwa"] = company["nazwa"]
    #         if "telefon" not in filtered:
    #             filtered["telefon"] = ""
    #         if "email" not in filtered:
    #             filtered["email"] = ""
    #         with Session(db_engine) as session:
    #             new_company = models.Company(
    #                     name=filtered["nazwa"],
    #                     nip=int(filtered["nip"]),
    #                     email=filtered["email"],
    #                     phone=filtered["telefon"]
    #                 )
    #             session.add(new_company)
    #             session.commit()
    #     # with open(f"firma_{i}.json", 'w', encoding='utf-8') as jsonfile:  # Encoding just to be sure things don't get messed up on Windows.
    #     #     jsonfile.write(json.dumps(json.loads(request.content), ensure_ascii=False, indent=4))
    #     i += 1

