from rest_framework import serializers
from .models import User, RolePermissions, Role, Permissions
from django.contrib.auth.hashers import make_password


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserListModelSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','role_id']
        depth = 2

class UserSerializer(serializers.Serializer):
    # TODO role_id compulsory garnu parxa login ma role halda problem aouxa
    role_id = serializers.CharField(required=False)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def save(self, role_id, email, password, username):
        h_password = make_password(password, salt=None, hasher='default')
        user = User(role_id=role_id, username=username, email=email, password=h_password)
        user.save()


class RoleSerializer(serializers.Serializer):
    role_id = serializers.ReadOnlyField()
    name = serializers.CharField()
    description = serializers.CharField()


class AddPermissionSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    perm_id = serializers.CharField()


class PermissionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class RoleModelSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Role
        exclude = ('role_id',)

    def get_id(self, obj):
        return obj.role_id


class RolePermissionsModelSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def get_role(self, obj):
        role = Role.objects.get(role_id=obj.role_id)
        return RoleModelSerializer(role).data

    def get_permission(self, obj):
        permission = Permissions.objects.get(name=obj.permission_id)
        return PermissionsModelSerializer(permission).data

    class Meta:
        model = RolePermissions
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length = 255)
    new_password = serializers.CharField(max_length = 255)