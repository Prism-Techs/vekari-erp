from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='Latin1_General_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='Latin1_General_CI_AI')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Latin1_General_CI_AI')
    first_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    last_name = models.CharField(max_length=150, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    mobile_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    email = models.CharField(max_length=254, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    is_admin = models.BooleanField()
    profile_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    date_joined = models.DateTimeField()
    creation_by = models.IntegerField(blank=True, null=True)
    update_profile_by = models.IntegerField(blank=True, null=True)
    last_ip_address = models.CharField(max_length=120, db_collation='Latin1_General_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return self.username
class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='Latin1_General_CI_AI')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='Latin1_General_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')
    model = models.CharField(max_length=100, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='Latin1_General_CI_AI')
    name = models.CharField(max_length=255, db_collation='Latin1_General_CI_AI')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='Latin1_General_CI_AI')
    session_data = models.TextField(db_collation='Latin1_General_CI_AI')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Permission(models.Model):
    permission_name = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'permission'


class UserPermission(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey('UserPermissionGroup', models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_permission'


class UserPermissionGroup(models.Model):
    group_name = models.CharField(unique=True, max_length=50, db_collation='Latin1_General_CI_AI')

    class Meta:
        managed = False
        db_table = 'user_permission_group'

class ApprovalMaster(models.Model):
    approval_id = models.AutoField(primary_key=True)
    approval_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'approval_master'

class UserApproval(models.Model):
    user_approval_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    approval = models.ForeignKey(ApprovalMaster, models.DO_NOTHING)
    approver_level = models.IntegerField()
    create_by = models.IntegerField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_approval'

