from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegUserView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('order/', OrderListView),
    path('order/<int:pk>', OrderDitaliView),
    path('cart/', CartListview),
    path('cart/<int:pk>', CartDetilView),
    path('product/', ProductListView),
    path('product/<int:pk>', ProductDetilView)
]