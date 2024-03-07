import network

def view_company_details(nip):
    company_id = network.get_company_id(nip)  # TODO: Get from the database instead of from network.
    url = f'https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/SearchDetails.aspx?Id={company_id}'