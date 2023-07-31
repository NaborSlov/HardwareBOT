from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password


class TgUser(models.Model):
    login = models.CharField(
        _("login name"), max_length=50, unique=True, primary_key=True
    )
    password = models.CharField(_("password"), max_length=255)

    def set_password(self, value: str) -> None:
        self.password = make_password(value)
        self.save()

    def check_password(self, value: str) -> None:
        return check_password(value, self.password)

    class Meta:
        verbose_name = _("Tg_user")
        verbose_name_plural = _("Tg_users")

    def __str__(self):
        return self.login
