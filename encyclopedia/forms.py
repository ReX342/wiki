from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="name", max_lenght=200)
    check = forms.BooleanField(required=False)