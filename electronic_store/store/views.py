from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product, Order

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
    template_name = 'store/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

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
        print("🟢 استقبلنا POST")

        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = float(request.POST.get('price'))
            stock = int(request.POST.get('stock'))
            sku = request.POST.get('sku')
            image = request.FILES.get('image')
            category_id = request.POST.get('category')

            print("بيانات جاية:", name, price, stock)

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
            print("✅ المنتج اتسجل:", product)
            return redirect('store:product_list')

        except Exception as e:
            print("⛔ حصل Error:", e)

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
