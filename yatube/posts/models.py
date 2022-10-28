from core.models import ModelWithDateAndText
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()

CHARS_OF_POST_TEXT = 15
CHARS_OF_COMMENT_TEXT = 15


class Group(models.Model):
    title = models.CharField("Group title", max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(ModelWithDateAndText):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author"
    )

    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Group",
        help_text="Choose group",
    )

    image = models.ImageField(
        "Image",
        upload_to="posts/",
        blank=True
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.text[:CHARS_OF_POST_TEXT]


class Comment(ModelWithDateAndText):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Post",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Author",
    )

    def __str__(self):
        return self.text[:CHARS_OF_COMMENT_TEXT]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Author",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "author"],
                name="follow_must_be_unique",
            )
        ]
