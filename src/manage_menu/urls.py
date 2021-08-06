from django.urls import path
from . import views

app_name = 'starbucks'

urlpatterns =[
    path('',views.chart),
    path('menu_list',views.menu_list),
    path('insertmenu',views.InsertMenu),
    path('product_manage/<pk>/',views.product_manage),
    path('order', views.order),
    path('order_manage/<id>/<detail_id>', views.order_manage),
    path('order_manage/order_fix/<detail_id>/<id>/<pk>', views.order_fix),
    path('comment', views.comment),
    path('edit_password', views.editPassword),
    path('member', views.member),
    
    path('ice_plus', views.ice_plus),
    path('sugar_plus', views.sugar_plus),
    path('coffee_plus', views.coffee_plus),
    path('plus', views.plus),
    path('product_type', views.product_type),

    path('advertise',views.advertise),
    path('shop_photo',views.shop_photo),
    path('banner',views.banner),
]

