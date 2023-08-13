from django.db import models
from django.utils.translation import gettext_lazy as _


class IndustrialUnit(models.Model):
    name = models.CharField(
        max_length=255, verbose_name=_("Название установки"), unique=True
    )

    class Meta:
        verbose_name = _("Установка")
        verbose_name_plural = _("Установки")
        ordering = ["id"]

    def __str__(self):
        return self.name


class MachineNode(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название узла"))
    industial_unit = models.ForeignKey(
        "machinery.IndustrialUnit",
        verbose_name=_("Установка"),
        on_delete=models.CASCADE,
        related_name="industial_units",
    )

    class Meta:
        verbose_name = _("Узел установки")
        verbose_name_plural = _("Узлы установки")
        constraints = [
            models.UniqueConstraint(
                name="unical_mach_node", fields=["name", "industial_unit"]
            )
        ]
        ordering = ["id"]

    def __str__(self):
        return self.name


class Element(models.Model):
    class Priority(models.IntegerChoices):
        GREEN = 1, _("Низкий")
        YELLOW = 2, _("Средний")
        RED = 3, _("Высокий")

    name = models.CharField(max_length=50, verbose_name=_("Имя элемента"))
    description = models.TextField(
        verbose_name=_("Описание элемента"), blank=True
    )
    hardware = models.ForeignKey(
        "machinery.MachineNode",
        verbose_name=_("оборудование"),
        on_delete=models.CASCADE,
        related_name="machine_nodes",
    )
    priority = models.SmallIntegerField(
        default=Priority.GREEN,
        verbose_name=_("Приоритет"),
        choices=Priority.choices,
    )
    count_fact = models.IntegerField(
        verbose_name=_("Количество факт"), default=1
    )
    count_need = models.IntegerField(
        verbose_name=_("Количество необходимо"), default=1
    )
    commute_hardware = models.CharField(
        _("Коммутационное оборудование"), max_length=50
    )

    class Meta:
        verbose_name = _("Элемент")
        verbose_name_plural = _("Элементы")
        constraints = [
            models.UniqueConstraint(
                name="unical_element", fields=["name", "hardware"]
            )
        ]
        ordering = ["id"]

    def __str__(self):
        return self.name


class VixDate(models.Model):
    data_fix = models.DateTimeField(_("Дата ремонта"), auto_now_add=True)
    description = models.TextField(_("Описание ремонта"))
    element = models.ForeignKey(
        "machinery.Element",
        verbose_name=_("Элемент"),
        on_delete=models.CASCADE,
        related_name="elements",
    )

    class Meta:
        verbose_name = _("Дата ремонта")
        verbose_name_plural = _("Даты ремонта")

    def __str__(self):
        return self.element.__str__()
