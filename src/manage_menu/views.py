from django.shortcuts import render, redirect
from .models import Customized, OrderDetail, Product, ProductSize, ProductAddrule, ShopDetail, Sort, Comment, Singleplus1, Singleplus2, Singleplus3, Multipleplus,DrinkOrder,CustomizedPlus,Guest, Advertise
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from dynamic_db_router import in_database
from django.db import connections
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.db.models import Avg, Sum, Count
import pandas as pd


@login_required
def chart(request):
    user = request.user
    labels = []
    data = []

    # queryset = City.objects.values('country__name').annotate(country_population=Sum('population')).order_by('-country_population')
    
    # for entry in queryset:
    #     labels.append(entry['country__name'])
    #     data.append(entry['country_population'])
 
 
    # return JsonResponse(data={
    #     'labels': labels,
    #     'data': data,
    # })

    month_price = OrderDetail.objects.using(user.username).aggregate(Sum('detail_price'))
    avg_daily_price = OrderDetail.objects.using(user.username).aggregate(Avg('detail_price'))

    test1 = OrderDetail.objects.using(user.username).values('productsize_id').annotate(total=Count('*'))
    df = pd.DataFrame(test1)
    # print(df)
    df1 = df['productsize_id'].tolist()
    # print(df1)
    df = df['total'].tolist()
    # print(df)
    # cursor = connections[user.username].cursor()
    # cursor.execute('SELECT product.product_name ,COUNT(*) as 次數 FROM order_detail \
    #                 left join product_size on order_detail.productsize_id = product_size.productsize_id \
    #                 left join product on product_size.product_id = product.product_id GROUP BY product_name')
    # saverecord = cursor.fetchall()




    context = {
        'month_price':month_price,
        'avg_daily_price':avg_daily_price,
        'df':df,
        'df1':df1,
    }

    return render(request, 'chart.html',context)



@login_required
def menu_list(request):
    user = request.user


    saverecord = Product.objects.using(user.username).all()


    paginator = Paginator(saverecord,5)

    page = request.GET.get('page')

    saverecord = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        saverecord = Product.objects.using(user.username).filter(Q(product_name__icontains=search)|Q(product_sort__icontains=search)|Q(product_id__icontains=search))
       
        if not request.GET['search']:
            return redirect('/')

    context = {
        'saverecord':saverecord
    }
    return render(request, 'menu_list.html',context)


@login_required
def InsertMenu(request):
    user = request.user 

    
    saverecord_addrule = ProductAddrule.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()

    if request.method == 'POST':

        p_id = request.POST.get('product_id')
        p_name = request.POST.get('product_name')
        p_sort = request.POST.get('product_sort')
        p_pic = request.FILES['product_pic']       
        p_add = request.POST.get('product_add')
        p_introduction = request.POST.get('product_introduction')
        Product.objects.using(user.username).create(product_id=p_id,product_name=p_name,product_sort=p_sort,product_pic=p_pic,product_add=p_add,product_introduction=p_introduction)

        small = request.POST.get('small_price')
        small = int('0' + small)

        medium = request.POST.get('medium_price')
        medium = int('0' + medium)

        big = request.POST.get('big_price')
        big = int('0' + big)

        superbig = request.POST.get('superbig_price')
        superbig = int('0' + superbig)

        bottle = request.POST.get('bottle_price')
        bottle = int('0' + bottle)

        cursor = connections[user.username].cursor()
        if small > 0:
            small_id = p_id + '0'            
            cursor.execute('INSERT INTO product_size(productsize_id, product_id, product_size, product_price) VALUES (%s,%s,"小杯",%s)',[small_id,p_id,small])
        if medium > 0:
            medium_id = p_id + '1'
            cursor.execute('INSERT INTO product_size(productsize_id, product_id, product_size, product_price) VALUES (%s,%s,"中杯",%s)',[medium_id,p_id,medium])
        if big > 0:
            big_id = p_id + '2'
            cursor.execute('INSERT INTO product_size(productsize_id, product_id, product_size, product_price) VALUES (%s,%s,"大杯",%s)',[big_id,p_id,big])
        if superbig > 0:
            superbig_id = p_id + '3'
            cursor.execute('INSERT INTO product_size(productsize_id, product_id, product_size, product_price) VALUES (%s,%s,"特大杯",%s)',[superbig_id,p_id,superbig])            
        if bottle > 0:
            bottle_id = p_id + '5'
            cursor.execute('INSERT INTO product_size(productsize_id, product_id, product_size, product_price) VALUES (%s,%s,"每份",%s)',[bottle_id,p_id,bottle])            

        return redirect('/')

    context = {
        'saverecord_addrule':saverecord_addrule,
        'sort':sort,
    }
    return render(request, 'product_Insert.html',context)    

