from django import forms

from .models import Author


class AuthorForm(forms.ModelForm):
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        if instance:
            self.fields["first_name"].initial = instance.first_name
            self.fields["last_name"].initial = instance.last_name
            self.fields["date_of_birth"].initial = instance.date_of_birth
            self.fields["date_of_death"].initial = instance.date_of_death

    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "date_of_death",
        ]

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "date_of_birth": "Date of Birth",
            "date_of_death": "Date of Death",
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                format="%d/%m/%Y",
                attrs={"class": "form-control", "required": False, "type": "date"},
            ),
            "date_of_death": forms.DateInput(
                format="%d/%m/%Y",
                attrs={"class": "form-control", "required": False, "type": "date"},
            ),
        }
