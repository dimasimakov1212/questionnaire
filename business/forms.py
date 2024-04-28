from django import forms

from business.models import Business, BusinessArea


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BusinessForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Business
        fields = ('business_title', 'business_description')


class BusinessAreaForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BusinessArea
        fields = ('business_area_title', 'business_area_description')
