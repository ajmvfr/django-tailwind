from django import forms
from .models import BookTitle
from django.core.exceptions import ValidationError

class BookTitleForm(forms.ModelForm):
    class Meta:
        model = BookTitle
        fields = ('publisher', 'author', 'title')
        
    def clean(self):
        title = self.cleaned_data.get('title')
        
        if len(title) < 5:
            error_msg = 'the title is too short'
            self.add_error('title', error_msg)
            # raise ValidationError(error_msg) #puts the error at the top of the form
        
        book_title_exists = BookTitle.objects.filter(title__iexact=title).exists() #returns true or false
        if book_title_exists:
            self.add_error('title', 'this book title already exists')
        
        return self.cleaned_data