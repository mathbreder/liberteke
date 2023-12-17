from django import forms

from .models import Genre


class GenreForm(forms.ModelForm):
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        if instance:
            self.fields["name"].initial = instance.name

    class Meta:
        model = Genre
        fields = [
            "name",
        ]

        labels = {
            "name": "Name",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
