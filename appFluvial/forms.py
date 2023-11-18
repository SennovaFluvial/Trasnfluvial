# forms.py

from django import forms
from .models import Departamento

class SelectDepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre']
