from django import forms
from django.contrib.auth.hashers import make_password
from tg_bot.models import TgUser


class TgUserAdminForm(forms.ModelForm):
    class Meta:
        model = TgUser
        fields = "__all__"

    def save(self, commit: bool = False) -> TgUser:
        instance: TgUser = super().save(commit)
        instance.password = make_password(instance.password)
        instance.save()
        return instance
