from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE, AFTER_UPDATE

from project.mixins.models import PKMixin
from project.model_choices import FeedbackCacheKeys

User = get_user_model()


class Feedback(LifecycleModelMixin, PKMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(FeedbackCacheKeys.FEEDBACKS)