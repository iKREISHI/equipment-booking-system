from rest_framework import viewsets, status
from rest_framework.decorators import action
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
from apps.users.serializers.user import UserSerializer, SetActiveSerializer
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

    # ------------------------------------------------------------------ #
    # выбор сериализатора
    # ------------------------------------------------------------------ #
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action == "set_active":
            return SetActiveSerializer
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

        # ------------------------------------------------------------------ #
        # PATCH /users/{id}/set-active/  — включить / отключить пользователя
        # ------------------------------------------------------------------ #
    @extend_schema(
            summary="Изменить флаг is_active",
            description=(
                    "Позволяет включить или выключить пользователя. "
                    "Требуются права `change_user` и принадлежность к разрешённой группе."
            ),
            request=SetActiveSerializer,
            responses={
                200: OpenApiResponse(
                    description="Статус is_active изменён",
                    examples=[
                        OpenApiExample(
                            "Пример ответа",
                            value={
                                "detail": "Статус обновлён",
                                "user_id": 42,
                                "username": "johndoe",
                                "is_active": False
                            },
                        )
                    ],
                ),
                400: OpenApiResponse(description="Ошибка валидации"),
                403: OpenApiResponse(description="Нет прав доступа"),
                404: OpenApiResponse(description="Пользователь не найден"),
            },
    )
    @action(detail=True, methods=["patch"], url_path="set-active")
    def set_active(self, request, pk=None):
        """Изменить поле `is_active` у выбранного пользователя."""
        user = self.get_object()  # 404 + checks IsSuperuserOrSystemAdmin
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.is_active = serializer.validated_data["is_active"]
        user.save(update_fields=["is_active"])

        return Response(
        {
                "detail": "Статус обновлён",
                "user_id": user.id,
                "username": user.username,
                "is_active": user.is_active,
            },
            status=status.HTTP_200_OK,
        )
