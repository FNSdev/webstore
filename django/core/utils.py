from django import forms


# TODO move this into forms.py
class FormGenerator():
    @staticmethod
    def generate(slug, specifications):
        from core.models import Category
        params = {}
    
        for key, value in specifications.items():
            if value == 'str':
                params[key] = forms.CharField(max_length=40, required=False)
            elif value == 'int':
                params[key] = forms.IntegerField(required=False)

        name = slug + '_form'
        form = type(name, (forms.Form,), params)
        return form