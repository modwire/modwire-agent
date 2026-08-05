from django.test import TestCase, override_settings


class BrowserTests(TestCase):
    def test_serves_the_siren_browser_from_the_index(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        page = response.content.decode()
        self.assertRegex(page, r'href="/static/browser/browser(?:\.[0-9a-f]{12})?\.css"')
        self.assertRegex(page, r'src="/static/browser/browser(?:\.[0-9a-f]{12})?\.js"')
        self.assertIn('data-siren-root="/siren/"', page)

    @override_settings(MODWIRE_SIREN_ROOT="/example-siren/")
    def test_exposes_the_configured_siren_root(self) -> None:
        response = self.client.get("/")

        self.assertContains(response, 'data-siren-root="/example-siren/"')
