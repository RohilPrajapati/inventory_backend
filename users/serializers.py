from rest_framework import serializers
from .models import User, RolePermissions, Role, Permissions
from django.contrib.auth.hashers import make_password


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserListModelSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'role_id', 'role']
        depth = 2

    def get_role(self, obj):
        """Returns the role name or None if the role is not set."""
        return obj.role.name if obj.role else None

class UserSerializer(serializers.Serializer):
    role_id = serializers.CharField(required=False)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=True)

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

    class Meta:
        model = Role
        fields = '__all__'


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