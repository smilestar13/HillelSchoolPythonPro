from django.db import models

class Config(models.Model):
    contact_form_email = models.EmailField(default='oleksienko.boris@gmail.com')

    def save(self, *args, **kwargs):
        if not self.pk and Config.objects.exists():
            raise ValueError('Можно создать только один экземпляр Config')
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Config'
