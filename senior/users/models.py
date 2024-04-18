import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

def image_directory_path(instance, filename):

    extension = filename.split('.')[-1]
    return f"users/{instance.id}.{extension}"

class User(AbstractUser):
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.username}"
    
    def delete_image(self):
        if self.image:
            image_path = self.image.path

            if os.path.exists(image_path):
                os.remove(image_path)

            self.image = None
            self.save(update_fields=["image"])