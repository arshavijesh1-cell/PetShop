
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from decimal import Decimal

from .models import Product, Category, CartItem


# Home page
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


# Product list
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products.html', {
        'products': products,
        'categories': categories
    })


# Product detail
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {
        'product': product
    })


# Only staff can add products
@login_required
@user_passes_test(lambda user: user.is_staff)
def product_create(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        messages.success(request, 'Product added successfully.')
        return redirect('product_list')

    return render(request, 'product_form.html', {
        'categories': categories
    })


# Only staff can edit products
@login_required
@user_passes_test(lambda user: user.is_staff)
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')

        category_id = request.POST.get('category')
        product.category = get_object_or_404(
            Category, id=category_id
        )

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()

        messages.success(request, 'Product updated successfully.')
        return redirect('product_list')

    return render(request, 'product_form.html', {
        'product': product,
        'categories': categories
    })


# Only staff can delete products
@login_required
@user_passes_test(lambda user: user.is_staff)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')

    return render(request, 'product_confirm_delete.html', {
        'product': product
    })


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )
        return redirect('login')

    return render(request, 'registration/register.html')


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(request, 'Login successful!')

            # Return to the page the user originally requested
            next_url = (
                request.POST.get('next')
                or request.GET.get('next')
            )

            if (
                next_url
                and next_url.startswith('/')
                and not next_url.startswith('//')
            ):
                return redirect(next_url)

            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


# Logout
@login_required
@require_POST
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


# Add to cart
@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if product.stock <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_list')

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': min(quantity, product.stock)}
    )

    if not created:
        item.quantity = min(
            item.quantity + quantity,
            product.stock
        )
        item.save()

    messages.success(request, 'Product added to cart.')
    return redirect('cart')


# Cart page - login required
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related('product', 'product__category')

    total = sum(
        (item.subtotal for item in cart_items),
        Decimal('0.00')
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# Update cart quantity
@login_required
@require_POST
def update_cart(request, product_id):
    item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0 or item.product.stock <= 0:
        item.delete()
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()

    return redirect('cart')


# Remove product from cart
@login_required
@require_POST
def remove_from_cart(request, product_id):
    CartItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    messages.success(request, 'Product removed from cart.')
    return redirect('cart')
