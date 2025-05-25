from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from apps.users.models import User
from apps.users.serializers.user import UserSerializer
from apps.users.serializers.registration import UserRegistrationSerializer
from apps.users.permission import IsSuperuserOrSystemAdmin
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список пользователей",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Номер страницы (≥ 1)"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY,
                             description="Размер страницы (по умолчанию 20, максимум 100)"),
        ],
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="Пагинированный список пользователей"
            ),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
    ),
    retrieve=extend_schema(
        summary="Детальная информация о пользователе",
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="Пользователь не найден"),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
    ),
    create=extend_schema(
        summary="Создать пользователя",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                description="Пользователь создан (не активен, ожидает подтверждения)",
                examples=[
                    OpenApiExample(
                        "Успешное создание",
                        value={
                            "detail": "Регистрация прошла успешно. Подтвердите e-mail.",
                            "user_id": 42,
                            "username": "new_user"
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
            403: OpenApiResponse(description="Нет прав доступа"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление пользователя",
        request=UserSerializer,
        responses={200: UserSerializer, 400: OpenApiResponse(description="Ошибки"), 403: OpenApiResponse(description="Нет прав доступа")},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление пользователя",
        request=UserSerializer,
        responses={200: UserSerializer, 400: OpenApiResponse(description="Ошибки"), 403: OpenApiResponse(description="Нет прав доступа")},
    ),
    destroy=extend_schema(
        summary="Удалить пользователя",
        responses={204: OpenApiResponse(description="Удалено"), 403: OpenApiResponse(description="Нет прав доступа")},
    ),
)
class UserAdminViewSet(viewsets.ModelViewSet):
    """
    **Полноценный CRUD для пользователей**.

    Доступ имеют:
    * суперпользователи;
    * члены групп **«Администратор системы»** или **«Модератор»**.
    """
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsSuperuserOrSystemAdmin]
    pagination_class = StandardResultsSetPagination

    # --------------------------------------------------------------------- #
    # сериализаторы
    # --------------------------------------------------------------------- #
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        return UserSerializer

    # --------------------------------------------------------------------- #
    # create: возвращаем кастомный ответ (detail + id + username)
    # --------------------------------------------------------------------- #
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "detail": "Регистрация прошла успешно. Подтвердите e-mail.",
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )
