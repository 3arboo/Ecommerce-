from django.urls import path
from . import views


urlpatterns = [
    path('orders/new',views.new_order,name='new_order'),
    path('orders/procces/<str:pk>',views.procces_orders,name='update_order'),
    path('orders/',views.get_orders,name='new_order'),
    path('order/<str:pk>',views.get_order,name='new_order'),   
    path('orders/delete/<str:pk>',views.delete_order,name='new_order'),   
]
