from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from poker.controllers.items_controller import ItemController
from poker.controllers.sessions_controller import SessionController
from poker.controllers.session_member_controller import SessionMemberController
from poker.controllers.votes_controller import VotesController
from poker.serializers import ItemSerializer

item_controller = ItemController()
session_controller = SessionController()
session_member_controller = SessionMemberController()
vote_controller = VotesController()


@csrf_exempt
def sessions(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return session_controller.create(request)
    elif request.method == "GET":
        return session_controller.list(request)
    return JsonResponse({"error": "Method not allowed."}, status=405)

@csrf_exempt
def delete_session(request: HttpRequest, id: int) -> HttpResponse:
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed."}, status=405)
    return session_controller.delete(request, id)


@csrf_exempt
@require_POST
def join_session(request: HttpRequest, code: str) -> HttpResponse:
    return session_member_controller.join_session(request, session_code=code)

@csrf_exempt
@require_POST
def create_session_member(request: HttpRequest) -> HttpResponse:
    return session_member_controller.create(request)

@csrf_exempt
@require_POST
def leave_session(request: HttpRequest, code: str) -> HttpResponse:
    return session_member_controller.leave_session(request, session_code=code)


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
    return item_controller.get_by_id(request, id)
    
@require_GET
def get_item_by_session_id(request: HttpRequest, id: int):
    position = request.GET.get('position')
    try:
        if position is not None:
            return item_controller.get_by_session_and_position(request, id, int(position))
        else:
            return item_controller.get_by_session_id(request, id)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)

@csrf_exempt
@require_POST
def create_item(request: HttpRequest):
    return item_controller.create(request)

@csrf_exempt
@require_http_methods(["PUT"])
def update_item(request: HttpRequest, id: int):
    return item_controller.update(request, id)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_item(request: HttpRequest, id: int):
    return item_controller.delete(request, id)

@csrf_exempt
@require_POST
def create_vote(request: HttpRequest):
   return vote_controller.create(request)

@csrf_exempt
@require_http_methods(["PUT"])
def update_vote(request: HttpRequest, id: int):
    return vote_controller.update(request, id)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_vote(request: HttpRequest, id: int):
    return vote_controller.delete(request, id)
