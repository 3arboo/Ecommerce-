from django.urls import path
from . import views


urlpatterns = [
    path('product/',views.get_all_products,name='product'),
    path('product/<str:pk>',views.get_by_id_product,name='get_by_id_product'),
    path('product/new',views.new_product,name='new_product'),
    path('product/update/<str:pk>',views.update_product,name='update_product'),
    path('product/delete/<str:pk>',views.delete_product,name='delete_product'),
    path('product/review/',views.add_review,name='review'),
    path('product/review/delete',views.delete_review,name='delete_review'),
    
]
