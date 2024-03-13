import argparse
import gui
import models
from sqlalchemy import create_engine

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

config.db_engine = create_engine("sqlite:///ceidg-crm.db", echo=True)
models.Base.metadata.create_all(config.db_engine)

gui = gui.GUI(config)

# TODO FEATURE Add "last DB update" in GUI.
# TODO FEATURE Add a widget to set scan date.
# TODO FEATURE Add a widget to filter the table: only not contacted, only with a phone number.
