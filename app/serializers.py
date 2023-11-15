from django import forms


class CreatePaymentRequest(forms.Form):
    account = forms.IntegerField(required=True)
    amount = forms.IntegerField(required=True)