@login_required
def product_manage(request, pk):

    user = request.user 

    sort = Sort.objects.using(user.username).all()
    saverecord = Product.objects.using(user.username).get(pk=pk)
    saverecords = ProductSize.objects.using(user.username).filter(product_id=pk)
    saverecord_addrule = ProductAddrule.objects.using(user.username).all()

    product_size = []
    product_price = []
    productsize_id = []
    product_addrule = []

    for add_rule in saverecord_addrule:
        product_add = add_rule.product_add
        product_addrule.append(product_add)

    for x in saverecords:
        
        if len(x.product_size) > 0:
            product_size.append(x.product_size)

        product_price.append(x.product_price)
        productsize_id.append(x.productsize_id) 

    if request.method == 'POST':
        if 'save' in request.POST:
            product_price_get = []
            test = request.POST.get('product_id')
            saverecord.product_id = request.POST.get('product_id')
            saverecord.product_name = request.POST.get('product_name')
            saverecord.product_sort = request.POST.get('product_sort')
        
            if bool(request.FILES.get('product_pic', False)) == True:
                saverecord.product_pic = request.FILES['product_pic']
            else:
                pass

            saverecord.product_add = request.POST.get('product_add')
            saverecord.product_introduction = request.POST.get('product_introduction')

            product_price_get = request.POST.getlist('product_prices')    

            if len(product_price_get) != len(product_size):
                print("No!")
            
            else:
                cursor = connections[user.username].cursor()
                for i in range(len(product_size)):
                    cursor.execute('UPDATE product_size SET product_id = %s ,product_size=%s ,product_price=%s WHERE productsize_id=%s',[pk,product_size[i],product_price_get[i],productsize_id[i]])
                     

            saverecord.save()

            return redirect('/')

        if 'delete' in request.POST:
            saverecord.delete()
            cursor = connections[user.username].cursor()
            cursor.execute('DELETE FROM product_size WHERE product_id = %s',[pk])
            cursor.execute('DELETE FROM product WHERE product_id = %s',[pk])
            return redirect('/')

    context = {
        'saverecord':saverecord,
        'product_size':product_size,
        'product_price':product_price,
        'product_addrule':product_addrule,
        'sort':sort,
    }

    return render(request, 'product_manage.html', context)   

@login_required
def order(request):
    user = request.user 

    
    cursor = connections[user.username].cursor()
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id ORDER BY drink_order.order_date ASC')
    saverecord = cursor.fetchall()

    paginator = Paginator(saverecord,10)

    page = request.GET.get('page')

    saverecord = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        saverecord = DrinkOrder.objects.using(user.username).filter(Q(order_id__icontains=search)|Q(Guest__guest_account__icontains=search))
        # cursor = connection.cursor()
        # cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id where drink_order.order_id = %s ORDER BY drink_order.order_date ASC',[search])
        # saverecord = cursor.fetchall()

        if not request.GET['search']:
            cursor = connections[user.username].cursor()
            cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id ORDER BY drink_order.order_date ASC')
            saverecord = cursor.fetchall()

            paginator = Paginator(saverecord,10)

            page = request.GET.get('page')

            saverecord = paginator.get_page(page)
    

    context = {
        'saverecord':saverecord,
    }

    return render(request, 'order.html',context)

