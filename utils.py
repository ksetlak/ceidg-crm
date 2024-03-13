import webbrowser


def company_to_tuple(company):
    contacted_text = ["Nie", "Tak"][int(company.contacted)]
    return company.nip, company.name, company.email, company.phone, contacted_text


def view_company_in_browser(uuid):
    webbrowser.open(f"https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/SearchDetails.aspx?Id={uuid}")
    