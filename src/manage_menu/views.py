from django.shortcuts import render, redirect
from .models import Customized, OrderDetail, Product, ProductSize,Advertise,TableUnit,ProductCase
from .models import ShopDetail, Sort, Comment, Singleplus1, Singleplus2, Singleplus3, Multipleplus,DrinkOrder,CustomizedPlus,Guest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import connections
from django.contrib.auth.models import User 
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from manage_proj import settings

@login_required
def menu_list(request):
    user = request.user.get_short_name()
    if Product.objects.using(user).filter(hide=0).exists():
        saverecord = Product.objects.using(user).filter(hide=0)
    else:
        saverecord = Product.objects.using(user).all()

    paginator = Paginator(saverecord,10)

    page = request.GET.get('page')

    saverecord = paginator.get_page(page)
    
    if 'search' in request.GET:
        search=request.GET['search']
        saverecord = Product.objects.using(user).filter(Q(product_name__icontains=search)|Q(product_sort__icontains=search)|Q(product_id__icontains=search))
       
        if not request.GET['search']:
            return redirect('/')

    context = {
        'saverecord':saverecord,
        'paginator':paginator,
    }
    return render(request, 'menu_list.html',context)


@login_required
def InsertMenu(request):
    user = request.user.get_short_name()

    productcase = ProductCase.objects.using(user).values_list('product_add', flat=True).order_by('product_add').distinct()
    saverecord_addrule = []
    for case in productcase:
        saverecord_addrule.append(case)

    sort = Sort.objects.using(user).filter(hide=0)

    path = os.path.join("c:/", "xampp/htdocs/images/", user)
    
    if request.method == 'POST':
        p_id = request.POST.get('product_id')
        p_name = request.POST.get('product_name')
        p_sort = request.POST.get('product_sort')
        p_pic = request.FILES['product_pic']       
        p_add = request.POST.get('product_add')
        p_introduction = request.POST.get('product_introduction')

        insert1_index = request.POST.get('insert1_index')
        insert1_size = request.POST.get('insert1_size')
        insert1_price = request.POST.get('insert1_price')

        insert2_index = request.POST.get('insert2_index')
        insert2_size = request.POST.get('insert2_size')
        insert2_price = request.POST.get('insert2_price')

        insert3_index = request.POST.get('insert3_index')
        insert3_size = request.POST.get('insert3_size')
        insert3_price = request.POST.get('insert3_price')
        
        
        if insert1_index != insert2_index and insert2_index != insert3_index and insert1_index != insert3_index:

            try:
                if Product.objects.using(user).filter(product_id=p_id).exists():
                    messages.error(request, '產品ID已存在，請使用其他ID') 
                else:
                    Product.objects.using(user).create(product_id=p_id,product_name=p_name,product_sort=p_sort,product_pic=p_pic,product_add=p_add,product_introduction=p_introduction,hide=0)        
                    fs = FileSystemStorage(location=path)
                    fs.delete(p_pic.name)
                    fs.save(p_pic.name,p_pic)
                if insert1_size and insert1_price:
                    try:
                        # if ProductSize.objects.using(user).filter(product_id=p_id,size=1).exists():
                            ProductSize.objects.using(user).create(product_id=p_id,product_size=insert1_size,product_price=insert1_price,size=insert1_index,hide=0)
                        # else:
                            # messages.error(request, '排序1輸入有錯，請至商品修改處重新輸入')
                    except:
                        messages.error(request, '排序1輸入有錯，請檢查完再送出') 
                if insert2_size and insert2_price:
                    try:
                        if ProductSize.objects.using(user).filter(product_id=p_id,size=1).exists():
                            ProductSize.objects.using(user).create(product_id=p_id,product_size=insert2_size,product_price=insert2_price,size=insert2_index,hide=0)
                        else:
                            messages.error(request, '排序2輸入有錯，請至商品修改處重新輸入')
                    except:
                        messages.error(request, '排序2輸入有錯，請至商品修改處重新輸入')
                if insert3_size and insert3_price:
                    try:                   
                        if ProductSize.objects.using(user).filter(product_id=p_id,size=2).exists():
                            ProductSize.objects.using(user).create(product_id=p_id,product_size=insert3_size,product_price=insert3_price,size=insert3_index,hide=0)
                        else:
                            messages.error(request, '排序3輸入有錯，請至商品修改處重新輸入') 
                    except:
                        messages.error(request, '排序3輸入有錯，請至商品修改處重新輸入') 
            except:
                pass
            #     messages.error(request, '產品輸入有錯，請檢查完再重新送出')  
 
        else:
            messages.error(request, '排序有錯，請檢查完再送出')  


        return redirect('/insertmenu')

    context = {
        'saverecord_addrule':saverecord_addrule,
        'sort':sort,
    }
    return render(request, 'product_Insert.html',context)    