@login_required
def order_manage(request,id,detail_id):

    user = request.user
    
    cursor = connections[user.username].cursor()   
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name, order_detail.detail_id, order_detail.detail_price,order_detail.detail_quantity,product_size.product_size,singleplus_1.name ,singleplus_2.name, singleplus_3.name, customized.add_other, product.product_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id left join customized on customized.customized_id = order_detail.customized_id left join singleplus_1 on customized.sp1_number = singleplus_1.number left join singleplus_2 on customized.sp2_number = singleplus_2.number left join singleplus_3 on customized.sp3_number = singleplus_3.number where drink_order.order_id = %s and order_detail.detail_id = %s ORDER BY drink_order.order_date ASC',[id,detail_id])
    # cursor.execute('SELECT DISTINCT drink_order.*,product.product_name, order_detail.detail_id, order_detail.detail_price,order_detail.detail_quantity,product_size.product_size,ice.name AS ice_name,sugar.name as sugar_name, coffee_plus.name as coffee_plus_name, customized.add_other, product.product_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id left join customized on customized.customized_id = order_detail.customized_id left join ice on customized.ice_id = ice.number left join sugar on customized.sugar_id = sugar.number left join coffee_plus on customized.coffeebeans_id = coffee_plus.number where drink_order.order_id = %s and order_detail.detail_id = %s ORDER BY drink_order.order_date ASC',[id,detail_id])
    saverecord = cursor.fetchall()

    cursor1 = connections[user.username].cursor()
    cursor1.execute('SELECT multipleplus.name,multipleplus.price FROM drink_order inner join order_detail on drink_order.order_id = order_detail.order_id left join customized on customized.customized_id = order_detail.customized_id inner join customized_plus on customized.customized_id = customized_plus.customized_id inner join multipleplus on customized_plus.mp_number = multipleplus.number where drink_order.order_id = %s AND customized_plus.customized_id = %s',[id,detail_id])
    saverecord1 = cursor1.fetchall()
    

    context = {
        'saverecord':saverecord,
        'saverecord1':saverecord1,

    }

    return render(request, 'order_manage.html',context)

@login_required
def order_fix(request,detail_id,id,pk):

    user = request.user

    product_size = ProductSize.objects.using(user.username).filter(product_id=pk)
    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()

    cursor3 = connections[user.username].cursor()
    cursor3.execute('SELECT * FROM `customized_plus` left join multipleplus on customized_plus.mp_number = multipleplus.number WHERE customized_id = %s',[detail_id])
    saverecord3 = cursor3.fetchall()

    plus_js1 = []
    plus_js2 = []
        
    cursor = connections[user.username].cursor()
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name, order_detail.detail_price,order_detail.detail_quantity,product_size.product_size,singleplus_1.name as singleplus_1_name,singleplus_2.name as singleplus_2_name, singleplus_3.name as singleplus_3_name, customized.add_other, product.product_id, product_size.product_price ,order_detail.detail_id,singleplus_1.number as s1_number,singleplus_2.number as s2_number,singleplus_3.number as s3_number FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id left join customized on customized.customized_id = order_detail.customized_id left join singleplus_1 on customized.sp1_number = singleplus_1.number left join singleplus_2 on customized.sp2_number = singleplus_2.number left join singleplus_3 on customized.sp3_number = singleplus_3.number where drink_order.order_id = %s AND order_detail.detail_id = %s  ORDER BY drink_order.order_date ASC',[id,detail_id])
    saverecord = cursor.fetchall()

    cursor1 = connections[user.username].cursor()
    cursor1.execute('SELECT * FROM `Multipleplus`')
    saverecord1 = cursor1.fetchall()

    for plus in saverecord1:
        plus1 = plus[1]
        plus2 = plus[2]
        plus_js1.append(plus1)
        plus_js2.append(plus2)

    if request.method == 'POST':

        selected_total = 0
        select_plus = request.POST.getlist('select_plus')
        plus_new = request.POST.getlist('plus_new')

        x_price=[]
        number=[]
        for selected in select_plus:
            multipleplus = Multipleplus.objects.using(user.username).filter(name=selected)

            for x in multipleplus:
                x_price.append(x.price)
                # selected_total = selected_total+x.price
                number.append(x.number)

        print(x_price)
        print(number)
        y_price=[]
        number_new=[]
        for selected_new in plus_new:
            multipleplus_new = Multipleplus.objects.using(user.username).filter(name=selected_new)

            for y in multipleplus_new:
                y_price.append(y.price)
                # selected_total = selected_total+y_price
                number_new.append(y.number)
        print(y_price)
        print(number_new)        
        p_size = request.POST.get('product_size')
        productsize_id = ProductSize.objects.using(user.username).filter(product_size=p_size,product_id=pk)     
        for p_id in productsize_id:
            size_price = p_id.product_price
            

        ice_name = request.POST.get('ice_name')
        sugar_name = request.POST.get('sugar_name')
        coffeeplus_name = request.POST.get('coffee_plus_name')
        add_other = request.POST.get('add_other')

        singleplus3_id = Singleplus3.objects.using(user.username).filter(number=coffeeplus_name)
        if singleplus3_id:
            for coffeeplus in singleplus3_id:
                coffeeplus_price = coffeeplus.price
        else:
            coffeeplus_price = 0
                
        
        detail_quantity = request.POST.get('detail_quantity')

        customized = Customized.objects.using(user.username).filter(customized_id=detail_id)

        customized.update(sp1_number=ice_name,sp2_number=sugar_name,sp3_number=coffeeplus_name,sp_price=coffeeplus_price,add_other=add_other)

        customized_plus = CustomizedPlus.objects.using(user.username).filter(customized_id=detail_id)

        # customized_plus.update(mp_number=number,customizedplus_price=x_price)

        # q = Multipleplus.objects.using(user.username).get(number=number_new)
        # print(number_new)
        # CustomizedPlus.objects.create(customized_id=detail_id,
        #                        mp_number=Multipleplus.objects.using(user.username).filter(number=number_new).get('number'),
        #                        plus_quantity=1,
        #                        customizedplus_price=y_price)
        
        # total = selected_total + int(detail_quantity)*int(size_price) + coffeeplus_price

        return redirect('/order')

        # cursor4 = connections[user.username].cursor()
        # cursor4.execute('UPDATE `customized` SET `customized_id`=%s,`sp1_number`=%s,`sp2_number`=%s,`sp3_number`=%s,`sp_price`=%s,`add_other`=%s',[detail_id,])
        # saverecord4 = cursor4.fetchall()


    context = {
        'saverecord':saverecord,
        'saverecord1':saverecord1,
        'saverecord3':saverecord3,
        'product_size':product_size,
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'plus_js1':plus_js1,
        'plus_js2':plus_js2,
        'plus':plus,
    } 

    return render(request, 'order_fix.html',context)

