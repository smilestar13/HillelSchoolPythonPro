from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from project.mixins.models import PKMixin

User = get_user_model()


class Feedback(PKMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MaxValueValidator(5)]
    )
