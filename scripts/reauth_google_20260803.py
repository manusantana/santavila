#!/usr/bin/env python3
"""Reautoriza el acceso Google (GSC + GA4 readonly) y regenera token.json.

Abre el navegador con el flujo OAuth; al completarlo, sobreescribe token.json.
Uso: .venv/bin/python scripts/reauth_google_20260803.py
"""

import glob
import os

from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/content",
]

secrets = glob.glob(os.path.join(ROOT, ".client_secret_*.json"))
if not secrets:
    raise SystemExit("No se encontro .client_secret_*.json en la raiz del proyecto")

flow = InstalledAppFlow.from_client_secrets_file(secrets[0], SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

token_path = os.path.join(ROOT, "token.json")
with open(token_path, "w", encoding="utf-8") as f:
    f.write(creds.to_json())
print("token.json regenerado en", token_path)
