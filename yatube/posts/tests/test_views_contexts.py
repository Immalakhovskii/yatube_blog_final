import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from faker import Faker

from ..models import Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

FIRST_OBJECT = 0


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name(),
        )
        cls.another_user = User.objects.create_user(
            username=fake.name(),
        )
        cls.additional_user = User.objects.create_user(
            username=fake.name(),
        )
        cls.group = Group.objects.create(
            title=fake.word(),
            slug=fake.slug(),
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name="small.gif",
            content=small_gif,
            content_type="image/gif"
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
            group=cls.group,
            text=fake.text(),
            image=uploaded,
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.another_user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.another_authorized_client = Client()
        self.another_authorized_client.force_login(self.additional_user)

    def test_index_group_and_profile_show_correct_context(self):
        """
        Test if index, group_posts, profile templates
        have correct context.
        """
        responses = [
            (self.guest_client.get(reverse("posts:index"))),
            (self.guest_client.get(reverse("posts:group_list",
             kwargs={"slug": self.group.slug}))),
            (self.guest_client.get(reverse("posts:profile",
             kwargs={"username": self.user.username}))),
        ]
        for response in responses:
            first_post = response.context["page_obj"][FIRST_OBJECT]
            first_post_fields = {
                first_post.author.username: self.user.username,
                first_post.text: self.post.text,
                first_post.group.title: self.group.title,
                first_post.image: self.post.image,
            }
            for instance, expected_instance in first_post_fields.items():
                with self.subTest(instance=instance):
                    self.assertEqual(instance, expected_instance)

    def test_post_detail_shows_correct_context(self):
        """Test if post_detail template has correct context."""
        response = (self.guest_client.get(reverse("posts:post_detail",
                    kwargs={"post_id": self.post.id})))
        post = response.context["post"]
        post_fields = {
            post.author.username: self.user.username,
            post.text: self.post.text,
            post.group.title: self.group.title,
            post.image: self.post.image,
        }
        for instance, expected_instance in post_fields.items():
            with self.subTest(instance=instance):
                self.assertEqual(instance, expected_instance)

    def test_post_create_and_post_edit_show_correct_context(self):
        """Test if post_create, post_edit templates have correct context."""
        responses = [
            (self.authorized_client.get(reverse("posts:post_create"))),
            (self.authorized_client.get(reverse("posts:post_edit",
             kwargs={"post_id": self.post.id}))),
        ]
        for response in responses:
            form_fields = {
                "text": forms.fields.CharField,
                "group": forms.models.ModelChoiceField,
            }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get("form").fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_follow_index_correctly_shows_new_post(self):
        """Test if new post is in follower feed."""
        Post.objects.create(author=self.another_user)
        response = self.authorized_client.get(reverse("posts:follow_index"))
        posts_count = response.context["posts"].count()
        self.assertTrue(posts_count != 0)
        response = self.another_authorized_client.get(reverse(
            "posts:follow_index"))
        posts_count = response.context["posts"].count()
        self.assertTrue(posts_count == 0)
