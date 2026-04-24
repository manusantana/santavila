import re
from pathlib import Path

def get_env_var(key):
    try:
        content = (Path(__file__).parent / ".env").read_text(encoding="utf-8")
        match = re.search(rf"^{key}=(.*)", content, re.MULTILINE)
        return match.group(1).strip() if match else ""
    except Exception:
        return ""

SHOPIFY_ACCESS_TOKEN = get_env_var("SHOPIFY_ACCESS_TOKEN")
HF_TOKEN = get_env_var("HF_TOKEN")
REMOVEBG_KEY = get_env_var("REMOVEBG_KEY")
