import os
import time
import uuid
import base64
import requests

from dotenv import load_dotenv

load_dotenv()
CLOVA_SECRET_KEY = os.getenv("CLOVA_SECRET_KEY")
CLOVA_INVOKE_URL = os.getenv("CLOVA_INVOKE_URL")


def request_to_clova(uploaded_files):
    images = []
    for file in uploaded_files:
        file_bytes = file.read()
        base64_bytes = base64.b64encode(file_bytes)
        base64_string = base64_bytes.decode("utf-8")

        images.append({
            'format': 'png',
            'name': file.name,
            'data': base64_string
        })

    request_json = {
        'version': 'V2',
        'requestId': str(uuid.uuid4()),
        'timestamp': int(round(time.time() * 1000)),
        'images': images,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-OCR-SECRET': CLOVA_SECRET_KEY
    }

    return requests.post(
        url=CLOVA_INVOKE_URL,
        data=request_json,
        headers=headers,
    )

