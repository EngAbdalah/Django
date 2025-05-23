from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    # path('products/<slug:slug>/', views.ProductListView.as_view(), name='product_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    
    path('new/', views.product_new, name='new'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('add/', views.add_product, name='add_product'),
    # path('<slug:slug>/',views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/update/',views.ProductUpdateView.as_view(), name='product_update'),
    path('insertcat/', views.Insertcategory.as_view(), name='add_category'),
    path('updatecategory/<int:pk>/', views.UpdateCategory.as_view(), name='update_category'),
    path('deletecategory/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),
    path('products/', views.product_list_create, name='product-list-create'),
    path('products/<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<int:pk>/',views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/',views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
