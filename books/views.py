from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import BookTitle, Book
from django.views.generic import (
    ListView, 
    FormView, 
    DetailView, 
    DeleteView,
)
from .forms import BookTitleForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import string
from django.contrib.auth.mixins import LoginRequiredMixin

class BookTitleListView(LoginRequiredMixin, FormView, ListView):
    # model = BookTitle
    # queryset = BookTitle.objects.all()   #.order_by('-created')
    template_name = 'books/main.html'
    context_object_name = 'qs'
    form_class = BookTitleForm
    # success_url = reverse_lazy('books:main')
    # ordering = ('-created',)
    # model_list.html -> booktitle_list.html
    i_instance = None
    
    def get_success_url(self):
        return self.request.path
        
    def get_queryset(self) :
        parameter = self.kwargs.get('letter') if self.kwargs.get('letter') else 'a'
        return BookTitle.objects.filter(title__startswith=parameter)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['hi'] = 'hello world'
        # context['hi2'] = 'hello world 2'
        letters = list(string.ascii_uppercase)
        context['letters'] = letters
        context['selected_letter'] = self.kwargs.get('letter') if self.kwargs.get('letter') else 'a'
        # context = {
        #     'hi': 'hello world',            #this is another way to do above.
        #     'form': self.get_form_class(),
        #     'qs': self.get_queryset()
        # }
        return context
    
    def form_valid(self, form):
        self.i_instance = form.save()
        messages.add_message(self.request, messages.INFO, f"Book title: {self.i_instance.title} has been created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)  #form.errors can be replaced with typed text
        return super().form_invalid(form)

# def book_title_list_view(request):
#     qs = BookTitle.objects.all()
#     return render(request, 'books/main.html', {'qs':qs})

#OPTION 1 - BOOK LIST VIEW +  overriding get_queryset method

# class BookListView(ListView):
#     template_name = 'books/detail.html'
#     paginate_by = 3
    
#     def get_queryset(self):
#         title_slug = self.kwargs.get('slug')
#         return Book.objects.filter(title__slug=title_slug) #book fc to booktitle, title__slug references book

#OPTION 2 - BOOK TITLE DETAIL VIEW + model method
class BookTitleDetailView(LoginRequiredMixin, DetailView):
    model = BookTitle
    template_name = 'books/detail.html' 
    
    def get_context_data(self, **kwargs):  #this is used to pass in the previous page
        context = super().get_context_data(**kwargs)
        context['previous_page'] = reverse('books:main')
        return context


# def book_title_detail_view(request, **kwargs):
#     slug=kwargs.get('slug')
#     obj = BookTitle.objects.get(slug=slug)
#     return render(request, 'books/detail.html', {'obj': obj})

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/detail_book.html'
    
    def get_object(self):
        id = self.kwargs.get('book_id')
        # obj = Book.objects.get(book_id=id)
        obj = get_object_or_404(Book, id=id)
        return obj

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/confirm_delete.html'
    
    def get_object(self):
        id = self.kwargs.get('book_id')
        obj = get_object_or_404(Book, id=id)
        return obj   
    
    def get_success_url(self):
        messages.add_message(self.request,messages.INFO, f"The book with isbn {self.get_object().isbn} has been deleted.")
        letter = self.kwargs.get('letter')
        slug = self.kwargs.get('slug')
        return reverse('books:detail',kwargs={'letter':letter, 'slug':slug})
    