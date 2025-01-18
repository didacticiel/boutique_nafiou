from django.urls import path
from .views import (
    Index, store, detail, Login, logout, Signup,SuccessView, 
    CheckOut, OrderView, about, contact,all_product,
    bazin,OrderConfirmation,homme,femme,enfant
)

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store/', store, name='store'),
    path('all_product/', all_product, name='all_product'),
    path('bazin/', bazin, name='bazin'),
    path('homme/', homme, name='homme'),
    path('femme/', femme, name='femme'),
    path('enfant/', enfant, name='enfant'),


    path('success/', SuccessView.as_view(), name='success'),  
    path('product/<int:my_id>/', detail, name='detail'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', Signup.as_view(), name='signup'),
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('order-confirmation/', OrderConfirmation.as_view(), name='order_confirmation'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]