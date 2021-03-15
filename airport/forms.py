from django import forms

class AirportForm(forms.Form):
    name = forms.CharField(label="Airport Name", max_length=256)
    code = forms.CharField(label="Airport Code", max_length=20)
    location = forms.CharField(label="Location", max_length=200)