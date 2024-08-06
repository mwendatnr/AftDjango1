
from django.contrib import admin
from django.urls import path
from hospitalapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index,name='home'),
    path('inner/', views.inner, name='inner'),
    path('about/', views.about,name= 'about'),
    path('doctors/', views.doctor,name='doctor'),
    path('appointment/', views.appointment,name='appointment'),
    path('show/', views.show,name='show'),
    path('patients/', views.patients,name='patient'),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('', views.register, name='register'),
    path('login/', views.login, name='login')
]
