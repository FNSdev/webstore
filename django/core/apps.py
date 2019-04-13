from django.apps import AppConfig
import sys

class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        not_a_run_server = {'collectstatic', 'makemigrations', 'migrate'}
        for command in not_a_run_server:
            if command in sys.argv:
                return True
        
        from core.models import Category
        from core.forms import FormGenerator, GENERATED_FORMS
        categories = Category.objects.all()
        for cat in categories:
            form = FormGenerator.generate(cat.slug, cat.specifications)
            GENERATED_FORMS[cat.slug] = form
