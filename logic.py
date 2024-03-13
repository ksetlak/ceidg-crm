import time
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
    page = 0
    while True:
        companies, last_page = network.get_new_companies(config, date_text, page)
        companies = [models.dict_to_company(company) for company in companies]
        with Session(config.db_engine) as session:
            stmt = insert(models.Company)
            values = []
            for company in companies:
                val = company.__dict__
                del (val["_sa_instance_state"])
                values.append(val)
            stmt = stmt.values(values)
            stmt = stmt.on_conflict_do_nothing(index_elements=['nip'])
            session.execute(stmt)
            session.commit()
        if page == last_page:
            break
        time.sleep(3.6)
        page += 1


def update_contact_info(config):
    with Session(config.db_engine) as session:
        query_results = select(models.Company).where(models.Company.status == models.CompanyState.NEW)
        for company in session.scalars(query_results):
            details = network.get_company_details(config, company.nip)
            if "telefon" in details or "email" in details:
                company.status = models.CompanyState.DATA_RETRIEVED
                if "telefon" in details:
                    company.phone = details["telefon"]
                if "email" in details:
                    company.email = details["email"]
            else:
                company.status = models.CompanyState.DATA_UNAVAILABLE
            session.commit()
            time.sleep(3.6)


def toggle_contacted_state(db_engine, nip):  # TODO Refactor this and button_toggle_company_command() to rely on UUID.
    with Session(db_engine) as session:
        query_results = select(models.Company).where(models.Company.nip == nip)
        company = session.scalars(query_results).one()
        company.contacted = not company.contacted
        session.commit()


def get_company_by_nip(db_engine, nip):
    with Session(db_engine) as session:
        query_results = select(models.Company).where(models.Company.nip == nip)
        company = session.scalars(query_results).one()
        return company