@login_required
def product_manage(request, pk):

    user = request.user.get_short_name() 
    sort = Sort.objects.using(user).all()
    saverecord = Product.objects.using(user).get(pk=pk)
    saverecords = ProductSize.objects.using(user).filter(product_id=pk,hide=0).order_by('size')


    product_size = []
    size_index = []
    productsize_id = []
    productcase = ProductCase.objects.using(user).values_list('product_add', flat=True).order_by('product_add').distinct()
    saverecord_addrule = []
    for case in productcase:
        saverecord_addrule.append(case)

    for x in saverecords:
        
        if len(x.product_size) > 0:
            product_size.append(x.product_size)
        
        productsize_id.append(x.productsize_id)
        size_index.append(x.size)
        
    maxsize=1
    for y in ProductSize.objects.using(user).filter(product_id=pk,hide=0):
        if y:
            maxsize = y.size+1
        else:
            pass
            

    if request.method == 'POST':
        if 'save' in request.POST:
            product_price_get = []
            saverecord.product_id = request.POST.get('product_id')
            saverecord.product_name = request.POST.get('product_name')
            saverecord.product_sort = request.POST.get('product_sort')
        
            if bool(request.FILES.get('product_pic', False)) == True:
                upload_pic = request.FILES['product_pic']
                saverecord.product_pic = upload_pic
            

            saverecord.product_add = request.POST.get('product_add')
            saverecord.product_introduction = request.POST.get('product_introduction')

            product_price_get = request.POST.getlist('product_prices')    

            if len(product_price_get) != len(product_size):
                pass
            
            else:
                cursor = connections[user].cursor()
                for i in range(len(product_size)):
                    cursor.execute('UPDATE product_size SET product_id = %s ,product_size=%s ,product_price=%s WHERE productsize_id=%s',[pk,product_size[i],product_price_get[i],productsize_id[i]])
                             
            saverecord.save()
            
            path = os.path.join("c:/", "xampp/htdocs/images/", user)
            if bool(request.FILES.get('product_pic', False)) == True:
                upload_pic = request.FILES['product_pic']
                fs = FileSystemStorage(location=path)
                fs.delete(upload_pic.name)
                fs.save(upload_pic.name,upload_pic)

            edit_delete = request.POST.getlist('edit_delete')
            for delete in range(len(edit_delete)):     
                ProductSize.objects.using(user).filter(productsize_id=edit_delete[delete]).update(size=0,hide=1) 

            id = []
            for g in ProductSize.objects.using(user).filter(product_id=pk,hide=0):
                id.append(g.productsize_id)
            
            
            for i in range(len(ProductSize.objects.using(user).filter(product_id=pk,hide=0))):               
                ProductSize.objects.using(user).filter(productsize_id=id[i]).update(size=(i+1))
            return redirect('product_manage',pk=pk)

        if 'index' in request.POST:
            edit_index = request.POST.getlist('edit_index')
            edit_name = request.POST.getlist('edit_name')

            if len(set(edit_index))==len(edit_index):
                for x in range(len(edit_index)):
                    ProductSize.objects.using(user).filter(product_size=edit_name[x]).update(size=edit_index[x])
            else:
                messages.error(request, '排序有錯，請檢查完再重新送出')
            return redirect('product_manage',pk=pk)    

        if 'delete' in request.POST:
            Product.objects.using(user).filter(product_id=pk).update(hide=1)
            ProductSize.objects.using(user).filter(product_id=pk).update(hide=1)
            return redirect('/')

        if 'insert' in request.POST:
            new_insertname = request.POST.get('new_insertname')    
            new_insertprice = request.POST.get('new_insertprice')    
            new_insertindex = request.POST.get('new_insertindex')

            if new_insertname and new_insertprice:
                ProductSize.objects.using(user).create(product_id=pk,product_size=new_insertname,product_price=new_insertprice,size=new_insertindex,hide=0)
            else:
                messages.error(request, '請輸入資料後再送出')
            return redirect('product_manage',pk=pk)

        
    context = {
        'saverecord':saverecord,
        'saverecords':saverecords,
        'product_size':product_size,
        'saverecord_addrule':saverecord_addrule,
        'sort':sort,
        'size_index':size_index,
        'maxsize':maxsize,
    }

    return render(request, 'product_manage.html', context)   

@login_required
def product_manage_edit(request, pk, product_size):
    user = request.user.get_short_name()
    saverecords = ProductSize.objects.using(user).filter(product_id=pk,product_size=product_size)
    edit_size = request.POST.get('edit_size')  
    edit_price = request.POST.get('edit_price')  

    if request.method == 'POST':
        ProductSize.objects.using(user).filter(product_id=pk,product_size=product_size).update(product_size=edit_size,product_price=edit_price)
        return redirect('product_manage',pk=pk)
        

    context = {
        'saverecords':saverecords,
        'pk':pk,
    }

    return render(request, 'product_manage_edit.html',context)

