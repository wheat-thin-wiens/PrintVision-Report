from .gooey import create_gui
from .spreadsheet import open_file, which_csv, csv_report
from .web import login, which_html, html_report

try:
    from .creds import username, password
    credsPresent = True
except ImportError:
    credPresent = False
    pass
