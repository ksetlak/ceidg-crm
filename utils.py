def company_to_tuple(company):
    contacted_text = ["Nie", "Tak"][int(company.contacted)]
    return company.nip, company.name, company.email, company.phone, contacted_text
