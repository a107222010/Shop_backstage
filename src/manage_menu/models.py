# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from manage_menu.storage import OverwriteStorage
from manage_menu.storage_banner import OverwriteStorage_banner
from manage_menu.storage_shop_photo import OverwriteStorage_shop_photo
from manage_menu.storage_sort import OverwriteStorage_sort


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class Comment(models.Model):
    detail = models.ForeignKey("OrderDetail", models.DO_NOTHING, primary_key=True)
    guest_account = models.CharField(max_length=10)
    comment = models.CharField(max_length=200)
    comment_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = "comment"
        unique_together = (("detail", "guest_account"),)


class Customized(models.Model):
    customized_id = models.AutoField(primary_key=True)
    sp1_number = models.ForeignKey(
        "Singleplus1", models.DO_NOTHING, db_column="sp1_number", blank=True, null=True
    )
    sp2_number = models.ForeignKey(
        "Singleplus2", models.DO_NOTHING, db_column="sp2_number", blank=True, null=True
    )
    sp3_number = models.ForeignKey(
        "Singleplus3", models.DO_NOTHING, db_column="sp3_number", blank=True, null=True
    )
    sp_price = models.IntegerField()
    add_other = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "customized"


class CustomizedPlus(models.Model):
    customized = models.ForeignKey(Customized, models.DO_NOTHING)
    mp_number = models.ForeignKey(
        "Multipleplus", models.DO_NOTHING, db_column="mp_number", primary_key=True
    )
    plus_quantity = models.IntegerField()
    customizedplus_price = models.IntegerField()

    class Meta:
        db_table = "customized_plus"
        unique_together = (("mp_number", "customized"),)


class DrinkOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    guest_account = models.ForeignKey(
        "Guest", models.DO_NOTHING, db_column="guest_account"
    )
    order_date = models.DateTimeField()
    order_status = models.IntegerField()

    class Meta:

        db_table = "drink_order"


class Guest(models.Model):
    guest_account = models.CharField(primary_key=True, max_length=10)
    guest_password = models.CharField(max_length=10)
    guest_name = models.CharField(max_length=10)
    guest_phone = models.CharField(max_length=12)
    guest_address = models.CharField(max_length=50)
    guest_mail = models.CharField(max_length=50)

    class Meta:

        db_table = "guest"

    def __str__(self):
        return self.guest_account


class Multipleplus(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    hide = models.IntegerField()

    class Meta:
        db_table = "multipleplus"

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(DrinkOrder, models.DO_NOTHING)
    productsize = models.ForeignKey("ProductSize", models.DO_NOTHING)
    customized = models.ForeignKey(Customized, models.DO_NOTHING)
    detail_quantity = models.IntegerField()
    detail_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = "order_detail"


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_sort = models.CharField(max_length=10)
    product_pic = models.ImageField(storage=OverwriteStorage(), upload_to="")
    product_add = models.CharField(max_length=10)
    product_introduction = models.CharField(max_length=500)
    hide = models.IntegerField(default="")

    class Meta:
        db_table = "product"


class ProductCase(models.Model):
    product_add = models.CharField(primary_key=True, max_length=10)
    plus_id = models.IntegerField()
    hide = models.IntegerField()

    class Meta:
        managed = False
        db_table = "product_case"
        unique_together = (("product_add", "plus_id"),)


class ProductSize(models.Model):
    productsize_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, default="")
    product_size = models.CharField(max_length=10)
    product_price = models.IntegerField()
    size = models.IntegerField(default="")
    hide = models.IntegerField(default="")

    class Meta:

        db_table = "product_size"


class Singleplus1(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    hide = models.IntegerField()

    class Meta:
        managed = False
        db_table = "singleplus_1"


class Singleplus2(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    hide = models.IntegerField()

    class Meta:
        managed = False
        db_table = "singleplus_2"


class Singleplus3(models.Model):
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    hide = models.IntegerField()

    class Meta:
        managed = False
        db_table = "singleplus_3"


class Sort(models.Model):
    sort_id = models.AutoField(primary_key=True)
    sort_type = models.CharField(max_length=10)
    photo = models.ImageField(storage=OverwriteStorage_sort(), upload_to="", default="")
    hide = models.IntegerField()

    class Meta:

        db_table = "sort"


class Stuff(models.Model):
    stuff_account = models.CharField(primary_key=True, max_length=10)
    stuff_password = models.CharField(max_length=10)
    stuff_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "stuff"


class ShopDetail(models.Model):
    shop_chinese = models.CharField(primary_key=True, max_length=50)
    shop_name = models.CharField(max_length=50)
    shop_phone = models.CharField(max_length=10)
    shop_admin = models.CharField(max_length=50)
    photo = models.ImageField(storage=OverwriteStorage_shop_photo(), upload_to="")

    class Meta:
        db_table = "shop_detail"


class Advertise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    photo = models.ImageField(storage=OverwriteStorage_banner(), upload_to="")
    URL = models.CharField(max_length=500)

    class Meta:
        db_table = "advertise"


class TableUnit(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True, default=""
    )  # Field name made lowercase.
    unit = models.TextField(db_column="Unit", default="")  # Field name made lowercase.

    class Meta:
        db_table = "table_unit"

