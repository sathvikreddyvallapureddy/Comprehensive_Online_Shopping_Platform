from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from email.mime import message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags



from main.models import *



@login_required(login_url="signin")
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        watches_count = Product.objects.all().count()
        orders_count = Order.objects.all().count()
        customers_count = User.objects.all().count()
        return render(request, "admin_index.html", {'watches_count':watches_count, 'orders_count':orders_count, 'customers_count':customers_count})

    else:
        messages.info(request, "You are not an admin!")
        return redirect('/')


@login_required(login_url="signin")
def admin_watches(request):
    product_data = Product.objects.all()
    product_data_count = Product.objects.all().count()
    return render(request, "admin_watches.html", {'product_data':product_data, 'product_data_count':product_data_count})


@login_required(login_url="signin")
def admin_orders(request):
    order_data = Order.objects.all()
    order_data_count = Order.objects.all().count()
    if request.method == "POST":
        trackingno = request.POST['trackingno']
        status = request.POST['order_status']
        order = Order.objects.get(tracking_no=trackingno)
        order.status = status
        order.save()


        #success email
        if status == "Out For Shipping":
            html_content = render_to_string('order_shipped_email_template.html', {'name':order.user.first_name, 'tracking_no':trackingno})
        elif status == "Completed":
            html_content = render_to_string('order_delivered_email_template.html', {'name':order.user.first_name, 'tracking_no':trackingno})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Order Status',
            text_content,
            settings.EMAIL_HOST_USER,
            [order.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.fail_silently = False
        if email.send():
            print("Yesss")
        else:
            print("Noooooo")
        messages.info(request, "Updated!!")

    return render(request, "admin_orders.html", {'order_data':order_data, 'order_data_count':order_data_count})


@login_required(login_url="signin")
def admin_customers(request):
    customer_data = User.objects.all()
    customer_data_count = User.objects.all().count()
    return render(request, "admin_customers.html", {'customer_data':customer_data, 'customer_data_count':customer_data_count})


@login_required(login_url="signin")
def admin_viewproduct(request,id):
    if Product.objects.filter(id=id):
        product_data = Product.objects.get(id=id)
        return render(request, 'admin_viewproduct.html', {'product_data':product_data})
    return redirect('/adminpanel/admin_watches')


@login_required(login_url="signin")
def admin_addproduct(request):
    if request.method == 'POST':
        product_title = request.POST['product_title']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        if request.POST.get('product_is_featured',False):
            product_is_featured = True
        else:
            product_is_featured = False

        product_image = request.FILES.get('product_image', False)
        if product_image == False:
            messages.info(request, "All Fields are mandatory!")
            return redirect('/adminpanel/admin_watches/admin_addproduct')

        if product_title=="" or product_description=="" or product_price=="":
            messages.info(request, "All Fields are mandatory!")
            return redirect('/adminpanel/admin_watches/admin_addproduct')

        
        Product.objects.create(title=product_title, description=product_description, price=product_price, is_featured=product_is_featured, image=product_image)
        messages.info(request, "Product has been Added!")
        return redirect('/adminpanel/admin_watches')

    else:
        return render(request, 'admin_addproduct.html')


@login_required(login_url="signin")
def admin_editproduct(request, id):
    product_data = Product.objects.get(id=id)

    if request.method == 'POST':
        product_title = request.POST['product_title']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        if request.POST.get('product_is_featured',False):
            product_is_featured = True
        else:
            product_is_featured = False

        product_image = request.FILES.get('product_image', False)

        if product_title=="" or product_description=="" or product_price=="":
            messages.info(request, "All Fields are mandatory!")
            return redirect('/adminpanel/admin_watches/admin_editproduct/{{id}}')

        product_data.title = product_title
        product_data.description = product_description
        product_data.price = product_price
        product_data.is_featured = product_is_featured
        if product_image:
            product_data.image = product_image
        
        product_data.save()
        
        messages.info(request, "Product has been Updated!")
        return redirect('/adminpanel/admin_watches')

    else:
        return render(request, "admin_editproduct.html",{'product_data':product_data})


@login_required(login_url="signin")
def admin_deleteproduct(request,id):
    if Product.objects.filter(id=id):
        product_data = Product.objects.get(id=id)
        product_data.delete()
        messages.info(request, "Product has been Deleted!")
        return redirect('/adminpanel/admin_watches')
    
    return redirect('/adminpanel/admin_watches')
    
@login_required(login_url="signin")
def admin_editcustomer(request, username):
    customer_data = User.objects.get(username=username)

    if request.method == "POST":
        customer_data.first_name = request.POST['customer_first_name']
        customer_data.last_name = request.POST['customer_last_name']
        customer_data.email = request.POST['customer_email']
        if request.POST.get('customer_is_active',False):
            customer_data.is_active= True
        else:
            customer_data.is_active = False


        if request.POST.get('customer_is_admin',False):
            customer_data.is_superuser = True
        else:
            customer_data.is_superuser = False

        customer_data.save()

        messages.info(request, "Customer has been Updated!")
        return redirect('/adminpanel/admin_customers')

    return render(request, "admin_editcustomer.html", {'customer_data':customer_data})


@login_required(login_url="signin")
def admin_deletecustomer(request,username):
    if User.objects.filter(username=username):
        customer_data = User.objects.get(username=username)
        customer_data.delete()
        messages.info(request, "Customer has been Deleted!")
        return redirect('/adminpanel/admin_customers')
    
    return redirect('/adminpanel/admin_customers')

@login_required(login_url="signin")
def admin_editorder(request, tracking_no):
    order_data =  Order.objects.filter(tracking_no=tracking_no).first()
    return render(request, "admin_editorder.html", {'order_data':order_data})
