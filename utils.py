import network

def view_company_details(nip):
    company_id = network.get_company_id(nip)  # TODO: Get from the database instead of from network.
    url = f'https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/SearchDetails.aspx?Id={company_id}'

def row_to_dict(row):  # Unused
    dictionary = dict()
    for column in row.__table__.columns:
        dictionary[column.name] = str(getattr(row, column.name))
    return dictionary

def row_to_tuple(row):  # Unused
    tuple = (getattr(row, column.name) for column in row.__table__.columns)
    return tuple

def company_to_tuple(company):
    # NIP, nazwa, email, telefon, obdzwoniona
    contacted_text = ["Nie", "Tak"][int(company.contacted)]
    return (company.nip, company.name, company.email, company.phone, contacted_text)
