from django.db import models


class ModelWithDateAndText(models.Model):
    text = models.TextField(
        "Text",
        help_text="Type some text",
    )
    created = models.DateTimeField(
        "Publication Date",
        auto_now_add=True,
    )

    class Meta:
        abstract = True
