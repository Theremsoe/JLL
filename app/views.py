# implement your views here
from json import loads
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Account, Payment
from app.serializers import CreatePaymentRequest


def account_create(request: HttpRequest) -> HttpResponse:
    account = Account()
    account.save()

    return JsonResponse(model_to_dict(account), status=201)

def account_read(request: HttpRequest, id: int) -> HttpResponse:
    record = get_object_or_404(Account, id=id)

    return JsonResponse(model_to_dict(record))

def payment_create(request: HttpRequest) -> HttpResponse:
    data = CreatePaymentRequest(data=loads(request.body))

    if data.is_valid():
        account = Account.objects.filter(id=data.cleaned_data.get('account')).first()

        if account:
            payment = Payment(account=account, amount=data.cleaned_data.get('amount'))
            payment.save()

            account.balance += data.cleaned_data.get('amount')
            account.save()

            return JsonResponse(model_to_dict(account), status=201)

    return HttpResponseBadRequest()
