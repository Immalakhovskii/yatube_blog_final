from http import HTTPStatus

from django.test import Client, TestCase

STATUS_200 = HTTPStatus.OK


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls_exist_at_desired_location(self):
        """Проверка URL about."""
        url_status = {
            "/about/author/": STATUS_200,
            "/about/tech/": STATUS_200,
        }
        for url, status in url_status.items():
            with self.subTest(status=status):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)
