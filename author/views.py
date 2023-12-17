from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from author.forms import AuthorForm
from author.models import Author

# Create your views here.

class AuthorBaseView(View):
    model = Author
    success_url = reverse_lazy('authors:all')

class AuthorListView(AuthorBaseView, ListView):
    template_name = 'authors/list.html'
    context_object_name = 'author_list'
    paginate_by = 5

    def get(self, request):
        author_list = self.model.objects.all()
        paginator = Paginator(author_list, self.paginate_by)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})

class AuthorDetailView(AuthorBaseView, DetailView):
    template_name = 'authors/detail.html'
    context_object_name = 'author'

    def get(self, request, pk):
        author = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'author': author})

class AuthorCreateView(AuthorBaseView, CreateView):
    template_name = 'authors/form.html'
    form_class = AuthorForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        new_obj = self.model()
        form = self.form_class(new_obj, request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form}, status=400)

class AuthorUpdateView(AuthorBaseView, UpdateView):
    template_name = 'authors/form.html'
    form_class = AuthorForm

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        form = self.form_class(self.prepare(obj))
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        form = self.form_class(obj, request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def prepare(self, obj):
        obj.date_of_birth = obj.date_of_birth.strftime('%Y-%m-%d')
        obj.date_of_death = obj.date_of_death.strftime('%Y-%m-%d')
        return obj

class AuthorDeleteView(AuthorBaseView, DeleteView):
    template_name = 'authors/confirm_delete.html'

    def get(self, request, pk):
        author = self.model.objects.get(id=pk)
        return render(request, self.template_name, {'author': author})

    def post(self, request, pk):
        author = self.model.objects.get(id=pk)
        author.delete()
        return redirect(self.success_url)

