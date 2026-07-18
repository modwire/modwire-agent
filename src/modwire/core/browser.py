from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.static import serve

from modwire.apps.tokens.models.api_key import ApiKey
from modwire.shared.api.siren import PROBLEM_TYPE, SIREN_TYPE, api_root_document


def api_root(request):
    if ApiKey.authenticate(request.headers.get("apikey", "")) is None:
        return JsonResponse(
            {"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Invalid API key"},
            status=401,
            content_type=PROBLEM_TYPE,
        )
    return JsonResponse(api_root_document(request), content_type=SIREN_TYPE)


def browser(request, path=""):
    dist = Path(settings.BASE_DIR) / "browser" / "dist"
    candidate = dist / path
    if path and candidate.is_file():
        return serve(request, path, document_root=dist)
    index = dist / "index.html"
    if index.is_file():
        return FileResponse(index.open("rb"), content_type="text/html")
    return HttpResponse(
        "The API browser has not been built. Run `cd browser && npm install && npm run build`.",
        status=503,
        content_type="text/plain",
    )