@login_required
def order_done(request):

    user = request.user.get_short_name() 
  
    cursor = connections[user].cursor()
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id WHERE drink_order.order_status = %s ORDER BY drink_order.order_date ASC',[1])
    saverecord = cursor.fetchall()

    paginator = Paginator(saverecord,10)
    page = request.GET.get('page')
    saverecord = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        cursor = connections[user].cursor()
        cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id WHERE guest_account = %s AND drink_order.order_status = %s ORDER BY drink_order.order_date ASC',[search,1])
        saverecord = cursor.fetchall()
               
        if not request.GET['search']:
            return redirect('/order_done')
    
    context = {
        'saverecord':saverecord,
        'paginator':paginator,
    }
    return render(request, 'order_done.html',context)

@login_required
def order(request):
    user = request.user.get_short_name() 
  
    cursor = connections[user].cursor()
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id WHERE drink_order.order_status = %s ORDER BY drink_order.order_date ASC',[0])
    saverecord = cursor.fetchall()
    print(saverecord)

    paginator = Paginator(saverecord,10)
    page = request.GET.get('page')
    saverecord = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        cursor = connections[user].cursor()
        cursor.execute('SELECT DISTINCT drink_order.*,product.product_name,order_detail.detail_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id  WHERE guest_account = %s AND drink_order.order_status = %s ORDER BY drink_order.order_date ASC',[search,0])
        saverecord = cursor.fetchall()
               
        if not request.GET['search']:
            return redirect('/order')
    
    context = {
        'saverecord':saverecord,
        'paginator':paginator,
    }

    return render(request, 'order.html',context)

@login_required
def order_manage(request,id,detail_id):

    user = request.user.get_short_name()
    
    cursor = connections[user].cursor()   
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name, order_detail.detail_id, order_detail.detail_price,order_detail.detail_quantity,product_size.product_size,singleplus_1.name ,singleplus_2.name, singleplus_3.name, customized.add_other, product.product_id FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id left join customized on customized.customized_id = order_detail.customized_id left join singleplus_1 on customized.sp1_number = singleplus_1.number left join singleplus_2 on customized.sp2_number = singleplus_2.number left join singleplus_3 on customized.sp3_number = singleplus_3.number where drink_order.order_id = %s and order_detail.detail_id = %s ORDER BY drink_order.order_date ASC',[id,detail_id])
    saverecord = cursor.fetchall()

    cursor1 = connections[user].cursor()
    cursor1.execute('SELECT multipleplus.name,multipleplus.price,customized_plus.plus_quantity FROM drink_order inner join order_detail on drink_order.order_id = order_detail.order_id left join customized on customized.customized_id = order_detail.customized_id inner join customized_plus on customized.customized_id = customized_plus.customized_id inner join multipleplus on customized_plus.mp_number = multipleplus.number where drink_order.order_id = %s AND customized_plus.customized_id = %s',[id,detail_id])
    saverecord1 = cursor1.fetchall()

    for i in saverecord:
        order_URL = '/order_manage/'+str(i[0])+'/'+str(i[5])
        order_fix_URL = '/order_manage/order_fix/'+str(i[5])+'/'+str(i[0])+'/'+str(i[13])
        request.session['order_URL'] = order_URL
        request.session['order_fix_URL'] = order_fix_URL

    context = {
        'saverecord':saverecord,
        'saverecord1':saverecord1,

    }

    return render(request, 'order_manage.html',context)

