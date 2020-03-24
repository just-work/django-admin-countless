from django.contrib import admin

from countless_admin import CountlessAdminMixin
from test_project.test_app.models import MyModel


@admin.register(MyModel)
class MyModelAdmin(CountlessAdminMixin, admin.ModelAdmin):
    pass
