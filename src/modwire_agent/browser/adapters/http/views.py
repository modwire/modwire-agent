from django.views.generic import TemplateView


class BrowserIndexView(TemplateView):
    template_name = "browser/index.html"
