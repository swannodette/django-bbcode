from django.db import models
from django import forms
validate = __import__('bbcode',level=0).validate

class BBCodeTextField(models.TextField):
    """
    BBCodeField for a database which basically is a TextField but uses the 
    BBCodeFormField form field to validate bbcode input (eg. in admin)
    """
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': BBCodeFormField}
        defaults.update(kwargs)
        return models.TextField.formfield(self, **defaults)

class BBCodeCharField(models.CharField):
    """
    BBCodeField for a database which basically is a CharField but uses the 
    BBCodeFormField form field to validate bbcode input (eg. in admin)
    """
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': BBCodeFormField}
        defaults.update(kwargs)
        return models.CharField.formfield(self, **defaults)
    
    
class BBCodeFormField(forms.CharField):
    """
    A form field validating BBCode Input (it does NOT parse it)
    """
    def clean(self, content):
        preclean = forms.CharField.clean(self, content)
        errors = validate(preclean)
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        return content