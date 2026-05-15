import base64
import hashlib
import json
import uuid

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .models import Product


# ──────────────────────────────────────────────
# Helpers: корзина в сессии
# ──────────────────────────────────────────────

def _get_cart(request):
    """Возвращает корзину из сессии: {product_id_str: quantity}"""
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _build_cart_items(cart):
    """
    cart = {'1': 2, '5': 1, ...}
    Возвращает (список позиций, итого Decimal)
    """
    if not cart:
        return [], 0

    product_ids  = [int(pk) for pk in cart.keys()]
    products_map = {p.pk: p for p in Product.objects.filter(pk__in=product_ids)}

    items = []
    total = 0
    for pk_str, qty in cart.items():
        product = products_map.get(int(pk_str))
        if product:
            line_total = product.price * qty
            total     += line_total
            items.append({
                'product':  product,
                'quantity': qty,
                'total':    line_total,
            })

    return items, total


# ──────────────────────────────────────────────
# Helpers: LiqPay
# ──────────────────────────────────────────────

def _liqpay_generate(amount, order_id, description):
    """
    Возвращает (data, signature) для скрытых полей формы LiqPay.
    Документация: https://www.liqpay.ua/documentation/api/aquiring/checkout
    """
    public_key  = settings.LIQPAY_PUBLIC_KEY
    private_key = settings.LIQPAY_PRIVATE_KEY

    params = {
        "version":     "3",
        "public_key":  public_key,
        "action":      "pay",
        "amount":      str(amount),
        "currency":    "UAH",
        "description": description,
        "order_id":    order_id,
        "sandbox":     "1",            # sandbox-режим, деньги не списываются
        "language":    "ru",
    }

    data_str  = base64.b64encode(json.dumps(params).encode()).decode()
    sign_str  = private_key + data_str + private_key
    signature = base64.b64encode(hashlib.sha1(sign_str.encode()).digest()).decode()

    return data_str, signature


# ──────────────────────────────────────────────
# Views
# ──────────────────────────────────────────────

def cart(request):
    cart_data              = _get_cart(request)
    cart_items, cart_total = _build_cart_items(cart_data)

    liqpay_data = liqpay_signature = ""
    if cart_items:
        order_id    = str(uuid.uuid4())
        description = "Оплата заказа Metro Shop"
        liqpay_data, liqpay_signature = _liqpay_generate(
            amount      = float(cart_total),
            order_id    = order_id,
            description = description,
        )

    return render(request, 'cart.html', {
        'cart_items':       cart_items,
        'cart_total':       cart_total,
        'liqpay_data':      liqpay_data,
        'liqpay_signature': liqpay_signature,
    })


def cart_add(request, pk):
    if request.method == 'POST':
        product   = get_object_or_404(Product, pk=pk, is_available=True)
        cart      = _get_cart(request)
        key       = str(product.pk)
        cart[key] = cart.get(key, 0) + 1
        _save_cart(request, cart)
    return redirect('cart')


def cart_update(request, pk):
    if request.method == 'POST':
        cart   = _get_cart(request)
        key    = str(pk)
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