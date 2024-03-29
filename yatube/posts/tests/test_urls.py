from http import HTTPStatus

from django.test import Client, TestCase
from faker import Faker

from ..models import Group, Post, User

STATUS_200 = HTTPStatus.OK
STATUS_404 = HTTPStatus.NOT_FOUND


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name(),
        )
        cls.group = Group.objects.create(
            slug=fake.slug(),
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_posts_urls_exist_at_desired_location(self):
        """Test if URLs accessible for anonymous."""
        url_statuses = {
            "/": STATUS_200,
            f"/group/{self.group.slug}/": STATUS_200,
            f"/profile/{self.user.username}/": STATUS_200,
            f"/posts/{self.post.id}/": STATUS_200,
        }
        for url, status in url_statuses.items():
            with self.subTest(status=status):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_posts_create_and_edit_urls_exist_at_desired_location(self):
        """Test if URLs accessible for authorized users."""
        url_status = {
            "/create/": STATUS_200,
            f"/posts/{self.post.id}/edit/": STATUS_200,
        }
        for url, status in url_status.items():
            with self.subTest(status=status):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_nonexistent_url_returns_404(self):
        """Test request to nonexistent URL."""
        fake_url = Faker()
        response = self.guest_client.get(f"/{fake_url.url()}/")
        self.assertEqual(response.status_code, STATUS_404)

    def test_post_create_edit_and_comment_redirects_anonymous(self):
        """Test if anonymous redirects from create/, edit/ and comment/."""
        response = self.guest_client.get("/create/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")
        response = self.guest_client.get(
            f"/posts/{self.post.id}/edit/",
            follow=True
        )
        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.id}/edit/"
        )
        response = self.guest_client.get(
            f"/posts/{self.post.id}/comment/",
            follow=True
        )
        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.id}/comment/"
        )
