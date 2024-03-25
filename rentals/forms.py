from django import forms
from .choices import FORMAT_CHOICE

class SearchBookForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'search by book id ...'}))
    
class SelectExportOptionForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICE, widget=forms.RadioSelect())
    
