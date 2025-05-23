from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from .models import Category, Product, Order
from .forms import *
from django.urls import reverse_lazy

from .serializers import ProductSerializer
from rest_framework.decorators import api_view 
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.filter(status=True)

    template_name = 'store/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('store:product_detail', kwargs={'slug': self.object.slug})

# CREATE
# def product_new(request):
#     categories = Category.objects.all()
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         stock = request.POST.get('stock')
#         image = request.FILES.get('image')
#         sku = request.POST.get('sku')
#         category_id = request.POST.get('category')

#         if all([name, description, price, stock, sku, category_id]):
#             category = get_object_or_404(Category, id=category_id)
#             Product.objects.create(
#                 name=name,
#                 description=description,
#                 price=price,
#                 stock=stock,
#                 image=image,
#                 sku=sku,
#                 category=category
#             )
#             return redirect('store:product_list')

#     return render(request, 'store/new.html', {'categories': categories})
def product_new(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        print("reseve the POST")

        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = float(request.POST.get('price'))
            stock = int(request.POST.get('stock'))
            sku = request.POST.get('sku')
            image = request.FILES.get('image')
            category_id = request.POST.get('category')

            print("comming data:", name, price, stock)

            category = Category.objects.get(id=category_id)

            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                sku=sku,
                category=category,
                image=image
            )
            print("product added", product)
            return redirect('store:product_list')

        except Exception as e:
            print(" Error:", e)

    return render(request, 'store/new.html', {'categories': categories})

# UPDATE
def update(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.sku = request.POST.get('sku')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('store:product_list')

    return render(request, 'store/update.html', {'product': product, 'categories': categories})




# DELETE
def delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('store:product_list')
    return render(request, 'store/delete.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  
            return redirect(product.get_absolute_url())  
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})



# ---------------------------lab4----------------------

# from django.views.generic import *

class Insertcategory(CreateView):
    model = Category
    success_url = reverse_lazy('store:category_list')

    # form_class = CategoryForm
    fields = '__all__'
    queryset = Category.objects.filter(status=True)
    content_object_name = 'add_category'
    template_name = 'store/insert_category.html'

class UpdateCategory(UpdateView):
    model = Category
    # form_class = CategoryForm
    queryset = Category.objects.filter(status=True)
    fields = '__all__'
    template_name = 'store/update_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('store:category_list')

# class DeleteCategory(DeleteView):
#     model = Category
#     template_name = 'store/delete_category.html'
#     context_object_name = 'category'
#     success_url = reverse_lazy('store:category_list')

#     def get_object(self):
#         return get_object_or_404(Category, id=self.kwargs['pk'])

#     def delete(self, request, *args, **kwargs):  # Fixed method signature
#         self.object = self.get_object()
#         self.object.status = False
#         self.object.save()
#         return redirect(self.get_success_url())

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.filter(status=True)
#         return context



# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class DeleteCategory(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'store/delete_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('store:category_list')

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs['pk'])

    # @login_required

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = False  # Soft delete: set status to False
        self.object.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status=True)
        return context



@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# from .serializers import ProductSerializer

class ProductUpdateAPIView(APIView):
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from rest_framework import generics
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

# ✅ Update by ID
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

# ✅ Delete by ID
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'



from rest_framework import viewsets
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer