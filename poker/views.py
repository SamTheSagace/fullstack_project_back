import json
import secrets
import string

from django.db import IntegrityError, transaction
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from poker.controllers.items_controller import ItemController
from poker.controllers.votes_controller import VotesController
from poker.serializers import ItemSerializer

from .models import MemberRole, MemberStatus, Session, SessionMember, SessionStatus, Item

item_controller = ItemController()
vote_controller = VotesController()

CODE_LENGTH = 6
CODE_ALPHABET = string.ascii_uppercase + string.digits
MAX_CODE_ATTEMPTS = 20


def generate_session_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def _parse_create_session_payload(request: HttpRequest) -> tuple[dict | None, HttpResponse | None]:
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JsonResponse({"error": "Invalid JSON body."}, status=400)

    name = payload.get("name")
    owner_roblox_user_id = payload.get("owner_roblox_user_id")

    if not isinstance(name, str) or not name.strip():
        return None, JsonResponse({"error": "Field 'name' must be a non-empty string."}, status=400)

    if isinstance(owner_roblox_user_id, bool) or not isinstance(owner_roblox_user_id, int):
        return None, JsonResponse({"error": "Field 'owner_roblox_user_id' must be an integer."}, status=400)

    return {
        "name": name.strip(),
        "owner_roblox_user_id": owner_roblox_user_id,
    }, None


@csrf_exempt
def sessions(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return create_session(request)
    elif request.method == "GET":
        try:
            active_sessions = Session.objects.filter(status=SessionStatus.WAITING).values("code", "name", "created_at")
            return JsonResponse({"sessions": list(active_sessions)}, status=200)
        except Exception:
            return JsonResponse({"error": "Failed to retrieve waiting sessions."}, status=500)
    return JsonResponse({"error": "Method not allowed."}, status=405)

@csrf_exempt
@require_POST
def create_session(request: HttpRequest) -> HttpResponse:
    payload, error_response = _parse_create_session_payload(request)
    if error_response is not None or payload is None:
        return error_response.json() if error_response else JsonResponse({"error": "Invalid payload."}, status=400)

    for _ in range(MAX_CODE_ATTEMPTS):
        code = generate_session_code()
        try:
            with transaction.atomic():
                session = Session.objects.create(
                    code=code,
                    name=payload["name"],
                    status=SessionStatus.WAITING,
                    owner_roblox_user_id=payload["owner_roblox_user_id"],
                )
                SessionMember.objects.create(
                    session=session,
                    roblox_user_id=payload["owner_roblox_user_id"],
                    role=MemberRole.OWNER,
                    status=MemberStatus.ACTIVE,
                )
            return JsonResponse(
                {
                    "code": session.code,
                    "id": session.pk,
                    "name": session.name,
                    "status": session.status,
                    "owner_roblox_user_id": session.owner_roblox_user_id,
                    "created_at": session.created_at.isoformat(),
                },
                status=201,
            )
        except IntegrityError:
            continue

    return JsonResponse({"error": "Could not generate a unique session code."}, status=500)


@require_POST
def join_session(request, code):
    return JsonResponse({"ok": True, "endpoint": "join_session", "code": code})


@require_POST
def add_item(request, code):
    return JsonResponse({"ok": True, "endpoint": "add_item", "code": code})


@require_POST
def start_session(request, code):
    return JsonResponse({"ok": True, "endpoint": "start_session", "code": code})


@require_POST
def vote_current_item(request, code):
    return JsonResponse({"ok": True, "endpoint": "vote_current_item", "code": code})


@require_GET
def get_session_state(request, code):
    return JsonResponse({"ok": True, "endpoint": "get_session_state", "code": code})

@require_GET
def get_item_by_id(request: HttpRequest, id: int):
    item: Item = item_controller.get_by_id(request, id)
    if item:
        item_serialize = ItemSerializer(item)
        return JsonResponse(item_serialize.data, status=200, safe=False)
    else:
        return JsonResponse({"error": "Item not found."}, status=404)
    
@require_GET
def get_item_by_session_id(request: HttpRequest, id: int):
    position = request.GET.get('position')
    try:
        if position is not None:
            item = item_controller.get_by_session_and_position(request, id, int(position))
            item_serialize = ItemSerializer(item)
            return JsonResponse(item_serialize.data, status=200, safe=False)
        else:
            items = item_controller.get_by_session_id(request, id)
            items_serialize = [ItemSerializer(item).data for item in items]
            return JsonResponse(items_serialize, status=200, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)

@csrf_exempt
@require_POST
def create_item(request: HttpRequest):
    item_controller.create(request)
    return JsonResponse("New item created", status=201, safe=False)

@csrf_exempt
@require_http_methods(["PUT"])
def update_item(request: HttpRequest, id: int):
    item_controller.update(request, id)
    return JsonResponse("Item updated", status=200, safe=False)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_item(request: HttpRequest, id: int):
    item_controller.delete(request, id)
    return JsonResponse("Item deleted", status=200, safe=False)

@csrf_exempt
@require_POST
def create_vote(request: HttpRequest):
    vote_controller.create(request)
    return JsonResponse("New vote created", status=201, safe=False)

@csrf_exempt
@require_http_methods(["PUT"])
def update_vote(request: HttpRequest, id: int):
    vote_controller.update(request, id)
    return JsonResponse("Vote updated", status=200, safe=False)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_vote(request: HttpRequest, id: int):
    vote_controller.delete(request, id)
    return JsonResponse("Vote deleted", status=200, safe=False)