@login_required
def order_fix(request,detail_id,id,pk):

    user = request.user.get_short_name()
    order_URL = request.session.get('order_URL')
    order_fix_URL = request.session.get('order_fix_URL')
    product_size = ProductSize.objects.using(user).filter(product_id=pk)
    singleplus1 = Singleplus1.objects.using(user).filter(hide=0)
    singleplus2 = Singleplus2.objects.using(user).filter(hide=0)
    singleplus3 = Singleplus3.objects.using(user).filter(hide=0)

    cursor3 = connections[user].cursor()
    cursor3.execute('SELECT * FROM `customized_plus` left join multipleplus on customized_plus.mp_number = multipleplus.number WHERE customized_id = %s',[detail_id])
    saverecord3 = cursor3.fetchall()

    plus_js1 = []
    plus_js2 = []
        
    cursor = connections[user].cursor()
    cursor.execute('SELECT DISTINCT drink_order.*,product.product_name, order_detail.detail_price,order_detail.detail_quantity,product_size.product_size,singleplus_1.name as singleplus_1_name,singleplus_2.name as singleplus_2_name, singleplus_3.name as singleplus_3_name, customized.add_other, product.product_id, product_size.product_price ,order_detail.detail_id,singleplus_1.number as s1_number,singleplus_2.number as s2_number,singleplus_3.number as s3_number FROM drink_order left join order_detail on drink_order.order_id = order_detail.order_id left join product_size on product_size.productsize_id = order_detail.productsize_id left join product on product.product_id = product_size.product_id left join customized on customized.customized_id = order_detail.customized_id left join singleplus_1 on customized.sp1_number = singleplus_1.number left join singleplus_2 on customized.sp2_number = singleplus_2.number left join singleplus_3 on customized.sp3_number = singleplus_3.number where drink_order.order_id = %s AND order_detail.detail_id = %s  ORDER BY drink_order.order_date ASC',[id,detail_id])
    saverecord = cursor.fetchall()

    cursor1 = connections[user].cursor()
    cursor1.execute('SELECT * FROM `Multipleplus`')
    saverecord1 = cursor1.fetchall()

    for plus in saverecord1:
        plus1 = plus[1]
        plus2 = plus[2]
        plus_js1.append(plus1)
        plus_js2.append(plus2)
    
    if request.method == 'POST':
       
        plus_new = request.POST.getlist('plus_new')
        select_plus_quantity = request.POST.getlist('select_plus_quantity')   #調整配料的quantity
        select_plus_quantity_new = request.POST.getlist('select_plus_quantity_new')  
        
        x_price=[] #調整配料的價格
        number=[]  #調整配料的number
        select_plus = request.POST.getlist('select_plus')
        
        for selected in select_plus:
            multipleplus = Multipleplus.objects.using(user).filter(name=selected)
                     
            for x in multipleplus:
                
                x_price.append(x.price)                
                number.append(x.number)       

        # selected_total = 0    
        # for y in range(len(select_plus_quantity)):      
        #     selected_total += int(x_price[y])*int(select_plus_quantity[y])


        y_price=[]        #新增的調整配料的價格
        number_new=[]     #新增的調整配料的number      
        for selected_new in plus_new:
            multipleplus_new = Multipleplus.objects.using(user).filter(name=selected_new)

            for y in multipleplus_new:
                y_price.append(y.price)
                number_new.append(y.number)

        
        p_size = request.POST.get('product_size')  #飲料的大小
        
        productsize_id = ProductSize.objects.using(user).filter(product_size=p_size,product_id=pk)     
        for p_id in productsize_id:
            size_price = p_id.product_price
            size = p_id.productsize_id
        
        OrderDetail.objects.using(user).filter(detail_id=detail_id).update(productsize_id=size)

        ice_name = request.POST.get('ice_name')
        sugar_name = request.POST.get('sugar_name')
        coffeeplus_name = request.POST.get('coffee_plus_name')
        add_other = request.POST.get('add_other')

        singleplus3_id = Singleplus3.objects.using(user).filter(number=coffeeplus_name)
        if singleplus3_id:
            for coffeeplus in singleplus3_id:
                coffeeplus_price = coffeeplus.price
        else:
            coffeeplus_price = 0
                
        
        detail_quantity = request.POST.get('detail_quantity')

        customized = Customized.objects.using(user).filter(customized_id=detail_id)

        customized.update(sp1_number=ice_name,sp2_number=sugar_name,sp3_number=coffeeplus_name,sp_price=coffeeplus_price,add_other=add_other)
        
        customized_plus = CustomizedPlus.objects.using(user).filter(customized_id__in=detail_id)    
        
        origin_customized_plus_number = []

        for origin_customized_plus in customized_plus:
            origin_customized_plus_number.append(origin_customized_plus.mp_number)

        
        for x in range(len(origin_customized_plus_number)):
            origin_price = x_price[x]
            origin_quantity = select_plus_quantity[x]
            origin_total = int(origin_price)*int(origin_quantity)

            if len(set(number)-set(number_new))==len(number):
                customized_plus.filter(mp_number=origin_customized_plus_number[x]).update(mp_number=number[x],customizedplus_price=origin_total,plus_quantity=select_plus_quantity[x])
        
        for x in range(len(number_new)):
            new_price = y_price[x]
            new_quantity = select_plus_quantity_new[x]
            new_total = int(new_price)*int(new_quantity)
            if len(set(number)-set(number_new))==len(number):
                CustomizedPlus.objects.using(user).create(customized_id=detail_id,
                                    mp_number=Multipleplus.objects.using(user).get(number=number_new[x]),
                                    plus_quantity=select_plus_quantity_new[x],
                                    customizedplus_price=new_total)                       
            else:
                messages.error(request, '加料商品有誤，請重新選擇')
                return redirect(order_fix_URL)

        select_delete = request.POST.getlist('select_delete')
        delete_price = []
        delete_number = []
        for x in range(len(select_delete)):
            m_number = Multipleplus.objects.using(user).filter(name=select_delete[x])
            for number in m_number:
                delete_number.append(number.number)
                delete_price.append(number.price)                      
            CustomizedPlus.objects.using(user).filter(customized_id=detail_id,mp_number=delete_number[x]).delete()
        select_price = 0

        for customid in CustomizedPlus.objects.using(user).filter(customized_id__in=detail_id):
            select_price += customid.customizedplus_price
        
        total = select_price + int(detail_quantity)*int(size_price) + coffeeplus_price
        OrderDetail.objects.using(user).filter(detail_id=detail_id).update(detail_quantity=detail_quantity,detail_price=total)
        return redirect(order_URL)


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
    user = request.user.get_short_name()
    user = User.objects.get(username=user)
    
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
    
    member = Guest.objects.all()

    paginator = Paginator(member,10)

    page = request.GET.get('page')

    member = paginator.get_page(page)

    if 'search' in request.GET:
        search=request.GET['search']
        member = Guest.objects.filter(Q(guest_account=search)|Q(guest_name=search)|Q(guest_phone=search))
        
        if not request.GET['search']:
            return redirect('/member')

    context = {
        'member':member,
        'paginator':paginator
    }
    return render(request, 'member.html',context)

