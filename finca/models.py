from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # media/finca_<user-id>/<filename>
    return f"finca_{instance.user.id}/{filename}"


class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE,
                                        related_name="finca_profile")
    display_name = models.CharField(max_length=100, blank=True)
    bio          = models.TextField(blank=True)
    avatar       = models.ImageField(upload_to=user_directory_path,
                                     blank=True, null=True)
    cover        = models.ImageField(upload_to=user_directory_path,
                                     blank=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Finca de {self.user.username}"


class Post(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="finca_posts")
    text        = models.TextField(blank=True)
    image       = models.ImageField(upload_to=user_directory_path,
                                    blank=True, null=True)
    video       = models.FileField(upload_to=user_directory_path,
                                    blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        preview = self.text[:30] if self.text else "📎 media"
        return f"{self.author.username}: {preview}"
