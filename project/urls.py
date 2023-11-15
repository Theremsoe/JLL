from django.urls import path

from app import views

# Wire up your API routes here
urlpatterns = [
    path('accounts/', views.account_create),
    path('accounts/<int:id>/', views.account_read),
    path('payments/', views.payment_create)
]
