from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Group, Post, User
from ..views import POSTS_PER_PAGE

POSTS_FOR_TESTS = 13


class PaginatorPostViewsTest(TestCase):
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
        Post.objects.bulk_create(
            [Post(author=cls.user, group=cls.group)]
            * POSTS_FOR_TESTS
        )

    def setUp(self):
        self.guest_client = Client()

    def test_first_pages_have_expected_number_of_records(self):
        """
        Test if first pages of index, group_list, profile
        have correct number of an objects.
        """
        page_with_objects = {
            reverse("posts:index"): POSTS_PER_PAGE,
            reverse("posts:group_list", kwargs={"slug": self.group.slug}):
            POSTS_PER_PAGE,
            reverse("posts:profile", kwargs={"username": self.user.username}):
            POSTS_PER_PAGE,
        }
        for page, objects in page_with_objects.items():
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(len(response.context["page_obj"]), objects)

    def test_second_pages_have_expected_number_of_records(self):
        """
        Test if second pages of index, group_list, profile
        have correct number of an objects.
        """
        posts_count = POSTS_FOR_TESTS - POSTS_PER_PAGE
        page_with_objects = {
            reverse("posts:index"): posts_count,
            reverse("posts:group_list", kwargs={"slug": self.group.slug}):
            posts_count,
            reverse("posts:profile", kwargs={"username": self.user.username}):
            posts_count,
        }
        for page, objects in page_with_objects.items():
            with self.subTest(page=page):
                response = self.guest_client.get(page + "?page=2")
                self.assertEqual(len(response.context["page_obj"]), objects)
