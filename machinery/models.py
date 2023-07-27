from django.db import models
from django.urls import reverse


class Industrial_unit(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название установки")

    class Meta:
        verbose_name = "Установка"
        verbose_name_plural = "Установки"

    def __str__(self):
        return self.name


class Machine_node(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название узла")
    industial_unit = models.ForeignKey(
        "machinery.Industrial_unit",
        verbose_name="Установка",
        on_delete=models.CASCADE,
        related_name="industial_units",
    )

    class Meta:
        verbose_name = "Узел установки"
        verbose_name_plural = "Узлы установки"

    def __str__(self):
        return self.name
