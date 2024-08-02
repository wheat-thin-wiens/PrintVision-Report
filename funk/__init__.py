from .web import Web_Report

try:
    import creds
    credsPresent = True
except ImportError:
    credPresent = False
    pass