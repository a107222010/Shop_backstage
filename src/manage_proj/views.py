from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from manage_proj import settings
from django.contrib.auth.models import User
from datetime import datetime
from manage_menu.models import ShopDetail, AuthUser
from django.db import connection
from django.core.files.storage import FileSystemStorage
import os


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def page_error(request):
    return render(request, "500.html", status=500)


def logout_view(request):
    logout(request)
    return redirect("/login/")


def login_view(request):

    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            db_ID = user.get_short_name()
            print(db_ID);
            if user is not None:
                login(request, user)
                database_id = db_ID  # just something unique
                newDatabase = {}
                newDatabase["id"] = database_id
                newDatabase["ENGINE"] = "django.db.backends.mysql"
                newDatabase["NAME"] = database_id
                newDatabase["USER"] = "root"
                newDatabase["PASSWORD"] = ""
                newDatabase["HOST"] = "localhost"
                newDatabase["PORT"] = "3306"
                settings.DATABASES[database_id] = newDatabase

                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("/")

    return render(request, "login.html", {"form": form})


def sign_up(request):
    
    if request.method == "POST":
        account = request.POST.get("shop_account")
        db_ID = request.POST.get("shop_account")
        password = request.POST.get("shop_password")
        e_mail = request.POST.get("shop_e_mail")
        shop_name = request.POST.get("shop_name")
        shop_phone = request.POST.get("shop_phone")
        shop_admin = request.POST.get("shop_admin")
        if bool(request.FILES.get("shop_photo", False)) == True:
            shop_photo = request.FILES["shop_photo"]
            fs = FileSystemStorage(location="C:\\xampp\\htdocs\\images\\ShopPhoto")
            fs.delete(shop_photo.name)
            fs.save(shop_photo.name, shop_photo)
            ShopDetail.objects.create(
                shop_chinese=shop_name,
                shop_name=account,
                shop_phone=shop_phone,
                shop_admin=shop_admin,
                photo=shop_photo,
            )
        else:
            ShopDetail.objects.create(
                shop_chinese=shop_name,
                shop_name=account,
                shop_phone=shop_phone,
                shop_admin=shop_admin,
            )

        os.mkdir(os.path.join("c:/", "xampp/htdocs/images/", account))
        os.mkdir(
            os.path.join("c:/", "xampp/htdocs/images/", account + "/", "AdvertisePhoto")
        )
        os.mkdir(os.path.join("c:/", "xampp/htdocs/images/", account + "/", "SortPic"))

        user = User.objects.create_user(
            username=account,
            email=e_mail,
            password=password,
            is_superuser=1,
            first_name = db_ID,
            is_staff=1,
            is_active=1,
            date_joined=datetime.now(),
        )

        if user:
            cursor = connection.cursor()
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                % account
            )
            cursor.execute(
                'USE %s; \
                CREATE TABLE `advertise` (\
                `id` int(11) NOT NULL,\
                `title` varchar(100) NOT NULL,\
                `photo` varchar(50) NOT NULL,\
                `URL` varchar(500) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8; \
                \
                CREATE TABLE `auth_group` (\
                `id` int(11) NOT NULL,\
                `name` varchar(150) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `auth_group_permissions` (\
                `id` int(11) NOT NULL,\
                `group_id` int(11) NOT NULL,\
                `permission_id` int(11) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `auth_permission` (\
                `id` int(11) NOT NULL,\
                `name` varchar(255) NOT NULL,\
                `content_type_id` int(11) NOT NULL,\
                `codename` varchar(100) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES\
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
                (24, "Can view session", 6, "view_session");\
                \
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
                \
                CREATE TABLE `auth_user_groups` (\
                `id` int(11) NOT NULL,\
                `user_id` int(11) NOT NULL,\
                `group_id` int(11) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `auth_user_user_permissions` (\
                `id` int(11) NOT NULL,\
                `user_id` int(11) NOT NULL,\
                `permission_id` int(11) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `comment` (\
                `detail_id` int(10) NOT NULL,\
                `guest_account` varchar(10) NOT NULL,\
                `comment` varchar(200) NOT NULL,\
                `comment_score` int(2) NOT NULL,\
                `recommend` int(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `customized` (\
                `customized_id` int(10) NOT NULL,\
                `sp1_number` int(10) DEFAULT NULL,\
                `sp2_number` int(10) DEFAULT NULL,\
                `sp3_number` int(10) DEFAULT NULL,\
                `sp_price` int(10) NOT NULL,\
                `add_other` varchar(100) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `customized_plus` (\
                `customized_id` int(10) NOT NULL,\
                `mp_number` int(10) NOT NULL,\
                `plus_quantity` int(2) NOT NULL,\
                `customizedplus_price` int(10) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
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
                (6, "sessions", "session");\
                \
                CREATE TABLE `django_migrations` (\
                `id` int(11) NOT NULL,\
                `app` varchar(255) NOT NULL,\
                `name` varchar(255) NOT NULL,\
                `applied` datetime(6) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES\
                (1, "contenttypes", "0001_initial", "2021-08-04 15:42:40.203562"),\
                (2, "auth", "0001_initial", "2021-08-04 15:42:40.294562"),\
                (3, "admin", "0001_initial", "2021-08-04 15:42:40.552382"),\
                (4, "admin", "0002_logentry_remove_auto_add", "2021-08-04 15:42:40.611785"),\
                (5, "admin", "0003_logentry_add_action_flag_choices", "2021-08-04 15:42:40.618962"),\
                (6, "contenttypes", "0002_remove_content_type_name", "2021-08-04 15:42:40.662839"),\
                (7, "auth", "0002_alter_permission_name_max_length", "2021-08-04 15:42:40.692825"),\
                (8, "auth", "0003_alter_user_email_max_length", "2021-08-04 15:42:40.728367"),\
                (9, "auth", "0004_alter_user_username_opts", "2021-08-04 15:42:40.735368"),\
                (10, "auth", "0005_alter_user_last_login_null", "2021-08-04 15:42:40.762366"),\
                (11, "auth", "0006_require_contenttypes_0002", "2021-08-04 15:42:40.764369"),\
                (12, "auth", "0007_alter_validators_add_error_messages", "2021-08-04 15:42:40.773373"),\
                (13, "auth", "0008_alter_user_username_max_length", "2021-08-04 15:42:40.786378"),\
                (14, "auth", "0009_alter_user_last_name_max_length", "2021-08-04 15:42:40.799373"),\
                (15, "auth", "0010_alter_group_name_max_length", "2021-08-04 15:42:40.834294"),\
                (16, "auth", "0011_update_proxy_permissions", "2021-08-04 15:42:40.844292"),\
                (17, "sessions", "0001_initial", "2021-08-04 15:42:40.858293"),\
                (18, "manage_menu", "0001_initial", "2021-08-11 16:31:12.280805");\
                \
                \
                CREATE TABLE `django_session` (\
                `session_key` varchar(40) NOT NULL,\
                `session_data` longtext NOT NULL,\
                `expire_date` datetime(6) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `drink_order` (\
                `order_id` int(10) NOT NULL,\
                `guest_account` varchar(10) NOT NULL,\
                `order_date` datetime NOT NULL DEFAULT current_timestamp(),\
                `order_status` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `multipleplus` (\
                `number` int(10) NOT NULL,\
                `name` varchar(10) NOT NULL,\
                `price` int(10) NOT NULL,\
                `hide` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `order_detail` (\
                `detail_id` int(10) NOT NULL,\
                `order_id` int(10) NOT NULL,\
                `productsize_id` int(10) NOT NULL,\
                `customized_id` int(10) NOT NULL,\
                `detail_quantity` int(10) NOT NULL,\
                `detail_price` int(10) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `product` (\
                `product_id` int(10) NOT NULL,\
                `product_name` varchar(100) NOT NULL,\
                `product_sort` varchar(10) NOT NULL,\
                `product_pic` varchar(50) NOT NULL,\
                `product_add` varchar(10) NOT NULL,\
                `product_introduction` varchar(500) NOT NULL,\
                `hide` int(1) NOT NULL DEFAULT 0\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `product_case` (\
                `product_add` varchar(10) NOT NULL,\
                `plus_id` int(10) DEFAULT NULL,\
                `hide` int(11) NOT NULL DEFAULT 0\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                \
                CREATE TABLE `product_size` (\
                `productsize_id` int(11) NOT NULL,\
                `product_id` int(10) NOT NULL,\
                `product_size` varchar(10) NOT NULL,\
                `product_price` int(3) NOT NULL,\
                `size` int(2) NOT NULL,\
                `hide` tinyint(1) DEFAULT 0\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `singleplus_1` (\
                `number` int(10) NOT NULL,\
                `name` varchar(10) NOT NULL,\
                `price` int(10) NOT NULL,\
                `hide` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `singleplus_2` (\
                `number` int(10) NOT NULL,\
                `name` varchar(10) NOT NULL,\
                `price` int(10) NOT NULL,\
                `hide` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `singleplus_3` (\
                `number` int(10) NOT NULL,\
                `name` varchar(10) NOT NULL,\
                `price` int(10) NOT NULL,\
                `hide` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `sort` (\
                `sort_id` int(3) NOT NULL,\
                `sort_type` varchar(10) NOT NULL,\
                `photo` varchar(11) DEFAULT NULL,\
                `hide` tinyint(1) NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                \
                CREATE TABLE `table_unit` (\
                `ID` int(11) NOT NULL,\
                `Unit` text NOT NULL\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;\
                INSERT INTO `table_unit` (`ID`, `Unit`) VALUES\
                (1, "冰度"),\
                (2, "甜度"),\
                (3, "咖啡豆"),\
                (4, "配料");\
                \
                \
                ALTER TABLE `advertise`\
                ADD PRIMARY KEY (`id`);\
                \
                \
                ALTER TABLE `auth_group`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `name` (`name`);\
                \
                \
                ALTER TABLE `auth_group_permissions`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),\
                ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);\
                \
                \
                ALTER TABLE `auth_permission`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);\
                \
                \
                ALTER TABLE `auth_user`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `username` (`username`);\
                \
                \
                ALTER TABLE `auth_user_groups`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),\
                ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);\
                \
                \
                ALTER TABLE `auth_user_user_permissions`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),\
                ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);\
                \
                \
                ALTER TABLE `comment`\
                ADD PRIMARY KEY (`detail_id`,`guest_account`) USING BTREE;\
                \
                \
                ALTER TABLE `customized`\
                ADD PRIMARY KEY (`customized_id`),\
                ADD KEY `customization_sp1` (`sp1_number`),\
                ADD KEY `customization_sp2` (`sp2_number`),\
                ADD KEY `customization_sp3` (`sp3_number`);\
                \
                \
                ALTER TABLE `customized_plus`\
                ADD PRIMARY KEY (`mp_number`,`customized_id`) USING BTREE,\
                ADD KEY `customization_cus` (`customized_id`);\
                \
                \
                ALTER TABLE `django_admin_log`\
                ADD PRIMARY KEY (`id`),\
                ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),\
                ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);\
                \
                \
                ALTER TABLE `django_content_type`\
                ADD PRIMARY KEY (`id`),\
                ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);\
                \
                \
                ALTER TABLE `django_migrations`\
                ADD PRIMARY KEY (`id`);\
                \
                \
                ALTER TABLE `django_session`\
                ADD PRIMARY KEY (`session_key`),\
                ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);\
                \
                \
                ALTER TABLE `drink_order`\
                ADD PRIMARY KEY (`order_id`);\
                \
                \
                ALTER TABLE `multipleplus`\
                ADD PRIMARY KEY (`number`);\
                \
                \
                ALTER TABLE `order_detail`\
                ADD PRIMARY KEY (`detail_id`),\
                ADD KEY `detail_order` (`order_id`),\
                ADD KEY `detail_customization` (`customized_id`),\
                ADD KEY `detail_productsize` (`productsize_id`);\
                \
                \
                ALTER TABLE `product`\
                ADD PRIMARY KEY (`product_id`);\
                \
                \
                ALTER TABLE `product_size`\
                ADD PRIMARY KEY (`productsize_id`) USING BTREE,\
                ADD KEY `product_size` (`product_id`);\
                \
                ALTER TABLE `singleplus_1`\
                ADD PRIMARY KEY (`number`);\
                \
                \
                ALTER TABLE `singleplus_2`\
                ADD PRIMARY KEY (`number`);\
                \
                \
                ALTER TABLE `singleplus_3`\
                ADD PRIMARY KEY (`number`);\
                \
                \
                ALTER TABLE `sort`\
                ADD PRIMARY KEY (`sort_id`);\
                \
                \
                ALTER TABLE `table_unit`\
                ADD PRIMARY KEY (`ID`);\
                \
                \
                ALTER TABLE `advertise`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;\
                \
                \
                ALTER TABLE `auth_group`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `auth_group_permissions`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `auth_permission`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;\
                \
                \
                ALTER TABLE `auth_user`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `auth_user_groups`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `auth_user_user_permissions`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `customized`\
                MODIFY `customized_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;\
                \
                \
                ALTER TABLE `django_admin_log`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;\
                \
                \
                ALTER TABLE `django_content_type`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;\
                \
                \
                ALTER TABLE `django_migrations`\
                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;\
                \
                \
                ALTER TABLE `drink_order`\
                MODIFY `order_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `multipleplus`\
                MODIFY `number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `order_detail`\
                MODIFY `detail_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;\
                \
                \
                ALTER TABLE `product_size`\
                MODIFY `productsize_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=220;\
                \
                \
                ALTER TABLE `singleplus_1`\
                MODIFY `number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `singleplus_2`\
                MODIFY `number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `singleplus_3`\
                MODIFY `number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `sort`\
                MODIFY `sort_id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                ALTER TABLE `table_unit`\
                MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;\
                \
                \
                ALTER TABLE `auth_group_permissions`\
                ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),\
                ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);\
                \
                \
                ALTER TABLE `auth_permission`\
                ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);\
                \
                \
                ALTER TABLE `auth_user_groups`\
                ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),\
                ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);\
                \
                \
                ALTER TABLE `auth_user_user_permissions`\
                ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),\
                ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);\
                \
                \
                ALTER TABLE `comment`\
                ADD CONSTRAINT `comment_detail` FOREIGN KEY (`detail_id`) REFERENCES `order_detail` (`detail_id`) ON DELETE CASCADE ON UPDATE CASCADE;\
                \
                \
                ALTER TABLE `customized`\
                ADD CONSTRAINT `customization_sp1` FOREIGN KEY (`sp1_number`) REFERENCES `singleplus_1` (`number`),\
                ADD CONSTRAINT `customization_sp2` FOREIGN KEY (`sp2_number`) REFERENCES `singleplus_2` (`number`),\
                ADD CONSTRAINT `customization_sp3` FOREIGN KEY (`sp3_number`) REFERENCES `singleplus_3` (`number`);\
                \
                \
                ALTER TABLE `customized_plus`\
                ADD CONSTRAINT `customization_cus` FOREIGN KEY (`customized_id`) REFERENCES `customized` (`customized_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                ADD CONSTRAINT `customization_plus` FOREIGN KEY (`mp_number`) REFERENCES `multipleplus` (`number`);\
                \
                \
                ALTER TABLE `django_admin_log`\
                ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),\
                ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);\
                \
                \
                ALTER TABLE `order_detail`\
                ADD CONSTRAINT `detail_customization` FOREIGN KEY (`customized_id`) REFERENCES `customized` (`customized_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                ADD CONSTRAINT `detail_order` FOREIGN KEY (`order_id`) REFERENCES `drink_order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
                ADD CONSTRAINT `detail_productsize` FOREIGN KEY (`productsize_id`) REFERENCES `product_size` (`productsize_id`) ON DELETE NO ACTION;\
                \
                \
                ALTER TABLE `product_size`\
                ADD CONSTRAINT `product_size` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;\
                COMMIT;\
                '
                % account
            )

        return redirect("/login/")

    return render(request, "login.html")

