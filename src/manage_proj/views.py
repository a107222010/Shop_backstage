from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from manage_proj import settings
from django.contrib.auth.models import User
from datetime import datetime
from manage_menu.models import ShopDetail,AuthUser
from django.db import connection

def page_not_found_view(request,exception):
    return render(request, '404.html', status=404)

def page_error(request):
    return render(request, '500.html', status=500)

def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):

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
                database_id = user.username #just something unique
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


    return render(request,'login.html',{'form':form})

def sign_up(request):
    if request.method == "POST":
        account = request.POST.get('shop_account')
        password = request.POST.get('shop_password')
        e_mail = request.POST.get('shop_e_mail')
        shop_name = request.POST.get('shop_name')
        shop_phone = request.POST.get('shop_phone')
        shop_admin = request.POST.get('shop_admin')

        user = User.objects.create_user(username=account,email=e_mail,password=password,is_superuser=1,is_staff=1,is_active=1,date_joined=datetime.now())
        ShopDetail.objects.create(shop_chinese=shop_name,shop_name=account,shop_phone=shop_phone,shop_admin=shop_admin)
        
        if user:
            cursor = connection.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;' % account )
            cursor.execute('USE %s; \
            CREATE TABLE `auth_group` (\
            `id` int(11) NOT NULL,\
            `name` varchar(150) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `auth_group_permissions` (\
            `id` int(11) NOT NULL,\
            `group_id` int(11) NOT NULL,\
            `permission_id` int(11) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `auth_permission` (\
            `id` int(11) NOT NULL,\
            `name` varchar(255) NOT NULL,\
            `content_type_id` int(11) NOT NULL,\
            `codename` varchar(100) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES \
            (1, "Can add log entry", 1, "add_logentry"),\
            (2, "Can change log entry", 1, "change_logentry"),\
            (3, "Can delete log entry", 1, "delete_logentry"),\
            (4, "Can view log entry", 1, "view_logentry"),\
            (5, "Can add permission", 2, "add_permission"),\
            (6, "Can change permission", 2, "change_permission"),\
            (7, "Can delete permission", 2, "delete_permission"),\
            (8, "Can view permission", 2, "view_permission"),\
            (9, "Can add group", 3, "add_group"),\
            (10, "Can change group", 3, "change_group"),\
            (11, "Can delete group", 3, "delete_group"),\
            (12, "Can view group", 3, "view_group"),\
            (13, "Can add user", 4, "add_user"),\
            (14, "Can change user", 4, "change_user"),\
            (15, "Can delete user", 4, "delete_user"),\
            (16, "Can view user", 4, "view_user"),\
            (17, "Can add content type", 5, "add_contenttype"),\
            (18, "Can change content type", 5, "change_contenttype"),\
            (19, "Can delete content type", 5, "delete_contenttype"),\
            (20, "Can view content type", 5, "view_contenttype"),\
            (21, "Can add session", 6, "add_session"),\
            (22, "Can change session", 6, "change_session"),\
            (23, "Can delete session", 6, "delete_session"),\
            (24, "Can view session", 6, "view_session"),\
            (25, "Can add auth group", 7, "add_authgroup"),\
            (26, "Can change auth group", 7, "change_authgroup"),\
            (27, "Can delete auth group", 7, "delete_authgroup"),\
            (28, "Can view auth group", 7, "view_authgroup"),\
            (29, "Can add auth group permissions", 8, "add_authgrouppermissions"),\
            (30, "Can change auth group permissions", 8, "change_authgrouppermissions"),\
            (31, "Can delete auth group permissions", 8, "delete_authgrouppermissions"),\
            (32, "Can view auth group permissions", 8, "view_authgrouppermissions"),\
            (33, "Can add auth permission", 9, "add_authpermission"),\
            (34, "Can change auth permission", 9, "change_authpermission"),\
            (35, "Can delete auth permission", 9, "delete_authpermission"),\
            (36, "Can view auth permission", 9, "view_authpermission"),\
            (37, "Can add auth user", 10, "add_authuser"),\
            (38, "Can change auth user", 10, "change_authuser"),\
            (39, "Can delete auth user", 10, "delete_authuser"),\
            (40, "Can view auth user", 10, "view_authuser"),\
            (41, "Can add auth user groups", 11, "add_authusergroups"),\
            (42, "Can change auth user groups", 11, "change_authusergroups"),\
            (43, "Can delete auth user groups", 11, "delete_authusergroups"),\
            (44, "Can view auth user groups", 11, "view_authusergroups"),\
            (45, "Can add auth user user permissions", 12, "add_authuseruserpermissions"),\
            (46, "Can change auth user user permissions", 12, "change_authuseruserpermissions"),\
            (47, "Can delete auth user user permissions", 12, "delete_authuseruserpermissions"),\
            (48, "Can view auth user user permissions", 12, "view_authuseruserpermissions"),\
            (49, "Can add customized", 13, "add_customized"),\
            (50, "Can change customized", 13, "change_customized"),\
            (51, "Can delete customized", 13, "delete_customized"),\
            (52, "Can view customized", 13, "view_customized"),\
            (53, "Can add django admin log", 14, "add_djangoadminlog"),\
            (54, "Can change django admin log", 14, "change_djangoadminlog"),\
            (55, "Can delete django admin log", 14, "delete_djangoadminlog"),\
            (56, "Can view django admin log", 14, "view_djangoadminlog"),\
            (57, "Can add django content type", 15, "add_djangocontenttype"),\
            (58, "Can change django content type", 15, "change_djangocontenttype"),\
            (59, "Can delete django content type", 15, "delete_djangocontenttype"),\
            (60, "Can view django content type", 15, "view_djangocontenttype"),\
            (61, "Can add django migrations", 16, "add_djangomigrations"),\
            (62, "Can change django migrations", 16, "change_djangomigrations"),\
            (63, "Can delete django migrations", 16, "delete_djangomigrations"),\
            (64, "Can view django migrations", 16, "view_djangomigrations"),\
            (65, "Can add django session", 17, "add_djangosession"),\
            (66, "Can change django session", 17, "change_djangosession"),\
            (67, "Can delete django session", 17, "delete_djangosession"),\
            (68, "Can view django session", 17, "view_djangosession"),\
            (69, "Can add drink order", 18, "add_drinkorder"),\
            (70, "Can change drink order", 18, "change_drinkorder"),\
            (71, "Can delete drink order", 18, "delete_drinkorder"),\
            (72, "Can view drink order", 18, "view_drinkorder"),\
            (73, "Can add guest", 19, "add_guest"),\
            (74, "Can change guest", 19, "change_guest"),\
            (75, "Can delete guest", 19, "delete_guest"),\
            (76, "Can view guest", 19, "view_guest"),\
            (77, "Can add multipleplus", 20, "add_multipleplus"),\
            (78, "Can change multipleplus", 20, "change_multipleplus"),\
            (79, "Can delete multipleplus", 20, "delete_multipleplus"),\
            (80, "Can view multipleplus", 20, "view_multipleplus"),\
            (81, "Can add order detail", 21, "add_orderdetail"),\
            (82, "Can change order detail", 21, "change_orderdetail"),\
            (83, "Can delete order detail", 21, "delete_orderdetail"),\
            (84, "Can view order detail", 21, "view_orderdetail"),\
            (85, "Can add product", 22, "add_product"),\
            (86, "Can change product", 22, "change_product"),\
            (87, "Can delete product", 22, "delete_product"),\
            (88, "Can view product", 22, "view_product"),\
            (89, "Can add product addrule", 23, "add_productaddrule"),\
            (90, "Can change product addrule", 23, "change_productaddrule"),\
            (91, "Can delete product addrule", 23, "delete_productaddrule"),\
            (92, "Can view product addrule", 23, "view_productaddrule"),\
            (93, "Can add product case", 24, "add_productcase"),\
            (94, "Can change product case", 24, "change_productcase"),\
            (95, "Can delete product case", 24, "delete_productcase"),\
            (96, "Can view product case", 24, "view_productcase"),\
            (97, "Can add product size", 25, "add_productsize"),\
            (98, "Can change product size", 25, "change_productsize"),\
            (99, "Can delete product size", 25, "delete_productsize"),\
            (100, "Can view product size", 25, "view_productsize"),\
            (101, "Can add singleplus1", 26, "add_singleplus1"),\
            (102, "Can change singleplus1", 26, "change_singleplus1"),\
            (103, "Can delete singleplus1", 26, "delete_singleplus1"),\
            (104, "Can view singleplus1", 26, "view_singleplus1"),\
            (105, "Can add singleplus2", 27, "add_singleplus2"),\
            (106, "Can change singleplus2", 27, "change_singleplus2"),\
            (107, "Can delete singleplus2", 27, "delete_singleplus2"),\
            (108, "Can view singleplus2", 27, "view_singleplus2"),\
            (109, "Can add singleplus3", 28, "add_singleplus3"),\
            (110, "Can change singleplus3", 28, "change_singleplus3"),\
            (111, "Can delete singleplus3", 28, "delete_singleplus3"),\
            (112, "Can view singleplus3", 28, "view_singleplus3"),\
            (113, "Can add sort", 29, "add_sort"),\
            (114, "Can change sort", 29, "change_sort"),\
            (115, "Can delete sort", 29, "delete_sort"),\
            (116, "Can view sort", 29, "view_sort"),\
            (117, "Can add store", 30, "add_store"),\
            (118, "Can change store", 30, "change_store"),\
            (119, "Can delete store", 30, "delete_store"),\
            (120, "Can view store", 30, "view_store"),\
            (121, "Can add stuff", 31, "add_stuff"),\
            (122, "Can change stuff", 31, "change_stuff"),\
            (123, "Can delete stuff", 31, "delete_stuff"),\
            (124, "Can view stuff", 31, "view_stuff"),\
            (125, "Can add comment", 32, "add_comment"),\
            (126, "Can change comment", 32, "change_comment"),\
            (127, "Can delete comment", 32, "delete_comment"),\
            (128, "Can view comment", 32, "view_comment"),\
            (129, "Can add customized plus", 33, "add_customizedplus"),\
            (130, "Can change customized plus", 33, "change_customizedplus"),\
            (131, "Can delete customized plus", 33, "delete_customizedplus"),\
            (132, "Can view customized plus", 33, "view_customizedplus");\
\
            CREATE TABLE `auth_user` (\
            `id` int(11) NOT NULL,\
            `password` varchar(128) NOT NULL,\
            `last_login` datetime(6) DEFAULT NULL,\
            `is_superuser` tinyint(1) NOT NULL,\
            `username` varchar(150) NOT NULL,\
            `first_name` varchar(30) NOT NULL,\
            `last_name` varchar(150) NOT NULL,\
            `email` varchar(254) NOT NULL,\
            `is_staff` tinyint(1) NOT NULL,\
            `is_active` tinyint(1) NOT NULL,\
            `date_joined` datetime(6) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `auth_user_groups` (\
            `id` int(11) NOT NULL,\
            `user_id` int(11) NOT NULL,\
            `group_id` int(11) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `auth_user_user_permissions` (\
            `id` int(11) NOT NULL,\
            `user_id` int(11) NOT NULL,\
            `permission_id` int(11) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            DROP TABLE IF EXISTS `comment`;\
            CREATE TABLE `comment` (\
            `detail_id` int(10) NOT NULL,\
            `guest_account` varchar(10) NOT NULL,\
            `comment` varchar(200) NOT NULL,\
            `comment_score` int(2) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `comment`\
            ADD PRIMARY KEY (`detail_id`,`guest_account`) USING BTREE,\
            ADD KEY `comment_guest` (`guest_account`);\
\
            DROP TABLE IF EXISTS `customized`;\
            CREATE TABLE `customized` (\
            `customized_id` int(10) NOT NULL,\
            `sp1_number` int(10) DEFAULT NULL,\
            `sp2_number` int(10) DEFAULT NULL,\
            `sp3_number` int(10) DEFAULT NULL,\
            `sp_price` int(10) NOT NULL,\
            `add_other` varchar(100) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `customized`\
            ADD PRIMARY KEY (`customized_id`),\
            ADD KEY `customization_sp1` (`sp1_number`),\
            ADD KEY `customization_sp2` (`sp2_number`),\
            ADD KEY `customization_sp3` (`sp3_number`);\
\
            DROP TABLE IF EXISTS `customized_plus`;\
            CREATE TABLE `customized_plus` (\
            `customized_id` int(10) NOT NULL,\
            `mp_number` int(10) NOT NULL,\
            `plus_quantity` int(2) NOT NULL,\
            `customizedplus_price` int(10) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `customized_plus`\
            ADD PRIMARY KEY (`mp_number`,`customized_id`) USING BTREE,\
            ADD KEY `customization_cus` (`customized_id`);\
\
            DROP TABLE IF EXISTS `product`;\
            CREATE TABLE `product` (\
            `product_id` int(10) NOT NULL,\
            `product_name` varchar(100) NOT NULL,\
            `product_sort` varchar(10) NOT NULL,\
            `product_pic` varchar(50) NOT NULL,\
            `product_add` varchar(10) NOT NULL,\
            `product_introduction` varchar(500) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `product`\
            ADD PRIMARY KEY (`product_id`),\
            ADD KEY `fk_productadd` (`product_add`);\
\
            DROP TABLE IF EXISTS `guest`;\
            CREATE TABLE `guest` (\
            `guest_account` varchar(10) NOT NULL,\
            `guest_password` varchar(10) NOT NULL,\
            `guest_name` varchar(10) NOT NULL,\
            `guest_phone` varchar(12) NOT NULL,\
            `guest_address` varchar(50) NOT NULL,\
            `guest_mail` varchar(50) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `guest`\
            ADD PRIMARY KEY (`guest_account`);\
  \
\
            DROP TABLE IF EXISTS `drink_order`;\
            CREATE TABLE `drink_order` (\
            `order_id` int(10) NOT NULL,\
            `guest_account` varchar(10) NOT NULL,\
            `order_date` datetime NOT NULL DEFAULT current_timestamp(),\
            `order_status` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `drink_order`\
            ADD PRIMARY KEY (`order_id`),\
            ADD KEY `order_guest` (`guest_account`);\
\
            DROP TABLE IF EXISTS `multipleplus`;\
            CREATE TABLE `multipleplus` (\
            `number` int(10) NOT NULL,\
            `name` varchar(10) NOT NULL,\
            `price` int(10) NOT NULL,\
            `hide` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `multipleplus`\
            ADD PRIMARY KEY (`number`);\
\
            DROP TABLE IF EXISTS `order_detail`;\
            CREATE TABLE `order_detail` (\
            `detail_id` int(10) NOT NULL,\
            `order_id` int(10) NOT NULL,\
            `productsize_id` int(10) NOT NULL,\
            `customized_id` int(10) NOT NULL,\
            `detail_quantity` int(10) NOT NULL,\
            `detail_price` int(10) NOT NULL,\
            `recommend` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            ALTER TABLE `order_detail`\
            ADD PRIMARY KEY (`detail_id`),\
            ADD KEY `detail_productsize` (`productsize_id`),\
            ADD KEY `detail_order` (`order_id`),\
            ADD KEY `detail_customization` (`customized_id`);\
            \
            DROP TABLE IF EXISTS `product_addrule`;\
            CREATE TABLE `product_addrule` (\
            `product_add` varchar(5) NOT NULL,\
            `add_chinese` varchar(50) DEFAULT NULL,\
            `add_table` varchar(100) DEFAULT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `product_addrule`\
            ADD PRIMARY KEY (`product_add`);\
            \
            DROP TABLE IF EXISTS `product_case`;\
            CREATE TABLE `product_case` (\
            `product_add` varchar(10) NOT NULL,\
            `plus_id` int(10) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `product_case`\
            ADD PRIMARY KEY (`product_add`,`plus_id`) USING BTREE;\
            \
            DROP TABLE IF EXISTS `product_size`;\
            CREATE TABLE `product_size` (\
            `productsize_id` int(10) NOT NULL,\
            `product_id` int(10) NOT NULL,\
            `product_size` varchar(10) NOT NULL,\
            `product_price` int(3) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            \
            ALTER TABLE `product_size`\
            ADD PRIMARY KEY (`productsize_id`),\
            ADD KEY `product_size` (`product_id`);\
            \
            DROP TABLE IF EXISTS `singleplus_1`;\
            CREATE TABLE `singleplus_1` (\
            `number` int(10) NOT NULL,\
            `name` varchar(10) NOT NULL,\
            `price` int(10) NOT NULL,\
            `hide` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `singleplus_1`\
            ADD PRIMARY KEY (`number`);\
            \
            DROP TABLE IF EXISTS `singleplus_2`;\
            CREATE TABLE `singleplus_2` (\
            `number` int(10) NOT NULL,\
            `name` varchar(10) NOT NULL,\
            `price` int(10) NOT NULL,\
            `hide` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `singleplus_2`\
            ADD PRIMARY KEY (`number`);\
            \
            DROP TABLE IF EXISTS `singleplus_3`;\
            CREATE TABLE `singleplus_3` (\
            `number` int(10) NOT NULL,\
            `name` varchar(10) NOT NULL,\
            `price` int(10) NOT NULL,\
            `hide` tinyint(1) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `singleplus_3`\
            ADD PRIMARY KEY (`number`);\
            \
            DROP TABLE IF EXISTS `sort`;\
            CREATE TABLE `sort` (\
            `sort_id` int(3) NOT NULL,\
            `sort_type` varchar(10) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `sort`\
            ADD PRIMARY KEY (`sort_id`);\
            \
            DROP TABLE IF EXISTS `stuff`;\
            CREATE TABLE `stuff` (\
            `stuff_account` varchar(10) NOT NULL,\
            `stuff_password` varchar(10) NOT NULL,\
            `stuff_name` varchar(10) NOT NULL,\
            `store_name` varchar(20) NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            \
            ALTER TABLE `stuff`\
            ADD PRIMARY KEY (`stuff_account`),\
            ADD KEY `stuff_store` (`store_name`);\
            \
            ALTER TABLE `multipleplus`\
            MODIFY `number` int(10) NOT NULL AUTO_INCREMENT;\
            \
            ALTER TABLE `customized`\
            MODIFY `customized_id` int(10) NOT NULL AUTO_INCREMENT;\
            \
            \
            ALTER TABLE `order_detail`\
            MODIFY `detail_id` int(10) NOT NULL AUTO_INCREMENT;\
            \
            ALTER TABLE `singleplus_1`\
            MODIFY `number` int(10) NOT NULL AUTO_INCREMENT;\
            \
            \
            ALTER TABLE `singleplus_2`\
            MODIFY `number` int(10) NOT NULL AUTO_INCREMENT;\
            \
            \
            ALTER TABLE `singleplus_3`\
            MODIFY `number` int(10) NOT NULL AUTO_INCREMENT;\
            \
            ALTER TABLE `sort`\
            MODIFY `sort_id` int(3) NOT NULL AUTO_INCREMENT;\
            \
            ALTER TABLE `drink_order`\
            MODIFY `order_id` int(10) NOT NULL AUTO_INCREMENT;\
            \
            ALTER TABLE `drink_order`\
            ADD CONSTRAINT `order_guest` FOREIGN KEY (`guest_account`) REFERENCES `guest` (`guest_account`) ON DELETE NO ACTION;\
            \
            \
            ALTER TABLE `product_size`\
            ADD CONSTRAINT `product_size` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;\
            \
            ALTER TABLE `order_detail`\
            ADD CONSTRAINT `detail_customization` FOREIGN KEY (`customized_id`) REFERENCES `customized` (`customized_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
            ADD CONSTRAINT `detail_order` FOREIGN KEY (`order_id`) REFERENCES `drink_order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
            ADD CONSTRAINT `detail_productsize` FOREIGN KEY (`productsize_id`) REFERENCES `product_size` (`productsize_id`) ON DELETE NO ACTION;\
            \
            ALTER TABLE `comment`\
            ADD CONSTRAINT `comment_detail` FOREIGN KEY (`detail_id`) REFERENCES `order_detail` (`detail_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
            ADD CONSTRAINT `comment_guest` FOREIGN KEY (`guest_account`) REFERENCES `guest` (`guest_account`);\
            \
            \
            ALTER TABLE `customized`\
            ADD CONSTRAINT `customization_sp1` FOREIGN KEY (`sp1_number`) REFERENCES `singleplus_1` (`number`),\
            ADD CONSTRAINT `customization_sp2` FOREIGN KEY (`sp2_number`) REFERENCES `singleplus_2` (`number`),\
            ADD CONSTRAINT `customization_sp3` FOREIGN KEY (`sp3_number`) REFERENCES `singleplus_3` (`number`);\
            \
            ALTER TABLE `customized_plus`\
            ADD CONSTRAINT `customization_cus` FOREIGN KEY (`customized_id`) REFERENCES `customized` (`customized_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
            ADD CONSTRAINT `customization_plus` FOREIGN KEY (`mp_number`) REFERENCES `multipleplus` (`number`);\
\
            CREATE TABLE `django_admin_log` (\
			  `id` int(11) NOT NULL,\
			  `action_time` datetime(6) NOT NULL,\
			  `object_id` longtext DEFAULT NULL,\
			  `object_repr` varchar(200) NOT NULL,\
			  `action_flag` smallint(5) UNSIGNED NOT NULL,\
			  `change_message` longtext NOT NULL,\
			  `content_type_id` int(11) DEFAULT NULL,\
			  `user_id` int(11) NOT NULL\
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `django_content_type` (\
  			  `id` int(11) NOT NULL,\
			  `app_label` varchar(100) NOT NULL,\
			  `model` varchar(100) NOT NULL\
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES\
			(1, "admin", "logentry"),\
			(3, "auth", "group"),\
			(2, "auth", "permission"),\
			(4, "auth", "user"),\
			(5, "contenttypes", "contenttype"),\
			(7, "manage_menu", "authgroup"),\
			(8, "manage_menu", "authgrouppermissions"),\
			(9, "manage_menu", "authpermission"),\
			(10, "manage_menu", "authuser"),\
			(11, "manage_menu", "authusergroups"),\
			(12, "manage_menu", "authuseruserpermissions"),\
			(32, "manage_menu", "comment"),\
			(13, "manage_menu", "customized"),\
			(33, "manage_menu", "customizedplus"),\
			(14, "manage_menu", "djangoadminlog"),\
			(15, "manage_menu", "djangocontenttype"),\
			(16, "manage_menu", "djangomigrations"),\
			(17, "manage_menu", "djangosession"),\
			(18, "manage_menu", "drinkorder"),\
			(19, "manage_menu", "guest"),\
			(20, "manage_menu", "multipleplus"),\
			(21, "manage_menu", "orderdetail"),\
			(22, "manage_menu", "product"),\
			(23, "manage_menu", "productaddrule"),\
			(24, "manage_menu", "productcase"),\
			(25, "manage_menu", "productsize"),\
			(26, "manage_menu", "singleplus1"),\
			(27, "manage_menu", "singleplus2"),\
			(28, "manage_menu", "singleplus3"),\
			(29, "manage_menu", "sort"),\
			(30, "manage_menu", "store"),\
			(31, "manage_menu", "stuff"),\
			(6, "sessions", "session");\
\
            CREATE TABLE `django_migrations` (\
			  `id` int(11) NOT NULL,\
			  `app` varchar(255) NOT NULL,\
			  `name` varchar(255) NOT NULL,\
			  `applied` datetime(6) NOT NULL\
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
\
            CREATE TABLE `django_session` (\
			  `session_key` varchar(40) NOT NULL,\
			  `session_data` longtext NOT NULL,\
			  `expire_date` datetime(6) NOT NULL\
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
            ' % account)
            

        return redirect('/login/')

    return render(request,'login.html')