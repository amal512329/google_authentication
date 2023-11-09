from django import forms

class TokenExchangeForm(forms.Form):
    client_id = forms.CharField(label='Client ID')
    client_secret = forms.CharField(label='Client Secret')
    authorization_code = forms.CharField(label='Authorization Code')