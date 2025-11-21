from django.shortcuts import render , redirect ,  get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .import models
from .import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Cart ,  UserProfile
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def navbar(request):
    products = Product.objects.all()
    return render(request , 'navbar.html',  {'products': products[0:5]} )

def sign_up(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('sign_up')

            # Create user safely
            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('log_in')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.UserForm()  # ✅ corrected

    return render(request, 'sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('navbar')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('log_in')

    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

def shop(request):
    return render(request , 'shop.html')

def seller(request):
    products = Product.objects.all()
    return render(request , 'seller.html' , {'products': products[5:19]})

def festiv(request):
    products = Product.objects.all()
    return render(request , 'festiv.html' , {'products': products[19:21]})
    
def french(request):
    products = Product.objects.all()
    return render(request , 'french.html' , {'products': products[21:41]})
    
def wear(request):
    products = Product.objects.all()
    return render(request , 'wear.html' , {'products': products[41:49]})

def ombre(request):
    products = Product.objects.all()
    return render(request , 'ombre.html' , {'products': products[49:54]})

def holiday(request):
    products = Product.objects.all()
    return render(request , 'holiday.html' , {'products': products[54:61]})

def party(request):
    products = Product.objects.all()
    return render(request , 'party.html' , {'products': products[61:72]})

def wedding(request):
    products = Product.objects.all()
    return render(request , 'wedding.html' , {'products': products[72:78]})

def formal(request):
    products = Product.objects.all()
    return render(request , 'formal.html' , {'products': products[78:86]})

def short(request):
    products = Product.objects.all()
    return render(request , 'short.html' , {'products': products[86:95]})

def medium(request):
    products = Product.objects.all()
    return render(request, 'medium.html' , {'products': products[95:101]})

def long(request):
    products = Product.objects.all()
    return render(request , 'long.html' , {'products': products[101:112]})

def almond(request):
    products = Product.objects.all()
    return render(request , 'almond.html' , {'products': products[112:120]})

def round(request):
    products = Product.objects.all()
    return render(request , 'round.html' , {'products': products[120:130]})

def square(request):
    products = Product.objects.all()
    return render(request , 'square.html' , {'products': products[130:144]})

def stiletto(request):
    products = Product.objects.all()
    return render(request , 'stiletto.html' , {'products': products[144:150]})

def all(request):
    products = Product.objects.all()
    return render(request , 'all.html' , {'products': products})

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('navbar')
    form = forms.ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required(login_url='log_in')

def details(request,id):
    product = get_object_or_404(Product, id=id)
    quantity = 1  # default

    if request.method == 'POST':
        # Detect if increment or decrement button pressed
        if 'increment' in request.POST:
            quantity = int(request.POST.get('quantity', 1)) + 1
        elif 'decrement' in request.POST:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 1:
                quantity -= 1
        else:
            # Other form submit or initial
            quantity = int(request.POST.get('quantity', 1))
    
    form = forms.OrderForm(initial={'quantity': quantity})
    return render(request, 'details.html', {'form': form , 'product': product})

@login_required(login_url='log_in')
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = Product.objects.get(id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({"message": f"Added {product.name} to cart!"})
    return JsonResponse({"message": "Invalid request"}, status=400)

@login_required(login_url='log_in')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})

@login_required(login_url='log_in')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required(login_url='log_in')
def buy(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        phone = request.POST.get('phone', '')
        country = request.POST.get('country', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        pin = request.POST.get('pin', '')

        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.firstname = firstname
        profile.lastname = lastname
        profile.phone = phone
        profile.country = country
        profile.address = address
        profile.city = city
        profile.state = state
        profile.pin = pin
        profile.save()
        

        return redirect('payment')
    # render by default (no else)
    return render(request, 'buy.html', {"cart_items": cart_items, "total": total})

@login_required(login_url='log_in')
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    try:
        profile = UserProfile.objects.filter(user=request.user).first()

        # If profile is missing, redirect back to buy page
        if not profile:
            print("⚠️ No profile found for user:", request.user)
            return redirect('buy')

        # ✅ Include total and cart_items in the render context
        return render(request, 'payment.html', {
            'firstname': profile.firstname,
            'lastname': profile.lastname,
            'phone': profile.phone,
            'cart_items': cart_items,
            'total': total,
            'country': profile.country,
            'city': profile.city
        })

    except Exception as e:
        print("⚠️ Error in payment view:", e)
        return render(request, 'payment.html', {
            'firstname': '',
            'lastname': '',
            'phone': '',
            'cart_items': cart_items,
            'total': total,
            'country': country,
            'city': city
        })
