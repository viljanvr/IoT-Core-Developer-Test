from django import forms

class RadiusForm(forms.Form):
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()
    radius = forms.IntegerField()