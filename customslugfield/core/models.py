from django.db import models
from django.utils.translation import gettext_lazy as _

from services.fields import CustomSlugField


# Create your models here.


class TestModel(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    slug = CustomSlugField(
        verbose_name=_("Slug"),
        source_field="name",
        symbol_mapping="default",
        unique=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    def __str__(self):
        return self.name if self.name else "Unnamed TestModel"

    class Meta:
        verbose_name = _("Test Model")
        verbose_name_plural = _("Test Models")