@login_required
def editPassword(request):
    user = request.user
    user = User.objects.get(username=user.username)
    
    if request.method == "POST":
        old_password = request.POST.get('old_pd')

        if old_password:
            check = user.check_password(old_password)
            if check == True:
                
                new_password = request.POST.get('new_pd')
                user.set_password(new_password)
                user.save()
                return redirect('/')

    return render(request, 'edit_password.html')

@login_required
def member(request):

    user = request.user
    
    member = Guest.objects.using(user.username).all()

    paginator = Paginator(member,7)

    page = request.GET.get('page')

    member = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        member = Guest.objects.using(user.username).filter(Q(guest_account=search)|Q(guest_name=search)|Q(guest_phone=search))
        
        if not request.GET['search']:
            return redirect('/member')

    context = {
        'member':member,
    }
    return render(request, 'member.html',context)

@login_required
def comment(request):

    user = request.user
    
    comment = Comment.objects.using(user.username).all()

    if 'search' in request.GET:
        search=request.GET['search']
        search = search + ''
        comment = Comment.objects.using(user.username).filter(Q(detail_id=search)|Q(guest_account=search))
        # comment = Comment.objects.all().order_by('detail_id__detail_id')
        # comment = Comment.objects.filter(detail_id = search)
        
        # search=request.GET['search']
        # cursor = connection.cursor()
        # cursor.execute('SELECT `detail_id`, `guest_account`, `comment`, `comment_score` FROM `comment` WHERE detail_id = %s OR guest_account = %s',[search,'search'])
        # comment = cursor.fetchall()
        
        if not request.GET['search']:
            return redirect('/comment')

    return render(request, 'comment.html',{'comment':comment})

@login_required
def ice_plus(request):

    user = request.user
    
    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()
    multipleplus = Multipleplus.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()


    if request.method == 'POST':

        ice_number = request.POST.getlist('ice_number')
        ice_name = request.POST.getlist('ice_name')
        ice_price = request.POST.getlist('ice_price')
        ice_delete = request.POST.getlist('ice_delete')

        for delete in ice_delete:
            cursor2 = connections[user.username].cursor()
            # cursor2.execute('DELETE FROM `singleplus_1` WHERE number = %s',[delete])            
            cursor2.execute('UPDATE `singleplus_1` SET `number`=%s,`hide`=1 WHERE number = %s ',[delete,delete])            

        for x in range(len(ice_number)):
            cursor = connections[user.username].cursor()
            cursor.execute('UPDATE `singleplus_1` SET `name`= %s ,`price`= %s WHERE `number` = %s',[ice_name[x],ice_price[x],ice_number[x]])
            

        plus_name = request.POST.getlist('name')
        price = request.POST.getlist('price')
        for i in range(len(plus_name)):
            if Singleplus1.objects.using(user.username).filter(name=plus_name[i]):
                cursor3 = connections[user.username].cursor()
                cursor3.execute('UPDATE `singleplus_1` SET `name`=%s,`price`=%s,`hide`=0 WHERE name = %s',[plus_name[i],price[i],plus_name[i]])
            else:
                cursor1 = connections[user.username].cursor()
                cursor1.execute('INSERT INTO `singleplus_1`(`name`, `price`) VALUES (%s,%s)',[plus_name[i],price[i]])

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
    }  

    return render(request, 'plus.html',context)
    
