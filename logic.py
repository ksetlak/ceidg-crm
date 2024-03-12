import models
import network
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from datetime import datetime as dt


def get_all_companies(db_engine):
    with Session(db_engine) as session:
        query_results = select(models.Company)
    companies = [company for company in session.scalars(query_results)] 
    return companies

def get_companies_with_contact_data(db_engine):
    with Session(db_engine) as session:
        query_results = select(models.Company).where(
            or_(models.Company.email != "NONE", models.Company.phone != "NONE")
        )
    companies = [company for company in session.scalars(query_results)]
    return companies

def update_database(config):
    date_text = dt.now().strftime("%Y-%m-%d")
    companies = network.get_new_companies(config, date_text)
    companies = [models.dict_to_company(company) for company in companies]
    with Session(config.db_engine) as session:
        stmt = insert(models.Company)
        values = []
        for company in companies:
            val = company.__dict__
            del(val["_sa_instance_state"])
            values.append(val)
        stmt = stmt.values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=['nip'])
        session.execute(stmt)
        session.commit()

def update_contact_info(config):
    index = 0  # TODO Remove
    with Session(config.db_engine) as session:
        query_results = select(models.Company).where(models.Company.status == models.CompanyState.NEW)
        for company in session.scalars(query_results):
            details = network.get_company_details(config, company.nip)
            # DEBUG TODO Remove
            import json
            with open(f"test_data/firma_{index}.json", 'w', encoding='utf8') as file:
                json.dump(details, file, indent=4)
            index += 1
            # DEBUG TODO Remove
            if "telefon" in details or "email" in details:
                company.status = models.CompanyState.DATA_RETRIEVED
                if "telefon" in details:
                    company.phone = details["telefon"]
                if "email" in details:
                    company.email = details["email"]
                session.commit()
            else:
                company.status = models.CompanyState.DATA_UNAVAILABLE

    
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

def toggle_contacted_state(db_engine, nip):
    with Session(db_engine) as session:
        query_results = select(models.Company).where(models.Company.nip == nip)
        company = session.scalars(query_results).one()
        company.contacted = not company.contacted
        session.commit()
