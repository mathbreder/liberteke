from django import forms

from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'summary',
            'isbn',
            'genre',
            'year',
            'score',
        ]

        labels = {
          'title': 'Title',
          'author': 'Author',
          'summary': 'Summary',
          'isbn': 'ISBN',
          'genre': 'Genre',
          'year': 'Year',
          'score': 'Score',
        }

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control'}),
          'author': forms.Select(attrs={'class': 'form-control'}),
          'summary': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 7em'}),
          'isbn': forms.TextInput(attrs={'class': 'form-control'}),
          'genre': forms.Select(attrs={'class': 'form-control'}),
          'year': forms.NumberInput(attrs={'class': 'form-control'}),
          'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }
