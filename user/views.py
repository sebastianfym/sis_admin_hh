from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .serializers import UserSerializer
from .services import get_access_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
# django
from django.db import transaction

# Локальные импорты
from .models import User


class Authentication(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["POST"], detail=False, url_path="auth")
    def authorization(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                user_data = self.get_serializer(user).data
                token = get_access_token(user, request)
                return Response({'token': token, 'user': user_data}, 200)
            else:
                raise Exception
        except Exception:
            return Response({'detail': 'Неверный логин или пароль'}, 403)

    @action(methods=["POST"], detail=False, url_path="auth_user")
    def authorization_user(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user_data = self.get_serializer(user).data
                token = get_access_token(user, request)
                return Response({'token': token, 'user': user_data}, 200)
            else:
                raise Exception
        except Exception:
            return Response({'detail': 'Неверный логин или пароль'}, 403)

    @action(methods=["POST"], detail=False)
    def registration(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Не указан email"}, status=400)
        username = request.data.get("username")
        user = User.objects.create(
            email=email,
            username=username,
        )
        user.set_password(request.data.get("password"))
        user.save()
        user_data = self.get_serializer(user).data
        token = get_access_token(user, request)
        return Response({'token': token, 'user': user_data}, status=200)


class Profile(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["GET"], detail=False)
    def info(self, request):
        return Response(self.get_serializer(request.user, many=False).data)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def change_profile(self, request):
        user = request.user
        username = request.data.get("username")
        email = request.data.get("email")
        if user.username != username and username != None:
            user.username = username
        if user.email != email and email != None:
            user.email = email
        user.save()
        return Response({"detail": "Данные пользователя изменены"}, 200)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def change_password(self, request):
        new_password = request.data.get("new_password")
        user = request.user
        if not new_password:
            return Response({"detail": "Укажите новый пароль"}, 400)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Пароль успешно изменен на новый"}, 200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('username', 'email', 'date_joined',)
    ordering_fields = (
        'username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'date_joined',
    )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        password = request.data.get('password')
        if password:
            serializer.instance.set_password(password)
            serializer.instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

    @transaction.atomic
    @action(methods=["POST"], detail=True)
    def change_password(self, request, pk=None):
        instance = self.get_object()
        password = request.data.get('password')
        if not password:
            return Response({'detail': 'Укажите пароль'}, status=400)
        if instance.check_password(password):
            return Response({'detail': 'Пароль должен отличаться от старого пароля'}, status=400)
        instance.set_password(password)
        instance.save()
        return Response({'detail': 'Пароль умпешно изменен'}, status=200)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
