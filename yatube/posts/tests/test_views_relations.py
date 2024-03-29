from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from ..models import Comment, Follow, Group, Post, User

FIRST_OBJECT = 0


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
        cls.group = Group.objects.create(
            id=fake.random_int(),
            slug=fake.slug(),
        )
        cls.group2 = Group.objects.create(
            id=fake.random_int(),
        )
        cls.post = Post.objects.create(
            id=fake.random_int(),
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_with_group_belongs_only_to_its_group(self):
        """Test if post belongs only own group."""
        response = self.guest_client.get(reverse("posts:group_list",
                                         kwargs={"slug": self.group.slug}))
        self.assertNotEqual(response.context.get("group").id,
                            self.group2.id)

    def test_post_detail_has_related_comment(self):
        """Test if post_detail has related commentary."""
        response = self.guest_client.get(reverse("posts:post_detail",
                                         kwargs={"post_id": self.post.id}))
        comment = response.context.get("comments")[FIRST_OBJECT]
        self.assertEqual(comment, self.comment)

    def test_authorized_user_can_subscribe_to_author(self):
        """Test if follow (subscription) to author is possible."""
        self.authorized_client.get(
            reverse("posts:profile_follow",
                    kwargs={"username": self.another_user.username})
        )
        follow_object = Follow.objects.filter(
            user=self.user,
            author=self.another_user,
        ).count()
        self.assertTrue(follow_object != 0)

    def test_authorized_user_can_unsubscribe_to_author(self):
        """Test if unfollow (unsubscription) to author is possible."""
        self.authorized_client.get(
            reverse("posts:profile_unfollow",
                    kwargs={"username": self.another_user.username})
        )
        follow_object = Follow.objects.filter(
            user=self.user,
            author=self.another_user,
        ).count()
        self.assertTrue(follow_object == 0)