@login_required
def comment(request):

    # saverecord = []

    user = request.user.get_short_name()

    # comment = Comment.objects.using(user).all()
    cursor = connections[user].cursor()
    cursor.execute('SELECT order_detail.order_id, comment.*, drink_order.order_status FROM comment JOIN order_detail ON comment.detail_id = order_detail.detail_id JOIN drink_order on drink_order.order_id = order_detail.order_id WHERE drink_order.order_status = %s',[1])
    comment = cursor.fetchall()

    paginator = Paginator(comment,10)

    page = request.GET.get('page')

    comment = paginator.get_page(page)

    


    if 'search' in request.GET:
        search=request.GET['search']
        if (search != ''):
            # comment = Comment.objects.using(user).filter(Q(detail__detail_id=search))
            comment = Comment.objects.using(user).filter(guest_account = search)

        else:
            return redirect('/comment')
                 

    context = {
        'comment':comment,
        'paginator':paginator,
    }

    return render(request, 'comment.html', context)

@login_required
def plus(request):

    user = request.user.get_short_name()
    
    tableunit = TableUnit.objects.using(user).all()
    singleplus1 = Singleplus1.objects.using(user).all()
    singleplus2 = Singleplus2.objects.using(user).all()
    singleplus3 = Singleplus3.objects.using(user).all()
    multipleplus = Multipleplus.objects.using(user).all()
    sort = Sort.objects.using(user).all()

    cursor = connections[user].cursor()
    cursor.execute('SELECT product_add ,GROUP_CONCAT(product_case.plus_id ORDER BY product_case.plus_id) AS plus_id, GROUP_CONCAT(table_unit.Unit) AS plus_id_cn,hide\
                    FROM product_case \
                    INNER JOIN table_unit ON product_case.plus_id = table_unit.ID\
                    GROUP BY product_case.product_add')

    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)
     

    context = {
        'singleplus1':singleplus1,
        'singleplus2':singleplus2,
        'singleplus3':singleplus3,
        'multipleplus':multipleplus,
        'sort':sort,
        'unit_name':unit_name,
        'cursor':cursor,

    }
    return render(request,'plus.html',context)


@login_required
def singleplus1(request):

    user = request.user.get_short_name()
    singleplus1 = Singleplus1.objects.using(user).all()  
    

    if request.method == 'POST':

        ice_delete = request.POST.getlist('ice_delete')

        for delete in ice_delete:
            Singleplus1.objects.using(user).filter(number=delete).update(hide=1)       
            
        new_single1name = request.POST.get('new_single1name')
        new_single1price = request.POST.get('new_single1price')

        if 'insert_single1' in request.POST:
            single1_name = request.POST.get('single1_name')
            if new_single1name and new_single1price:
                if Singleplus1.objects.using(user).filter(name=new_single1name,hide=0):
                    messages.error(request, '名稱與現有名稱相同，請修改')
                else:
                    Singleplus1.objects.using(user).create(name=new_single1name,price=new_single1price,hide=0)
            else:
                error = '請輸入'+single1_name+'完整資料後再送出'
                messages.error(request, error) 

        if 'send' in request.POST:
            single1_name = request.POST.get('single1_name')
            TableUnit.objects.using(user).filter(id=1).update(unit=single1_name)

        return redirect('/plus')

    context = {
        'singleplus1':singleplus1,
    }  

    return render(request, 'plus.html',context)

@login_required
def singleplus1_edit(request,pk):

    user = request.user.get_short_name()
    singleplus1 = Singleplus1.objects.using(user).filter(number=pk)

    tableunit = TableUnit.objects.using(user).all()
    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)

    if request.method == 'POST':
        edit_single1name = request.POST.get('edit_single1name')
        edit_single1price = request.POST.get('edit_single1price')
        if edit_single1name and edit_single1price:
            Singleplus1.objects.using(user).filter(number=pk).update(name=edit_single1name,price=edit_single1price)
        else:
            messages.error(request, '請輸入完整資料後再送出')
            return redirect('singleplus1_edit',pk=pk)
        return redirect('/plus')

    context = {
        'singleplus1':singleplus1,
        'unit_name':unit_name
    } 

    return render(request,'singleplus1_edit.html',context)

