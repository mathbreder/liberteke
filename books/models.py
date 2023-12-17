from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from author.models import Author
from genre.models import Genre

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text=mark_safe('13 Character <a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN number</a>'))
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL, help_text='Select a genre for this book')
    year = models.PositiveIntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        if self.year:
            return f"{self.title} ({self.year})"
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
