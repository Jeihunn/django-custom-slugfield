from django.contrib import admin

from . import models


# Register your models here.


@admin.register(models.TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "updated_at", "created_at")
    readonly_fields = ("slug",)
