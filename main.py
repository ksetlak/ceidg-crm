# TODO: Insert **or ignore** into the database. https://stackoverflow.com/a/19343100/5306048
import argparse
cmdlinearg_parser = argparse.ArgumentParser(
    prog="CEiDG-CRM",
    usage="""USAGE""",
    description="""DESCRIPTION""",
    epilog="""EPILOG"""
)
cmdlinearg_parser.add_argument("--test-config", action=argparse.BooleanOptionalAction, help="Use a test configuration instead of the production one.")
cmdlinearg_parser.set_defaults(test_config=False)
cmdlineargs = cmdlinearg_parser.parse_args()

if cmdlineargs.test_config:
    import test_config as config
else:
    import prod_config as config

import gui
from datetime import datetime as dt
import logic, network, models
from sqlalchemy import create_engine

db_engine = create_engine("sqlite:///ceidg-crm.db", echo=True)
models.Base.metadata.create_all(db_engine)

date_text = dt.now().strftime("%Y-%m-%d")
payload = network.get_new_companies(config, date_text)
logic.update_database(payload)


gui = gui.GUI(config)
def toggle_contacted_state(event):
    pass





# URL = config.BASE_URL + "/firma"
# URL += "?" + "nip=" + "9241211252"
# request = requests.get(URL, headers=headers)
# print(f"Request to CEiDG API done with the following status: {request.status_code}.")
# print(request.content)







# URL = config.BASE_URL + "/raporty"
# params = [
#     f"dataod={dt.now().strftime("%Y-%m-18")}",  # DEBUG
#     f"datado={dt.now().strftime("%Y-%m-19")}"  # DEBUG
# ]
# URL += "?" + "&".join(params)
# request = requests.get(URL, headers=headers)
# print(f"Request to CEiDG API done with the following status: {request.status_code}.")
# 
# reports = json.loads(request.content)["raporty"]
# 
# nazwy = set()
# # print(reports)
# for report in reports:
#     nazwy.add(report["nazwa"])
#     # if report["nazwa"].startswith("Złożone wnioski"):
#     if report["nazwa"].startswith("Zarejestrowane działalności"):
#         report_id = report["id"]
#         print(report_id)
#         break
# 
# URL = config.BASE_URL + f"/raport/{report_id}"
# print(URL)
# request = requests.get(URL, headers=headers)
# print(f"Request to CEiDG API done with the following status: {request.status_code}.")
# 
# with open("raport.zip", 'wb') as zip_file:
#     zip_file.write(request.content)
