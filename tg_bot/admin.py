from django.contrib import admin
from tg_bot.forms import TgUserAdminForm

from tg_bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("login",)
    form = TgUserAdminForm
