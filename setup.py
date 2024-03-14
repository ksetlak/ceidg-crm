from cx_Freeze import setup, Executable

VERSION = "0.1.0"

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": [], "excludes": []}
bdist_msi_options = dict(
    target_name=f"CEiDG-CRM-{VERSION.replace('.', '_')}.msi",
    upgrade_code="{fdb31120-1b7f-4c35-94e3-d7cafcd4ee23}"
    # Thanks https://www.guidgenerator.com/online-guid-generator.aspx!
)

base = 'Win32GUI'

executables = [
    Executable("main.py",
               base=base,
               target_name="CEiDG-CRM",
               shortcut_name="CEiDG-CRM",
               shortcut_dir="StartMenuFolder")
]

setup(name="CEiDG-CRM",
      version="0.1.0",
      description="A PoC for software that lets you discover newly registered sole proprietorships so that you can offer them your services.",
      options={"build_exe": build_options, "bdist_msi": bdist_msi_options},
      executables=executables)
