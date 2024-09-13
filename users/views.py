from rest_framework.views import APIView
from .models import User, Role, Permissions, RolePermissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password

from backend.permissions import IsAdminUser
from .tokens import get_token, decode_token
from .serializers import UserSerializer, RoleSerializer, AddPermissionSerializer, RolePermissionsModelSerializer,PermissionsModelSerializer, UserLoginSerializer,UserListModelSerailizer,ChangePasswordSerializer
from backend.paginations import PagePaginationCustom
from django.http.response import Http404
from django.db.models import ProtectedError
from rest_framework.permissions import AllowAny

class HelloWorldAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({"message":"Hello World !"},status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            # checking if the user exist or not
            if not User.objects.filter(email=serializer.validated_data['email']).exists():
                if not User.objects.filter(username=serializer.validated_data['email']).exists():
                    return Response("Invalid User", status=status.HTTP_401_UNAUTHORIZED)

            # extacting the data
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                user = User.objects.get(username=serializer.validated_data['email'])
            password = serializer.validated_data['password']

            # checking if the password is wrong or not
            if not check_password(password, user.password):
                return Response("Invalid Password", status=status.HTTP_401_UNAUTHORIZED)

            # generating the token
            token = get_token(user)
            return Response(token)


class UserRegistration(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save(serializer.validated_data['role_id'],serializer.validated_data['email'],serializer.validated_data['password'])
            try:
                User.objects.get(email=serializer.validated_data['username'])
                return Response('Username cannot be an existing email!')
            except User.DoesNotExist:
                pass
            if not User.objects.filter(email=serializer.validated_data['email']).exists():
                if not User.objects.filter(username=serializer.validated_data['username']).exists():
                    password = serializer.validated_data['password']
                    h_password = make_password(password, salt=None, hasher='default')
                    role = Role.objects.get(role_id=serializer.validated_data['role_id'])
                    user = User(role_id=role, username=serializer.validated_data['username'],
                                email=serializer.validated_data['email'], password=h_password)
                    user.save()
                    response = {
                        'message': 'User has been register',
                        'data': serializer.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
            response = {
                'message': 'User is already register'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView,PagePaginationCustom):
    def get(self,request):
        user = User.objects.all()
        search = request.GET.get('search')
        if search is not None:
            user = user.filter(username__icontains=search) | \
                   user.filter(email__icontains=search) | \
                   user.filter(role_id__name__icontains=search)
        data = self.paginate_queryset(user, request)
        serializer = UserListModelSerailizer(data, many=True)
        return self.get_paginated_response(serializer.data)


class RoleView(APIView, PagePaginationCustom):
    def get(self, request):
        role = Role.objects.all()
        data = self.paginate_queryset(role, request)
        serializer = RoleSerializer(data, many=True)
        return self.get_paginated_response(serializer.data)
        # return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            input_name = serializer.validated_data['name']
            description = serializer.validated_data['description']
            # print(name) 
            if not Role.objects.filter(name=input_name, status=1).exists():
                role = Role(name=input_name, description=description)
                role.save()
                response = {
                    'message': 'Role have been added'
                }
                return Response(response, status=status.HTTP_200_OK)
            response = {
                'message': 'Role Already Exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'post failed'})


class RoleDetailView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(role_id=pk)
        except:
            raise Http404

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            role = self.get_object(pk)
            if Role.objects.filter(name=serializer.validated_data['name'],
                                   description=serializer.validated_data['description']).exists():
                response = {
                    'message': 'Role Already Exists'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            role.name = serializer.validated_data['name']
            role.description = serializer.validated_data['description']
            role.save()
            response = {
                'message': 'updated successfully',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'message': 'Fail to updated the Role'}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, pk):
        try:
            role = self.get_object(pk)
            role.status = 0
            role.save()
            response = {
                'message': 'Role deleted'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            response = {
                'error': 'ProtectedError',
                'message': 'Could not delete Role.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AddRolePermission(APIView):
    def post(self, request):
        role = decode_token(request)['role']
        if role == "Super-Admin":
            serializer = AddPermissionSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return Response({'error': e.args}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            role_id = serializer.validated_data['role_id']
            perm_id = serializer.validated_data['perm_id']

            if not Role.objects.filter(role_id=role_id).exists():
                return Response({'error': "Role not Found"}, status.HTTP_404_NOT_FOUND)
            if not Permissions.objects.filter(name=perm_id).exists():
                return Response({'error': "Permission not Found"}, status.HTTP_404_NOT_FOUND)

            role = Role.objects.get(role_id=role_id)
            permission = Permissions.objects.get(name=perm_id)

            if not RolePermissions.objects.filter(role=role, permission=permission).exists():
                role_permission = RolePermissions(role=role, permission=permission)
                role_permission.save()
                return Response(RolePermissionsModelSerializer(role_permission).data, status.HTTP_201_CREATED)
            else:
                role_permission = RolePermissions.objects.get(role=role, permission=permission)
                return Response(RolePermissionsModelSerializer(role_permission).data, status.HTTP_200_OK)
        else:
            return Response({'error': "Permission Denied"}, status=status.HTTP_401_UNAUTHORIZED)


class DeletePermission(APIView):
    def delete(self, request, role_id, perm_id):
        role = decode_token(request)['role']
        if role != "Super-Admin":
            return Response({'error': "Permission Denied"}, status=status.HTTP_401_UNAUTHORIZED)

        if not RolePermissions.objects.filter(role_id=role_id, permission_id=perm_id).exists():
            return Response({'error': 'Requested Permissions is not Present'}, status.HTTP_404_NOT_FOUND)

        role_perm = RolePermissions.objects.get(role_id=role_id, permission_id=perm_id)
        role_perm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListPermission(APIView):
    def get(self, request, role_id=None):
        if role_id == None:
            return Response(PermissionsModelSerializer(self.list_permissions(), many=True).data, status.HTTP_200_OK)
        else:
            return Response(RolePermissionsModelSerializer(self.list_role_permissions(role_id), many=True).data,
                            status.HTTP_200_OK)

    def list_permissions(self):
        return Permissions.objects.all()

    def list_role_permissions(self, role_id):
        return RolePermissions.objects.filter(role_id=role_id)


class ChangePasswordView(APIView):
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # checking if the user exist or not
            user = User.objects.get(user_id= decode_token(request)['user_id'])
            
            # checking if the password is wrong or not
            if not check_password(old_password, user.password):
                return Response("Invalid Password", status=status.HTTP_409_CONFLICT)
            h_password = make_password(new_password, salt=None, hasher='default')
            user.password = h_password
            user.save()

            response = {
                'message':'Password have been change'
            }
            return Response(response,status = status.HTTP_201_CREATED)