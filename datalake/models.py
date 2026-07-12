from django.contrib.auth.models import User
from django.db import models


class Dataset(models.Model):

    # Dataset owner
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="datasets"
    )

    # Uploaded file
    file = models.FileField(upload_to="datasets/")

    # Upload date & time
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Validation status
    status = models.CharField(
        max_length=30,
        default="Pending"
    )

    # Dataset information
    total_columns = models.IntegerField(default=0)
    valid_columns = models.IntegerField(default=0)
    invalid_columns = models.IntegerField(default=0)

    # File information
    file_type = models.CharField(
        max_length=20,
        default="Unknown"
    )

    file_hash = models.CharField(
        max_length=64,
        blank=True
    )

    file_size = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"