from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductListView.as_view(), name='product_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    
    path('new/', views.product_new, name='new'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
