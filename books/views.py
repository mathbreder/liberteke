from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import BookForm
from .models import Book

# Create your views here.


class BookBaseView(View):
    model = Book
    success_url = reverse_lazy('books:all')


class BookListView(BookBaseView, ListView):
    template_name = 'books/list.html'
    context_object_name = 'book_list'
    paginate_by = 5

    def get(self, request):
        search_string = request.GET.get('search')
        if search_string:
            book_list = self.model.objects.filter(
                Q(title__icontains=search_string) |
                Q(author__first_name__icontains=search_string) |
                Q(author__last_name__icontains=search_string) |
                Q(summary__icontains=search_string) |
                Q(isbn__icontains=search_string) |
                Q(genre__name__icontains=search_string) |
                Q(year__icontains=search_string)
            )
        else:
            book_list = self.model.objects.all()
        paginator = Paginator(book_list, self.paginate_by)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj, 'search_string': search_string})

class BookDetailView(BookBaseView, DetailView):
    template_name = 'books/detail.html'
    context_object_name = 'book'

    def get(self, request, pk):
        book = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'book': book})

class BookCreateView(BookBaseView, CreateView):
    template_name = 'books/form.html'
    form_class = BookForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form}, status=400)

class BookUpdateView(BookBaseView, UpdateView):
    template_name = 'books/form.html'
    form_class = BookForm

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        form = self.form_class(instance=obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.instance
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form}, status=400)

class BookDeleteView(BookBaseView, DeleteView):
    template_name = 'books/confirm_delete.html'

    def get(self, request, pk):
        book = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'book': book})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        return redirect(self.success_url)

class BookExportView(BookBaseView, ListView):
    model = Book
    template_name = 'books/export.html'

    def post(self, request):
        from .resources import BookResource
        search_string = request.POST.get('search')
        book_list = self.get_book_list(search_string)
        dataset = BookResource().export(book_list)
        ds = dataset.xlsx
        response = HttpResponse(ds, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
        return response

    def get_book_list(self, search_string):
        if search_string:
            return self.model.objects.filter(
                Q(title__icontains=search_string) |
                Q(author__first_name__icontains=search_string) |
                Q(author__last_name__icontains=search_string) |
                Q(summary__icontains=search_string) |
                Q(isbn__icontains=search_string) |
                Q(genre__name__icontains=search_string) |
                Q(year__icontains=search_string)
            )
        else:
            return self.model.objects.all()