@login_required
def sugar_plus(request):

    user = request.user
        
    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()
    multipleplus = Multipleplus.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()

    if request.method == 'POST':

        sugar_number = request.POST.getlist('sugar_number')
        sugar_name = request.POST.getlist('sugar_name')
        sugar_price = request.POST.getlist('sugar_price')
        sugar_delete = request.POST.getlist('sugar_delete')

        for delete in sugar_delete:
            cursor2 = connections[user.username].cursor()
            # cursor.execute('DELETE FROM `singleplus_2` WHERE number = %s',[delete])
            cursor2.execute('UPDATE `singleplus_2` SET `number`= %s,`hide`=1 WHERE number = %s',[delete,delete])


        for x in range(len(sugar_number)):
            cursor = connections[user.username].cursor()
            cursor.execute('UPDATE `singleplus_2` SET `name`= %s ,`price`= %s WHERE `number` = %s',[sugar_name[x],sugar_price[x],sugar_number[x]])


        plus_name = request.POST.getlist('name')
        price = request.POST.getlist('price')
        for i in range(len(plus_name)):
            if Singleplus2.objects.using(user.username).filter(name=plus_name[i]):
                cursor3 = connections[user.username].cursor()
                cursor3.execute('UPDATE `singleplus_2` SET `name`=%s,`price`=%s,`hide`=0 WHERE name = %s',[plus_name[i],price[i],plus_name[i]])
            else:
                cursor1 = connections[user.username].cursor()
                cursor1.execute('INSERT INTO `singleplus_2`(`name`, `price`) VALUES (%s,%s)',[plus_name[i],price[i]])
        

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
    }    
    

    return render(request, 'plus.html',context)

@login_required
def coffee_plus(request):

    user = request.user  

    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()
    multipleplus = Multipleplus.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()

    if request.method == 'POST':

        coffeeplus_number = request.POST.getlist('coffeeplus_number')
        coffeeplus_name = request.POST.getlist('coffeeplus_name')
        coffeeplus_price = request.POST.getlist('coffeeplus_price')
        coffeeplus_delete = request.POST.getlist('coffeeplus_delete')

        for delete in coffeeplus_delete:
            cursor2 = connections[user.username].cursor()
            # cursor2.execute('DELETE FROM `singleplus_3` WHERE number = %s',[delete])
            cursor2.execute('UPDATE `singleplus_3` SET `number`= %s,`hide`=1 WHERE number = %s',[delete,delete])


        for x in range(len(coffeeplus_number)):
            cursor = connections[user.username].cursor()
            cursor.execute('UPDATE `singleplus_3` SET `name`= %s ,`price`= %s WHERE `number` = %s',[coffeeplus_name[x],coffeeplus_price[x],coffeeplus_number[x]])


        plus_name = request.POST.getlist('name')
        price = request.POST.getlist('price')
        for i in range(len(plus_name)):
            if Singleplus3.objects.using(user.username).filter(name=plus_name[i]):
                cursor3 = connections[user.username].cursor()
                cursor3.execute('UPDATE `singleplus_3` SET `name`=%s,`price`=%s,`hide`=0 WHERE name = %s',[plus_name[i],price[i],plus_name[i]])
            else:
                cursor1 = connections[user.username].cursor()
                cursor1.execute('INSERT INTO `singleplus_3`(`name`, `price`) VALUES (%s,%s)',[plus_name[i],price[i]])

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
    }  

    return render(request, 'plus.html',context)

