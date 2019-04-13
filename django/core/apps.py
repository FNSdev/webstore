from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from core.models import Category
        from core.forms import FormGenerator, GENERATED_FORMS
        categories = Category.objects.all()
        for cat in categories:
            form = FormGenerator.generate(cat.slug, cat.specifications)
            GENERATED_FORMS[cat.slug] = form
