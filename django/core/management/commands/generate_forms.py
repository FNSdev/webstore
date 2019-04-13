from django.core.management.base import BaseCommand
from core.models import Category
from core.forms import GENERATED_FORMS, FormGenerator


class Command(BaseCommand):
    help = 'Generates filtering forms for product categories. Must be executed whenever server restarts'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        for cat in categories:
            form = FormGenerator.generate(cat.slug, cat.specifications)
            GENERATED_FORMS[cat.slug] = form