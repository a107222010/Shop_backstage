from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns =[
    path('',views.menu_list),
    path('insertmenu',views.InsertMenu),
    path('product_manage/<pk>/',views.product_manage, name='product_manage'),
    path('product_manage_edit/<pk>/<slug:product_size>/',views.product_manage_edit),
    path('order', views.order),
    path('order_done', views.order_done),
    path('order_manage/<id>/<detail_id>', views.order_manage),
    path('order_manage/order_fix/<detail_id>/<id>/<pk>', views.order_fix),
    path('comment', views.comment),
    path('edit_password', views.editPassword),
    path('member', views.member),
    
    path('plus',views.plus),
    
    path('singleplus1', views.singleplus1),
    path('singleplus1_edit/<pk>', views.singleplus1_edit,name='singleplus1_edit'),

    path('singleplus2', views.singleplus2),
    path('singleplus2_edit/<pk>', views.singleplus2_edit,name="singleplus2_edit"),
    
    path('singleplus3', views.singleplus3),
    path('singleplus3_edit/<pk>', views.singleplus3_edit,name="singleplus3_edit"),

    path('multi_plus', views.multi_plus),
    path('multi_plus_edit/<pk>', views.multi_plus_edit,name="multi_plus_edit"),

    path('product_type', views.product_type),
    path('product_type_edit/<pk>', views.product_type_edit,name="product_type_edit"),


    path('product_case', views.product_case),
    path('product_case_edit/<str:product_case>', views.product_case_edit),

    path('advertise',views.advertise),
    path('shop_photo',views.shop_photo),
    path('banner',views.banner),
    path('edit_banner/<pk>',views.edit_banner),
    path('create_staff',views.create_staff),
]

