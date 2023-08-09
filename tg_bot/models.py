from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password as check_password_django


class TgUser(models.Model):
    login = models.CharField(
        _("login name"), max_length=50, unique=True, primary_key=True
    )
    password = models.CharField(_("password"), max_length=255)
    tg_login = models.BigIntegerField(_("Телеграм логин"), default=0)

    def check_password(self, value: str) -> bool:
        return check_password_django(value, self.password)

    class Meta:
        verbose_name = _("Tg_user")
        verbose_name_plural = _("Tg_users")

    def __str__(self):
        return self.login

    @staticmethod
    def get_model_name():
        return "TgUser"
