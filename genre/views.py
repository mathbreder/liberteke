from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import GenreForm
from .models import Genre

# Create your views here.

class GenreBaseView(View):
    model = Genre
    success_url = reverse_lazy('genres:all')

class GenreListView(GenreBaseView, ListView):
    template_name = 'genres/list.html'
    context_object_name = 'genre_list'
    paginate_by = 5

    def get(self, request):
        genre_list = self.model.objects.all()
        paginator = Paginator(genre_list, self.paginate_by)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})

class GenreDetailView(GenreBaseView, DetailView):
    template_name = 'genres/detail.html'
    context_object_name = 'genre'

    def get(self, request, pk):
        genre = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'genre': genre})

class GenreCreateView(GenreBaseView, CreateView):
    template_name = 'genres/form.html'
    form_class = GenreForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'action': 'create'})

    def post(self, request):
        new_obj = self.model()
        form = self.form_class(new_obj, request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form}, status=400)

class GenreUpdateView(GenreBaseView, UpdateView):
    template_name = 'genres/form.html'
    form_class = GenreForm

    def get(self, request, pk):
        form = self.form_class(instance=self.model.objects.get(id=pk))
        return render(request, self.template_name, {'form': form, 'action': 'update'})

    def post(self, request, pk):
        form = self.form_class(instance=self.model.objects.get(id=pk), data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form}, status=400)

class GenreDeleteView(GenreBaseView, DeleteView):
    template_name = 'genres/confirm_delete.html'
    context_object_name = 'genre'

    def get(self, request, pk):
        genre = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'genre': genre})

    def post(self, request, pk):
        genre = self.model.objects.get(id=pk)
        genre.delete()
        return redirect(self.success_url)
