from django.apps import AppConfig
from django.forms import Form
import sys
import ast


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        not_a_run_server = {'collectstatic', 'makemigrations', 'migrate'}
        for command in not_a_run_server:
            if command in sys.argv:
                return True
        from core.models import Category
        from core.forms import MetaForm, GENERATED_FORMS
        categories = Category.objects.all()
        for cat in categories:
            specs = cat.specifications
            specs = specs.replace('=>', ':')
            specs = '{' + specs + '}'
            specs = ast.literal_eval(specs)
            form = MetaForm(cat.slug, (Form, ), specs)
            GENERATED_FORMS[cat.slug] = form