@login_required
def singleplus2(request):

    user = request.user.get_short_name()
    singleplus2 = Singleplus2.objects.using(user).all()  
    
    if request.method == 'POST':

        single2_delete = request.POST.getlist('single2_delete')

        for delete in single2_delete:
            Singleplus2.objects.using(user).filter(number=delete).update(hide=1)       
            
        new_single2name = request.POST.get('new_single2name')
        new_single2price = request.POST.get('new_single2price')

        if 'insert_single2' in request.POST:
            single2_name = request.POST.get('single2_name')
            if new_single2name and new_single2name:
                if Singleplus2.objects.using(user).filter(name=new_single2name,hide=0):
                    messages.error(request, '名稱與現有名稱相同，請修改')
                else:
                    Singleplus2.objects.using(user).create(name=new_single2name,price=new_single2price,hide=0)
            else:
                error = '請輸入'+single2_name+'完整資料後再送出'
                messages.error(request, error)

        if 'send' in request.POST:
            single2_name = request.POST.get('single2_name')
            TableUnit.objects.using(user).filter(id=2).update(unit=single2_name)

        return redirect('/plus')
        

    context = {
        'singleplus2':singleplus2,
    }    
    

    return render(request, 'plus.html',context)

@login_required
def singleplus2_edit(request,pk):

    user = request.user.get_short_name()
    singleplus2 = Singleplus2.objects.using(user).filter(number=pk)

    tableunit = TableUnit.objects.using(user).all()
    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)

    if request.method == 'POST':
        edit_single2name = request.POST.get('edit_single2name')
        edit_single2price = request.POST.get('edit_single2price')
        if edit_single2name and edit_single2price:
            Singleplus2.objects.using(user).filter(number=pk).update(name=edit_single2name,price=edit_single2price)
        else:
            messages.error(request, '請輸入完整資料後再送出')
            return redirect('singleplus2_edit',pk=pk)
        
        return redirect('/plus')

    context = {
        'singleplus2':singleplus2,
        'unit_name':unit_name
    } 

    return render(request,'singleplus2_edit.html',context)


@login_required
def singleplus3(request):

    user = request.user.get_short_name()
    singleplus3 = Singleplus3.objects.using(user).all()  
    
    if request.method == 'POST':

        single3_delete = request.POST.getlist('single3_delete')

        for delete in single3_delete:
            Singleplus3.objects.using(user).filter(number=delete).update(hide=1)       
            
        new_single3name = request.POST.get('new_single3name')
        new_single3price = request.POST.get('new_single3price')

        if 'insert_single3' in request.POST:
            single3_name = request.POST.get('single3_name')
            if new_single3name and new_single3price:
                if Singleplus3.objects.using(user).filter(name=new_single3name,hide=0):
                    messages.error(request, '名稱與現有名稱相同，請修改')
                else:
                    Singleplus3.objects.using(user).create(name=new_single3name,price=new_single3price,hide=0)
            else:
                error = '請輸入'+single3_name+'完整資料後再送出'
                messages.error(request, error)
        if 'send' in request.POST:
            single3_name = request.POST.get('single3_name')
            TableUnit.objects.using(user).filter(id=3).update(unit=single3_name)

        return redirect('/plus')
        

    context = {
        'singleplus3':singleplus3,
    }    
    

    return render(request, 'plus.html',context)

@login_required
def singleplus3_edit(request,pk):

    user = request.user.get_short_name()
    singleplus3 = Singleplus3.objects.using(user).filter(number=pk)

    tableunit = TableUnit.objects.using(user).all()
    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)

    if request.method == 'POST':
        edit_single3name = request.POST.get('edit_single3name')
        edit_single3price = request.POST.get('edit_single3price')
        
        if edit_single3name and edit_single3price:
            Singleplus3.objects.using(user).filter(number=pk).update(name=edit_single3name,price=edit_single3price)
        else:
            messages.error(request, '請輸入完整資料後再送出')
            return redirect('singleplus3_edit',pk=pk)

        return redirect('/plus')

    context = {
        'singleplus3':singleplus3,
        'unit_name':unit_name
    } 

    return render(request,'singleplus3_edit.html',context)

@login_required
def multi_plus(request):

    user = request.user.get_short_name()

    multipleplus = Multipleplus.objects.using(user).all()
    if request.method == 'POST':

        multi_delete = request.POST.getlist('multi_delete')

        for delete in multi_delete:
            Multipleplus.objects.using(user).filter(number=delete).update(hide=1)       
            
        new_multiname = request.POST.get('new_multiname')
        new_multiprice = request.POST.get('new_multiprice')

        if 'insert_multi' in request.POST:
            multiplus_name = request.POST.get('multiplus_name')
            if new_multiname and new_multiprice:
                if Multipleplus.objects.using(user).filter(name=new_multiname,hide=0):
                    messages.error(request, '名稱與現有名稱相同，請修改')
                else:
                    Multipleplus.objects.using(user).create(name=new_multiname,price=new_multiprice,hide=0)
            else:
                error = '請輸入'+multiplus_name+'完整資料後再送出'
                messages.error(request, error)
        if 'send' in request.POST:
            multiplus_name = request.POST.get('multiplus_name')
            TableUnit.objects.using(user).filter(id=4).update(unit=multiplus_name)    

        return redirect('/plus')

    context = {
        'multipleplus':multipleplus,
    }  

    return render(request, 'plus.html',context)

