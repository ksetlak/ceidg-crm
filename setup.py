from cx_Freeze import setup, Executable

VERSION = "0.1.0"

msi_options = dict(
    target_name=f'CEiDG-CRM-{VERSION.replace(".", "_")}.msi',
    upgrade_code='{fdb31120-1b7f-4c35-94e3-d7cafcd4ee23}'  # Thanks https://www.guidgenerator.com/online-guid-generator.aspx!
)

setup(name='CEiDG-CRM',
      version=VERSION,
      description='A PoC for software you can use to contact newly registered sole proprietorships in Poland to offer them your services.',
      executables=[Executable('ceidg-crm.pyw',
                              base='Win32GUI',
                              targetName='ceidg-crm.exe',
                              # icon='assets/inverter.ico',
                              shortcutName='CEiDG-CRM',
                              shortcutDir='StartMenuFolder'
                              )])
