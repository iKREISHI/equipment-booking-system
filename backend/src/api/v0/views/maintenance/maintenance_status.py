from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from apps.maintenance.models import MaintenanceStatus
from apps.maintenance.serializers import MaintenanceStatusSerializer
from api.v0.core.pagination import StandardResultsSetPagination


class AuthenticatedDjangoModelPermissions(DjangoModelPermissions):
    """
    Сначала проверяем, что пользователь аутентифицирован,
    иначе бросаем NotAuthenticated (401).
    Затем — стандартная проверка model-permissions,
    в случае провала которой получается PermissionDenied (403).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        return super().has_permission(request, view)


@extend_schema_view(
    list=extend_schema(
        summary="Список статусов обслуживания оборудования",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY, description="Номер страницы (≥ 1)"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, description="Размер страницы (по умолчанию 20, максимум 100)"),
        ],
        responses={200: MaintenanceStatusSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали статуса обслуживания оборудования",
        responses={
            200: MaintenanceStatusSerializer,
            404: OpenApiResponse(description="Не найдено")
        },
    ),
    create=extend_schema(
        summary="Создать статус обслуживания оборудования",
        request=MaintenanceStatusSerializer,
        responses={
            201: OpenApiResponse(
                description="Создано",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 3,
                            "name": "В ремонте",
                            "description": "Оборудование находится в процессе ремонта"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление статуса обслуживания оборудования"),
    partial_update=extend_schema(summary="Частичное обновление статуса обслуживания оборудования"),
    destroy=extend_schema(summary="Удалить статус обслуживания оборудования"),
)
class MaintenanceStatusViewSet(viewsets.ModelViewSet):
    """
    CRUD эндпоинт для **MaintenanceStatus**.

    | Операция               | Требуемая permission                         |
    |------------------------|----------------------------------------------|
    | list / retrieve        | `view_maintenancestatus`                    |
    | create                 | `add_maintenancestatus`                     |
    | update / partial_update| `change_maintenancestatus`                  |
    | destroy                | `delete_maintenancestatus`                  |
    """
    # используем сессионную и базовую аутентификацию
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # наш кастомный класс, обеспечивающий 401 для анонимных, 403 для без прав
    permission_classes = [AuthenticatedDjangoModelPermissions]

    queryset = MaintenanceStatus.objects.all().order_by("id")
    serializer_class = MaintenanceStatusSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_obj = serializer.save()
        return Response(
            MaintenanceStatusSerializer(status_obj).data,
            status=status.HTTP_201_CREATED,
        )
