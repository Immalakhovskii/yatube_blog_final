from django.test import TestCase
from faker import Faker

from ..models import Group, Post, User

CHARS_OF_POST_TEXT = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name()
        )
        cls.group = Group.objects.create(
            title=fake.word(),
        )
        cls.post = Post.objects.create(
            author=cls.user,
        )

    def test_models_have_correct_objects_names(self):
        """Test correct functionality of __str__ in models."""
        group = PostModelTest.group
        post = PostModelTest.post
        objects_names = (
            (str(group), group.title),
            (str(post), post.text[:CHARS_OF_POST_TEXT]),
        )
        for title, expected_title in objects_names:
            with self.subTest(title=title):
                self.assertEqual(title, expected_title)

    def test_post_model_verbose_names(self):
        """Test if verbose_names in Post model fields are correct."""
        post = PostModelTest.post
        field_verboses = {
            "text": "Text",
            "created": "Publication Date",
            "author": "Author",
            "group": "Group",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_model_help_texts(self):
        """Test if help_texts in Post model fields are correct."""
        post = PostModelTest.post
        field_help_texts = {
            "text": "Type some text",
            "group": "Choose group",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
