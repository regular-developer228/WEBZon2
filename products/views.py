from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product


def index(request):
    context = {
        'featured_products': Product.objects.filter(is_available=True).order_by('-created_at')[:6],
        'new_products':       Product.objects.filter(is_available=True).order_by('-created_at')[:10],
        'bestsellers':        Product.objects.filter(is_available=True)[:10],
        'sale_products':      Product.objects.filter(is_available=True)[:10],
        'recommended_products': Product.objects.filter(is_available=True)[:10],
        'categories':         Category.objects.all(),
    }
    return render(request, 'index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.review_set.all()
    avg_rating = (
        sum(r.rating for r in reviews) / len(reviews)
        if reviews else None
    )
    return render(request, 'product_detail.html', {
        'product':    product,
        'reviews':    reviews,
        'avg_rating': avg_rating,
    })


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, is_available=True).order_by('-created_at')
    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
    })


def cart(request):
    return render(request, 'cart.html')


def search(request):
    query = request.GET.get('q', '').strip()
    results = (
        Product.objects.filter(name__icontains=query, is_available=True)
        if query else Product.objects.none()
    )
    return render(request, 'search.html', {
        'query':   query,
        'results': results,
    })


def filter_view(request):
    categories = Category.objects.all()
    products   = Product.objects.filter(is_available=True)

    cat_id   = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if cat_id:
        products = products.filter(category_id=cat_id)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    return render(request, 'filter.html', {
        'categories': categories,
        'products':   products,
    })


def _get_cart(request):
    """Возвращает корзину из сессии: {product_id_str: quantity}"""
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _build_cart_items(cart):
    """
    Возвращает список словарей и итоговую сумму.
    cart = {'1': 2, '5': 1, ...}
    """
    if not cart:
        return [], 0

    product_ids = [int(pk) for pk in cart.keys()]
    products = Product.objects.filter(pk__in=product_ids)
    products_map = {p.pk: p for p in products}

    items = []
    total = 0
    for pk_str, qty in cart.items():
        product = products_map.get(int(pk_str))
        if product:
            line_total = product.price * qty
            total += line_total
            items.append({
                'product': product,
                'quantity': qty,
                'total': line_total,
            })

    return items, total


# ---- views ----

def cart(request):
    cart_data = _get_cart(request)
    cart_items, cart_total = _build_cart_items(cart_data)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def cart_add(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk, is_available=True)
        cart = _get_cart(request)
        key = str(product.pk)
        cart[key] = cart.get(key, 0) + 1
        _save_cart(request, cart)
    return redirect('cart')


def cart_update(request, pk):
    """Увеличить или уменьшить количество товара."""
    if request.method == 'POST':
        cart = _get_cart(request)
        key = str(pk)
        action = request.POST.get('action')

        if key in cart:
            if action == 'increase':
                cart[key] += 1
            elif action == 'decrease':
                cart[key] -= 1
                if cart[key] <= 0:
                    del cart[key]

        _save_cart(request, cart)
    return redirect('cart')


def cart_remove(request, pk):
    if request.method == 'POST':
        cart = _get_cart(request)
        cart.pop(str(pk), None)
        _save_cart(request, cart)
    return redirect('cart')


def cart_clear(request):
    if request.method == 'POST':
        _save_cart(request, {})
    return redirect('cart')