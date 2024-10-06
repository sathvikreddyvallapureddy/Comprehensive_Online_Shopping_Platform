from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name="index"),
    path('admin_watches',views.admin_watches, name="admin_watches"),
    path('admin_orders',views.admin_orders, name="admin_orders"),
    path('admin_customers',views.admin_customers, name="admin_customers"),
    path('admin_watches/<int:id>',views.admin_viewproduct, name="admin_viewproduct"),
    path('admin_watches/admin_addproduct',views.admin_addproduct, name="admin_addproduct"),
    path('admin_watches/admin_editproduct/<int:id>',views.admin_editproduct, name="admin_editproduct"),
    path('admin_watches/admin_deleteproduct/<int:id>',views.admin_deleteproduct, name="admin_deleteproduct"),
    path('admin_customers/admin_editcustomer/<str:username>',views.admin_editcustomer, name="admin_editcustomer"),
    path('admin_customers/admin_deletecustomer/<str:username>',views.admin_deletecustomer, name="admin_deletecustomer"),
    path('admin_orders/admin_editorder/<str:tracking_no>',views.admin_editorder, name="admin_editorder"),

]