from json.decoder import JSONDecodeError

from django.test import TestCase
from rest_framework.test import RequestsClient
from rest_framework import status

HOST = 'http://localhost:8000'
ACCOUNTS_ENDPOINT = HOST + '/accounts/'
PAYMENTS_ENDPOINT = HOST + '/payments/'


def get_account_endpoint(account_id):
    return HOST + '/accounts/%d/' % account_id


class CreateAccountTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()

    def test_with_valid_payload(self):
        r = self.client.post(ACCOUNTS_ENDPOINT, data={})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        data = r.json()
        expected_account = {
            'id': 1,
            'balance': 0,
        }
        self.assertEqual(data, expected_account)


class MakePaymentTestCase(TestCase):
    def setUp(self):
        self.client = RequestsClient()
        try:
            self.account = self.client.post(ACCOUNTS_ENDPOINT, data={}).json()
        except JSONDecodeError:
            self.fail('Implement correct POST method for the endpoint')

    def test_with_existing_account(self):
        payment_payload = {
            'account': self.account['id'],
            'amount': 1000,
        }
        r = self.client.post(PAYMENTS_ENDPOINT, data=payment_payload)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        data = r.json()
        expected_payment = {
            'id': 1,
            'account': self.account['id'],
            'amount': 1000,
        }
        self.assertEqual(data, expected_payment)

    def test_with_non_existing_account(self):
        payment_payload = {
            'account': 2,
            'amount': 1000,
        }
        r = self.client.post(PAYMENTS_ENDPOINT, data=payment_payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class GetAccountTestCase(TestCase):
    def setUp(self):
        self.client = RequestsClient()
        try:
            self.account = self.client.post(ACCOUNTS_ENDPOINT, data={}).json()
        except JSONDecodeError:
            self.fail('Implement correct POST method for the endpoint')

    def test_with_no_payments(self):
        url = get_account_endpoint(self.account['id'])
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        expected_account = {
            'id': self.account['id'],
            'balance': 0,
        }
        self.assertEqual(data, expected_account)

    def test_with_two_payments(self):
        payment_payloads = [
            {'account': self.account['id'], 'amount': 1000},
            {'account': self.account['id'], 'amount': 899},
        ]

        for payload in payment_payloads:
            self.client.post(PAYMENTS_ENDPOINT, data=payload)

        url = get_account_endpoint(self.account['id'])
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()

        expected_balance = sum(obj['amount'] for obj in payment_payloads)
        expected_account = {
            'id': self.account['id'],
            'balance': expected_balance,
        }
        self.assertEqual(data, expected_account)

    def test_with_payments_to_different_accounts(self):
        another_account = self.client.post(ACCOUNTS_ENDPOINT, data={}).json()
        payment_payloads = [
            {'account': self.account['id'], 'amount': 1000},
            {'account': another_account['id'], 'amount': 899},
            {'account': self.account['id'], 'amount': 500},
        ]

        for payload in payment_payloads:
            self.client.post(PAYMENTS_ENDPOINT, data=payload)

        url = get_account_endpoint(self.account['id'])
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()

        expected_balance = sum(obj['amount'] for obj in payment_payloads
                               if obj['account'] == self.account['id'])
        expected_account = {
            'id': self.account['id'],
            'balance': expected_balance,
        }
        self.assertEqual(data, expected_account)

    def test_with_non_existing_account(self):
        url = get_account_endpoint(2)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
