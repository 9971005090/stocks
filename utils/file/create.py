import os
import json
import io
from email.mime.base import MIMEBase
from email import encoders

__all__ = ['GET_JSON_ATTACHMENT']

def GET_JSON_ATTACHMENT(data, filename = "data.json"):
    json_bytes = io.BytesIO(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))
    part = MIMEBase("application", "octet-stream")
    part.set_payload(json_bytes.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    return part