@login_required
def multi_plus_edit(request,pk):

    user = request.user.get_short_name()
    multipleplus = Multipleplus.objects.using(user).filter(number=pk)

    tableunit = TableUnit.objects.using(user).all()
    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)

    if request.method == 'POST':
        edit_multiname = request.POST.get('edit_multiname')
        edit_multiprice = request.POST.get('edit_multiprice')
        if edit_multiname and edit_multiprice:
            Multipleplus.objects.using(user).filter(number=pk).update(name=edit_multiname,price=edit_multiprice)
        else:
            messages.error(request, '請輸入完整資料後再送出')
            return redirect('singleplus3_edit',pk=pk)
        

        return redirect('/plus')

    context = {
        'multipleplus':multipleplus,
        'unit_name':unit_name
    } 

    return render(request,'multiplus_edit.html',context)

@login_required
def product_type(request):

    user = request.user.get_short_name()
    sort = Sort.objects.using(user).all()
    if request.method == 'POST':

        producttype_delete = request.POST.getlist('producttype_delete')

        for delete in producttype_delete:
            Sort.objects.using(user).filter(sort_id=delete).update(hide=1)       

        
        if 'insert_sort' in request.POST:
            new_sortname = request.POST.get('new_sortname')
            # new_sortpic = request.FILES['new_sortpic']

            if new_sortname:
                if Sort.objects.using(user).filter(sort_type=new_sortname,hide=0):
                    messages.error(request, '名稱與現有名稱相同，請修改')
                else:
                    if bool(request.FILES.get('new_sortpic', False)):
                        new_sortpic = request.FILES['new_sortpic']
                        Sort.objects.using(user).create(sort_type=new_sortname, photo = new_sortpic, hide=0)
                        path = os.path.join("c:/", "xampp/htdocs/images/", user+"/","SortPic")
                        fs = FileSystemStorage(location=path)
                        fs.delete(new_sortpic.name)
                        fs.save(new_sortpic.name,new_sortpic)
                    else:
                        messages.error(request, '未選擇檔案，請修改')
            else:
                error = '請輸入'+new_sortname+'完整資料後再送出'
                messages.error(request, error) 

        return redirect('/plus')

    context = {
        'sort':sort,
    }  

    return render(request, 'plus.html',context)

@login_required
def product_type_edit(request,pk):

    user = request.user.get_short_name()
    sort = Sort.objects.using(user).filter(sort_id=pk)

    tableunit = TableUnit.objects.using(user).all()
    unit_name=[]
    for tu in tableunit:
        unit_name.append(tu.unit)

    if request.method == 'POST':
        edit_sorttype = request.POST.get('edit_sorttype')

        if bool(request.FILES.get('edit_photo', False)) == True:               
            edit_photo = request.FILES['edit_photo']
            photo = edit_photo.name
            Sort.objects.using(user).filter(sort_id=pk).update(photo=photo,sort_type=edit_sorttype)
        else:
            Sort.objects.using(user).filter(sort_id=pk).update(sort_type=edit_sorttype)

        return redirect('/plus')

    context = {
        'sort':sort,
        'unit_name':unit_name
    } 

    return render(request, 'product_type_edit.html',context)

@login_required
def product_case(request):

    user = request.user.get_short_name()

    if request.method == 'POST':
        
        product_addrule_delete = request.POST.getlist('product_addrule_delete')
        for addrule_delete in product_addrule_delete:
            ProductCase.objects.using(user).filter(product_add=addrule_delete).update(hide=1)

        if 'product_addrule_return' in request.POST:
            product_addrule_return = request.POST.get('product_addrule_return')
            ProductCase.objects.using(user).filter(product_add=product_addrule_return).update(hide=0)

        if 'insert' in request.POST:
            new_addrule = request.POST.get('new_addrule')
            new_check = request.POST.getlist('new_check')
            list4cn = []
            if new_addrule:
                if ProductCase.objects.using(user).filter(product_add=new_addrule):
                    messages.error(request, '規則名稱已重複，請修改')
                else:
                    for cn_list in new_check:
                        cn = TableUnit.objects.using(user).filter(unit=cn_list)
                        for cnn in cn:
                            list4cn.append(cnn.id)       
                    
                    if ProductCase.objects.using(user).filter(product_add=new_addrule):
                        messages.error(request, '命名重複，請修改命名')  
                    else:
                        for x in range(len(list4cn)):
                            ProductCase.objects.using(user).create(product_add=new_addrule,plus_id=list4cn[x],hide=0)
            else:
                messages.error(request, '請輸入完整資料後再送出')

        return redirect('/plus')

    return render(request, 'plus.html')

