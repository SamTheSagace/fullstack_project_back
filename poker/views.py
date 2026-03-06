from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from poker.controllers.items_controller import ItemController
from poker.controllers.sessions_controller import SessionController
from poker.controllers.session_member_controller import SessionMemberController

item_controller = ItemController()
session_controller = SessionController()
session_member_controller = SessionMemberController()


@csrf_exempt
def sessions(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return session_controller.create(request)
    elif request.method == "GET":
        return session_controller.list(request)
    return JsonResponse({"error": "Method not allowed."}, status=405)

@csrf_exempt
def delete_session(request: HttpRequest) -> HttpResponse:
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed."}, status=405)
    return session_controller.delete(request)


@csrf_exempt
@require_POST
def join_session(request: HttpRequest) -> HttpResponse:
    return session_member_controller.join_session(request)

@csrf_exempt
@require_POST
def create_session_member(request: HttpRequest) -> HttpResponse:
    return session_member_controller.create(request)

@csrf_exempt
@require_POST
def leave_session(request: HttpRequest) -> HttpResponse:
    return session_member_controller.leave_session(request)


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
def get_item_By_id(request: HttpRequest, id: int):
    item = item_controller.get_by_id(request, id)
    if item:
        return JsonResponse(model_to_dict(item), status=200, safe=False)
    else:
        return JsonResponse({"error": "Item not found."}, status=404)

@csrf_exempt
@require_POST
def create_item(request: HttpRequest):
    item_controller.create(request)
    return JsonResponse("New item created", status=201)

@csrf_exempt
@require_http_methods(["PUT"])
def update_item(request: HttpRequest, id: int):
    item_controller.update(request, id)
    return JsonResponse("Item updated", status=200, safe=False)
