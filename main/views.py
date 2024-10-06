from email.mime import message
from http.client import HTTPResponse
from statistics import quantiles
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from main.models import *
import random
# Create your views here.

def index(request):
    data = Product.objects.filter(is_featured=True)
    return render(request, 'index.html',{'data':data})

def watches(request):
    data = Product.objects.all()
    return render(request, 'watches.html',{'data':data})

def about(request):
    return render(request, 'about.html')


@login_required(login_url="signin")
def contact(request):
    if request.method=="POST":
        message = request.POST['message']
        html_content = render_to_string('contact_email_template.html', {'name':request.user.first_name, 'email':request.user.email, 'message':message})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Contact Form',
            text_content,
            settings.EMAIL_HOST_USER,
            ['sathvikreddyvallapureddy@gmail.com'],
        )
        email.attach_alternative(html_content, "text/html")
        email.fail_silently = False
        email.send()

        messages.info(request, "Thank you for Contacting us!")
        
        email = EmailMessage(
            'Thank You for Contacting us',
            'we will reach you back soon with a solution',
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently = False
        email.send()

    return redirect('/')

def watch_detail(request,title):
    product = Product.objects.get(title=title)
    similarproducts = Product.objects.exclude(title=title)
    similarproducts = similarproducts[:4]
    return render(request, 'watch_detail.html',{'product':product, 'similarproducts':similarproducts})


def myaccount(request):
    return render(request, 'myaccount.html')

def search(request):
    if request.method=="GET":
        searchedterm = request.GET.get('searchedterm')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(title__contains=searchedterm)
            return render(request, 'search.html', {'data':product, 'searchedterm':searchedterm})
            #return redirect('watches/'+product.title)
            # #return redirect('/')


    return redirect(request.META.get('HTTP_REFERER'))


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect('/')

    if request.method == 'POST':
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, "username taken")
                
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                
            else:
                user = User.objects.create_user(username=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, "Your account has been created!!")
                login(request, user)
                

                #success email
                template = render_to_string('email_template.html', {'name':user.first_name})
                email = EmailMessage(
                    'Thanks for signing up for Timups',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user.email,],
                    )
                email.fail_silently = False
                email.send()

                return redirect('/')
        else:
            messages.info(request, "Password Not Matching")
            return redirect(signup)
        
        return redirect(signup)

    else:
        return render(request, 'signup.html')



def signin(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome %s, '% user.first_name)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('/')

        else:
            messages.success(request, 'invalid credentials')

        return redirect(signin)


    else:
        return render(request, 'signin.html')



def signout(request):
    logout(request)
    messages.info(request, 'Signed Out Successfully')
    return redirect(signin)


#@login_required(login_url='signin')
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':'product already in the cart'},safe=False)
                else:
                    product_qty = int(request.POST['product_qty'])
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return JsonResponse({'status':'product added successfully'},safe=False)
            else:
                return JsonResponse({'status':'Product not found'}, safe=False)
        else:
            return JsonResponse({'status':'Login to continue'}, safe=False)
    else:
        return redirect('/')


def movetowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':'product already in the wishlist'},safe=False)
                else:
                    Wishlist.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status':'product moved to wishlist successfully'},safe=False)
            else:
                return JsonResponse({'status':'Product not found'}, safe=False)
        else:
            return JsonResponse({'status':'Login to continue'}, safe=False)
    else:
        return redirect('/')

@login_required(login_url="signin")
def wishlist(request):
    wishlist_data = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html",{'wishlist_data':wishlist_data})

@login_required(login_url='signin')
def cart(request):
    cart_data = Cart.objects.filter(user=request.user)
    cart_data_count = Cart.objects.filter(user=request.user).count()
    total_price = 0
    for item in cart_data:
        total_price = total_price + item.product.price * item.product_qty
    context = {'cart_data':cart_data, 'cart_data_count':cart_data_count, 'total_price':total_price}
    return render(request, 'cart.html', context)

def updatecart(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        if Cart.objects.filter(user=request.user, product_id=product_id):
            product_qty = int(request.POST.get("product_qty"))
            cart = Cart.objects.get(product_id=product_id, user=request.user)
            cart.product_qty = product_qty
            cart.save()
            return JsonResponse({'status':'Updated Successfully'})
    return redirect('/')

def deletecartitem(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        #return JsonResponse({'status':product_id})
        if Cart.objects.filter(user=request.user, product_id=product_id):
            cartitem = Cart.objects.get(product_id=product_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status':'Deleted Successfully'})
    return redirect('/')


def deletewishlistitem(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        #return JsonResponse({'status':product_id})
        if Wishlist.objects.filter(user=request.user, product_id=product_id):
            wishlistitem = Wishlist.objects.get(product_id=product_id, user=request.user)
            wishlistitem.delete()
            return JsonResponse({'status':'Deleted Successfully'})
    return redirect('/')



@login_required(login_url="signin")
def checkout(request):
    checkout_data = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in checkout_data:
        total_price = total_price + item.product.price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()
    
    return render(request, 'checkout.html',{'checkout_data':checkout_data, 'total_price':total_price, 'userprofile':userprofile})




@login_required(login_url="signin")
def placeorder(request):
    if request.method == "POST":

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()



        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')


        cart_data = Cart.objects.filter(user=request.user)
        grand_total = 0
        for item in cart_data:
            grand_total = grand_total + item.product.price * item.product_qty
        
        neworder.total_price = grand_total

        tracking_no = 'timups'+str(random.randint(1111111, 9999999)) 
        while Order.objects.filter(tracking_no=tracking_no) is None:
            tracking_no = 'timups'+str(random.randint(1111111, 9999999)) 

        neworder.tracking_no = tracking_no
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.price,
                quantity = item.product_qty
            )

        # clear the cart
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed Successfully")

        payment_mode = request.POST.get('payment_mode')
        if payment_mode == 'Paid by Razorpay':
            #success email
            order_data = Order.objects.filter(user=request.user, tracking_no=tracking_no).first()
            orderitems = OrderItem.objects.filter(order=order_data)
            context = {'order_data':order_data, 'orderitems':orderitems}
            html_content = render_to_string('order_confirmation_mail_template.html', context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                'Order Confirmation',
                text_content,
                settings.EMAIL_HOST_USER,
                [request.user.email,],
            )
            email.attach_alternative(html_content, "text/html")
            email.fail_silently = False
            email.send()
            return JsonResponse({ 'status' : 'Your order has been placed Successfully'})
        
        #success email
        order_data = Order.objects.filter(user=request.user, tracking_no=tracking_no).first()
        orderitems = OrderItem.objects.filter(order=order_data)
        context = {'order_data':order_data, 'orderitems':orderitems}
        html_content = render_to_string('order_confirmation_mail_template.html', context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Order Confirmation',
            text_content,
            settings.EMAIL_HOST_USER,
            [request.user.email,],
        )
        email.attach_alternative(html_content, "text/html")
        email.fail_silently = False
        email.send()

    return redirect('myorders')



@login_required(login_url="signin")
def proceedtopay(request):
    checkout_data = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in checkout_data:
        total_price = total_price + item.product.price * item.product_qty

    return JsonResponse({
        'total_price': total_price
    })

def myorders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}

    return render(request, 'myorders.html',context)

def vieworder(request, tracking_no):
    order = Order.objects.filter(user=request.user, tracking_no=tracking_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems}

    return render(request, 'vieworder.html', context)

def forgotpassword(request):
    return render(request, 'forgotpassword.html')

def productlistAjax(request):
    products = Product.objects.all().values_list('title', flat=True)
    productsList = list(products)

    return JsonResponse(productsList, safe=False)