@login_required
def product_case_edit(request,product_case):
    user = request.user.get_short_name()

    tableunit = TableUnit.objects.using(user).all()
    add_cn=[]
    for tu in tableunit:
        add_cn.append(tu.unit)


    unit_name = connections[user].cursor()
    unit_name.execute('SELECT product_add ,GROUP_CONCAT(product_case.plus_id ORDER BY product_case.plus_id) AS plus_id, GROUP_CONCAT(table_unit.Unit) AS plus_id_cn\
                    FROM product_case \
                    INNER JOIN table_unit ON product_case.plus_id = table_unit.ID WHERE product_add = %s \
                    GROUP BY product_case.product_add',[product_case])

    if request.method == 'POST':
        product_addrule_edit = request.POST.get('product_addrule_edit')
        product_addrule_cn = request.POST.getlist('product_addrule_cn')

        list4cn = []
        for cn_list in product_addrule_cn:
            cn = TableUnit.objects.using(user).filter(unit=cn_list)
            for cnn in cn:
                list4cn.append(cnn.id)

        ProductCase.objects.using(user).filter(product_add=product_addrule_edit).delete()
        for x in range(len(list4cn)):
            ProductCase.objects.using(user).create(product_add=product_addrule_edit,plus_id=list4cn[x],hide=0)

        return redirect('/plus')

    context = {
        'add_cn':add_cn,
        'unit_name':unit_name
    }

    return render(request, 'product_case_edit.html',context)

@login_required
def advertise(request):
    
    user = request.user.get_short_name()
    advertise = Advertise.objects.using(user).all()
    ad_length = []
    for ad in advertise:
        ad_length.append(ad)
        
    if request.method == 'POST':
        
        ad_title = request.POST.get('ad_title')
        ad_photo = request.FILES['ad_photo'] 
        ad_url = request.POST.get('ad_url')
                
        if len(ad_length) >= 5:
            messages.error(request, '限制最多只能5個，請刪除舊有選項以新增!')  
        else:
            Advertise.objects.using(user).create(title=ad_title,photo=ad_photo,URL=ad_url)
            fs = FileSystemStorage(location=('C:\\xampp\\htdocs\\images\\'+user+'\\AdvertisePhoto'))
            fs.save(ad_photo.name,ad_photo)

        return redirect('/advertise')

    return render(request, 'advertise.html')

@login_required
def shop_photo(request):
    user = request.user.get_short_name()

    if request.method == 'POST':
        shop_photo = request.FILES['shop_photo']
        ShopDetail.objects.filter(shop_name=user).update(photo=shop_photo)

    return render(request, 'advertise.html')

@login_required
def banner(request):
    user = request.user.get_short_name()
    advertise = Advertise.objects.using(user).all()

    if request.method == 'POST':

        banner_delete = request.POST.getlist('banner_delete')

        for d in banner_delete:
            delete = Advertise.objects.using(user).get(id=d)
            delete.delete()
    

    context = {
        'advertise':advertise,
    }

    return render(request, 'banner.html',context)

@login_required
def edit_banner(request,pk):

    user = request.user.get_short_name()
    advertise = Advertise.objects.using(user).filter(id=pk)

    if request.method == 'POST':
            edit_title = request.POST.get('edit_title')
            edit_photo = request.FILES.get('edit_photo')
            edit_URL = request.POST.get('edit_URL')

            if edit_photo != None:
                Advertise.objects.using(user).filter(id=pk).update(title=edit_title,photo=edit_photo,URL=edit_URL) 
                return redirect('/banner')
            else:
                Advertise.objects.using(user).filter(id=pk).update(title=edit_title,URL=edit_URL) 
                return redirect('/banner')

    context={
        'advertise':advertise,
    }

    return render(request,'edit_banner.html',context)

@login_required
def create_staff(request):
    db_ID = request.user.get_short_name()
    if request.method == "POST":
        account = request.POST.get('account')
        password = request.POST.get('password')
        User.objects.create_user(username=account,email=None,password=password,is_superuser=1,first_name=db_ID,is_staff=0,is_active=1,date_joined=datetime.now())
    return render(request,'create_staff.html')

@login_required
def delete_store(request):
    user = request.user.get_short_name()
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            print('hello')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                database_id = user #just something unique
                newDatabase = {}
                newDatabase["id"] = database_id
                newDatabase['ENGINE'] = 'django.db.backends.mysql'
                newDatabase['NAME'] = database_id
                newDatabase['USER'] = 'root'
                newDatabase['PASSWORD'] = ''
                newDatabase['HOST'] = 'localhost'
                newDatabase['PORT'] = '3306'
                settings.DATABASES[database_id] = newDatabase

                if request.GET.get('next'):
                    
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/')
        
        cursor = connections[user].cursor()
        cursor.execute('drop database %s;',[user])
    
    return render(request,'delete_store.html')
