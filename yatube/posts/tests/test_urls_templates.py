from django.test import Client, TestCase
from faker import Faker

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name()
        )
        cls.group = Group.objects.create(
            slug=fake.slug(),
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_urls_use_correct_template(self):
        """Test if URLs using correct HTML templates."""
        urls_for_templates = {
            "/": "posts/index.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/profile/{self.user.username}/": "posts/profile.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
            "/create/": "posts/create_post.html",
            f"/posts/{self.post.id}/edit/": "posts/create_post.html",
        }
        for address, template in urls_for_templates.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
