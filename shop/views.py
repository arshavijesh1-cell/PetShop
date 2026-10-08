from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories
        }
    )


def product_list(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(
            category_id=category_id
        )

    return render(
        request,
        'products.html',
        {
            'products': products,
            'categories': categories
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )


def product_create(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        category = get_object_or_404(
            Category,
            id=category_id
        )

        Product.objects.create(
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        return redirect('product_list')

    return render(
        request,
        'product_form.html',
        {
            'categories': categories
        }
    )


def product_update(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    categories = Category.objects.all()

    if request.method == 'POST':

        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')

        category_id = request.POST.get('category')

        product.category = get_object_or_404(
            Category,
            id=category_id
        )

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()

        return redirect('product_list')

    return render(
        request,
        'product_form.html',
        {
            'product': product,
            'categories': categories
        }
    )

def product_delete(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        return redirect('product_list')

    return render(
        request,
        'product_confirm_delete.html',
        {
            'product': product
        }
    )


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        from django.contrib.auth.models import User

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

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

    return render(
        request,
        'registration/register.html'
    )


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

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'registration/login.html'
    )


def user_logout(request):

    logout(request)

    messages.success(
        request,
        'Logged out successfully.'
    )

    return redirect('home')


