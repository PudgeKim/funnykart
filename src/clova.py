import json
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
    files = []

    for file in uploaded_files:
        images.append({
            'format': 'png',
            'name': file.name
        })

        files.append(('file', file.getvalue()))

    request_json = {
        'version': 'V2',
        'requestId': str(uuid.uuid4()),
        'timestamp': int(round(time.time() * 1000)),
        'images': images,
    }
    payload = {
        'message': json.dumps(request_json).encode('UTF-8')
    }
    headers = {
        'X-OCR-SECRET': CLOVA_SECRET_KEY
    }

    return requests.post(
        url=CLOVA_INVOKE_URL,
        headers=headers,
        data=payload,
        files=files,
    )