@login_required
def plus(request):

    user = request.user

    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()
    multipleplus = Multipleplus.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()

    if request.method == 'POST':

        plus_number = request.POST.getlist('plus_number')
        plus_name = request.POST.getlist('plus_name')
        plus_price = request.POST.getlist('plus_price')
        plus_delete = request.POST.getlist('plus_delete')

        for delete in plus_delete:
            cursor2 = connections[user.username].cursor()
            # cursor2.execute('DELETE FROM `multipleplus` WHERE number = %s',[delete])
            cursor2.execute('UPDATE `multipleplus` SET `number`= %s,`hide`=1 WHERE number = %s',[delete,delete])
            
        for x in range(len(plus_number)):
            cursor = connections[user.username].cursor()
            cursor.execute('UPDATE `multipleplus` set `name`= %s ,`price`= %s WHERE `number` = %s',[plus_name[x],plus_price[x],plus_number[x]])

        plus_name = request.POST.getlist('name')
        price = request.POST.getlist('price')
        for i in range(len(plus_name)):
            if Multipleplus.objects.using(user.username).filter(name=plus_name[i]):
                cursor3 = connections[user.username].cursor()
                cursor3.execute('UPDATE `multipleplus` SET `name`=%s,`price`=%s,`hide`=0 WHERE name = %s',[plus_name[i],price[i],plus_name[i]])
            else:
                cursor1 = connections[user.username].cursor()
                cursor1.execute('INSERT INTO `multipleplus`(`name`, `price`) VALUES (%s,%s)',[plus_name[i],price[i]])

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
    }  

    return render(request, 'plus.html',context)

@login_required
def product_type(request):

    user = request.user

    singleplus1 = Singleplus1.objects.using(user.username).all()
    singleplus2 = Singleplus2.objects.using(user.username).all()
    singleplus3 = Singleplus3.objects.using(user.username).all()
    multipleplus = Multipleplus.objects.using(user.username).all()
    sort = Sort.objects.using(user.username).all()

    if request.method == 'POST':

        sort_id = request.POST.getlist('producttype_id')
        sort_type = request.POST.getlist('producttype_name')
        sort_delete = request.POST.getlist('producttype_delete')
        
        for delete in sort_delete:
            cursor2 = connections[user.username].cursor()
            # cursor2.execute('DELETE FROM `sort` WHERE sort_id = %s',[delete])
            cursor2.execute('UPDATE `sort` SET `sort_id`= %s,`hide`=1 WHERE sort_id = %s',[delete,delete])

        for x in range(len(sort_type)):
            cursor = connections[user.username].cursor()
            cursor.execute('UPDATE `sort` SET `sort_type`= %s WHERE `sort_id` = %s',[sort_type[x],sort_id[x]])

        plus_name = request.POST.getlist('name')
        for i in range(len(plus_name)):
            if Sort.objects.using(user.username).filter(sort_type=plus_name[i]):
                cursor3 = connections[user.username].cursor()
                cursor3.execute('UPDATE `sort` SET `sort_type`=%s,`hide`=0 WHERE sort_type = %s',[plus_name[i],plus_name[i]])
            else:
                cursor1 = connections[user.username].cursor()
                cursor1.execute('INSERT INTO `sort`(`sort_type`) VALUES (%s)',[plus_name[i]])

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
    }  

    return render(request, 'plus.html',context)

@login_required
def advertise(request):
    
    user = request.user

    if request.method == 'POST':
        
        ad_title = request.POST.get('ad_title')
        ad_photo = request.FILES['ad_photo'] 
        ad_url = request.POST.get('ad_url')
        Advertise.objects.using(user.username).create(title=ad_title,photo=ad_photo,URL=ad_url)

        return redirect('/advertise')

    return render(request, 'advertise.html')

@login_required
def shop_photo(request):
    user = request.user

    if request.method == 'POST':
        shop_photo = request.FILES['shop_photo']
        ShopDetail.objects.filter(shop_name=user.username).update(photo=shop_photo)

    return render(request, 'advertise.html')

@login_required
def banner(request):
    user = request.user
    advertise = Advertise.objects.using(user.username).all()

    if request.method == 'POST':

        if 'edit' in request.POST:
            banner_id = request.POST.getlist('banner_id')
            edit_title = request.POST.getlist('edit_title')
            edit_chosephoto = request.FILES.get('edit_chosephoto')
            edit_URL = request.POST.getlist('edit_URL')
            
        
            for x in range(len(banner_id)):
                print(x)
                
                print(edit_title)
                # if banner_photo == None: 
                    # Advertise.objects.using(user.username).filter(id=edit_id[x]).update(title=edit_title,photo=edit_chosephoto,URL=edit_URL)
                # else:
                    # Advertise.objects.using(user.username).filter(id=banner_id[x]).update(title=banner_title[x],photo=banner_photo[x],URL=banner_URL[x])
        
        banner_delete = request.POST.getlist('banner_delete')
        for d in banner_delete:
            delete = Advertise.objects.using(user.username).get(title=banner_delete[d])
            delete.delete()
    

    context = {
        'advertise':advertise,
    }

    return render(request, 'banner.html',context)