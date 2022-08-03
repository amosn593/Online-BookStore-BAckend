from django.urls import path

from order import views

urlpatterns = [
    # path('access/', views.getAccessToken, name='get_mpesa_access_token'),
    path('checkout/', views.checkout),
    path('orders/', views.OrdersList.as_view()),
]
