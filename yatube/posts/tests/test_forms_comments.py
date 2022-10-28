from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..forms import CommentForm
from ..models import Comment, Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake = Faker()
        cls.user = User.objects.create_user(
            username=fake.name(),
        )
        cls.group = Group.objects.create(
            id=fake.random_int(),
            slug=fake.slug(),
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text=fake.text(),
            post=cls.post,
            author=cls.user,
        )
        cls.form = CommentForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_commenting_is_possible(self):
        """Test if authorized user can create comment."""
        comments_count = Comment.objects.count()
        form_data = {"text": self.comment.text}
        response = self.authorized_client.post(
            reverse("posts:add_comment",
                    kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(
                "posts:post_detail",
                kwargs={"post_id": self.post.id})
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text=form_data["text"],
            ).exists()
        )

    def test_anonymous_cant_comment(self):
        """Test if unauthorized user can't create comment."""
        comments_count = Comment.objects.count()
        new_text = Faker()
        form_data = {"text": new_text.text()}
        response = self.guest_client.post(
            reverse("posts:add_comment",
                    kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            f"/auth/login/?next=/posts/{self.post.id}/comment/"
        )
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertFalse(
            Comment.objects.filter(
                text=form_data["text"],
            ).exists()
        )
