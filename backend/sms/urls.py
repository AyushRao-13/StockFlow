from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('purchase/', views.index, name='index'),
    path('issued/', views.issued, name='issued'),
    path('exports/purchases.csv', views.export_purchases_csv, name='export_purchases_csv'),
    path('exports/issued.csv', views.export_issued_csv, name='export_issued_csv'),
    path('profile/',views.profile, name='profile'),
]