from django import forms

from business.models import BusinessArea


class UserBusinessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(UserBusinessForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BusinessArea
        fields = ('business',)
