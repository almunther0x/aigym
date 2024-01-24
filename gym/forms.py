from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = forms.widgets.FileInput(
            attrs={
                'id': 'image',
                'class': 'd-none',
                'accept': "image/jpeg, image/png, image/jpg"
                }
            )
        self.fields['image'].required = False
        self.fields['image'].label = False
        self.fields['user'].required = False
        self.fields['user'].widget = forms.widgets.HiddenInput(
            attrs={
                'class': 'd-none',
                },
            )
    class Meta:
        model = Profile
        fields = '__all__'
