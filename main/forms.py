from django import forms

class JogadorSearchForm(forms.Form):
    query = forms.CharField(label='Pesquisar Jogador', max_length=100, required=False)