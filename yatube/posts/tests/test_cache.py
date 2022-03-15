from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Post, User


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name(),
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
            text=fake.text(),
        )

    def setUp(self):
        self.guest_client = Client()

    def test_index_content_saved_in_cache(self):
        """Проверка сохранения постов index в кэше"""
        response = self.guest_client.get(reverse("posts:index"))
        index_post = response.content
        Post.objects.filter(id=self.post.id).delete()
        response = self.guest_client.get(reverse("posts:index"))
        index_post_2 = response.content
        self.assertEqual(index_post, index_post_2)
