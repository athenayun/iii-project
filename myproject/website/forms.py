from django import forms

class PostForm(forms.Form):
    classification = forms.CharField(max_length=100)
    price = forms.CharField(max_length=200)
    effect = forms.CharField(max_length=100)

