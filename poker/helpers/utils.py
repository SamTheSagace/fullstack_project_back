import json
import secrets
import string
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse

CODE_LENGTH = 6
CODE_ALPHABET = string.ascii_uppercase + string.digits


def generate_session_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def parse_json_body(request: HttpRequest) -> tuple[dict[str, Any] | None, HttpResponse | None]:
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JsonResponse({"error": "Invalid JSON body."}, status=400)

    if not isinstance(payload, dict):
        return None, JsonResponse({"error": "JSON body must be an object."}, status=400)

    return payload, None
