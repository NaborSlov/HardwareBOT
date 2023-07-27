from django.db import models
from django.utils.translation import gettext_lazy as _


class Industrial_unit(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название установки"))

    class Meta:
        verbose_name = _("Установка")
        verbose_name_plural = _("Установки")

    def __str__(self):
        return self.name


class Machine_node(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название узла"))
    industial_unit = models.ForeignKey(
        "machinery.Industrial_unit",
        verbose_name=_("Установка"),
        on_delete=models.CASCADE,
        related_name="industial_units",
    )

    class Meta:
        verbose_name = _("Узел установки")
        verbose_name_plural = _("Узлы установки")

    def __str__(self):
        return self.name


class Hardware(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название оборудования"))
    machine_node = models.ForeignKey(
        "machinery.Machine_node",
        verbose_name=_("Узел установки"),
        on_delete=models.CASCADE,
        related_name="machine_nodes",
    )

    class Meta:
        verbose_name = _("Оборудование")
        verbose_name_plural = _("Оборудование")

    def __str__(self):
        return self.name


class Element(models.Model):
    class Priority(models.IntegerChoices):
        GREEN = 1, "Низкий"
        YELLOW = 2, "Средний"
        RED = 3, "Высокий"

    name = models.CharField(max_length=50, verbose_name=_("Имя элемента"))
    description = models.TextField(verbose_name=_("Описание элемента"))
    hardware = models.ForeignKey(
        "machinery.Hardware",
        verbose_name=_("оборудование"),
        on_delete=models.CASCADE,
        related_name="hardwares",
    )
    priority = models.SmallIntegerField(
        default=Priority.GREEN,
        verbose_name=_("Приоритет"),
        choices=Priority.choices,
    )
    count_fact = models.IntegerField(verbose_name=_("Количество факт"))
    count_need = models.IntegerField(verbose_name=_("Количество необходимо"))

    class Meta:
        verbose_name = _("Элемент")
        verbose_name_plural = _("Элементы")

    def __str__(self):
        return self.name
