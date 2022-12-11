from django.db import models

class Blogs(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200, null=False, blank=False)
    content = models.TextField(verbose_name="Content", null=False, blank=False)
    author = models.CharField(verbose_name="Author Username", max_length=200)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp of the moment the blog was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The timestamp of last time blog was updated."
    )
