from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from books.models import Book
from author.models import Author


class BookResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Title')
    author_name = Field(column_name='Author Name')
    summary = Field(attribute='summary', column_name='Summary')
    isbn = Field(attribute='isbn', column_name='ISBN')
    genre__name = Field(attribute='genre__name', column_name='Genre')
    year = Field(attribute='year', column_name='Year')
    score = Field(attribute='score', column_name='Score')

    class Meta:
        model = Book
        export_order = ['title', 'author_name', 'year', 'isbn', 'genre__name', 'summary', 'score']

    def dehydrate_author_name(self, book):
        first_name = book.author.first_name
        last_name = book.author.last_name
        return f'{first_name} {last_name}'
