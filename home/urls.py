from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home import views

from django.contrib.auth.views import LogoutView
from .views import Reviews

urlpatterns = [
    path('', views.home , name='home'),
    path('product/<int:pk>', views.product , name='product'),
    path('rate/<int:pk>', views.Reviews.as_view() , name='reviews'),
    path('addproduct/', views.addproduct , name='addproduct'),
    path('edit/<int:pk>', views.edit , name='edit'),
    path('delete/<int:pk>', views.deleteWatch , name='deleteWatch'),
    path('login/', views.login , name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('search_product/', views.search_product, name='search_product'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)