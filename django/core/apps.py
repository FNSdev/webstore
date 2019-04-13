from django.apps import AppConfig
from core.models import Category
from core.forms import FormGenerator, GENERATED_FORMS


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        categories = Category.objects.all()
        for cat in categories:
            form = FormGenerator.generate(cat.slug, cat.specifications)
            GENERATED_FORMS[cat.slug] = form
