from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.static import serve

from shared.api.root.controller import COLLECTIONS
from shared.api.siren import PROBLEM_TYPE, SIREN_TYPE
from tokens.models.api_key import ApiKey


def api_root(request):
    if ApiKey.authenticate(request.headers.get("apikey", "")) is None:
        return JsonResponse(
            {"type": "about:blank", "title": "Unauthorized", "status": 401, "detail": "Invalid API key"},
            status=401,
            content_type=PROBLEM_TYPE,
        )
    absolute = request.build_absolute_uri
    links = [{"rel": ["self"], "href": absolute("/api/")}]
    links.extend(
        {
            "rel": [name.replace("_", "-")],
            "href": absolute(f"/api/{name}"),
            "title": name.replace("_", " ").title(),
        }
        for name in COLLECTIONS
    )
    links.extend(
        [
            {
                "rel": ["service-desc"],
                "href": absolute("/api/openapi.json"),
                "type": "application/vnd.oai.openapi+json;version=3.1",
            },
            {"rel": ["browser"], "href": absolute("/browser/")},
        ]
    )
    return JsonResponse(
        {
            "class": ["api", "entry-point"],
            "properties": {"title": "Modwire API", "version": "1.0.0"},
            "links": links,
            "actions": [],
        },
        content_type=SIREN_TYPE,
    )


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
