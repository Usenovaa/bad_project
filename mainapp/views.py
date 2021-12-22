from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, View
from .models import Notebook, Smartphone, Category, LatestProducts, Product
from .mixins import CategoryDetailMixin


class BaseView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_nav()
        products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'index.html', context)


class NotebookCreateView(View):
    def get(self, request):
        return render(request, 'notebook_create.html')


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category.html'
    slug_url_kwarg = 'slug'


User = get_user_model()
from cart.forms import CartAddProductForm


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})

# class CartView(View):
#     def get(self, request, *args, **kwargs):
#         print(dir(request.user.id))
#         user = request.user
#         customer = User.objects.get(username=user)
#         cart = Cart.objects.get(owner=user.id)
#         categories = Category.objects.get_categories_for_nav()
#         context = {
#             'cart': cart,
#             'categories': categories
#         }
#         return render(request, 'cart.html', context)

