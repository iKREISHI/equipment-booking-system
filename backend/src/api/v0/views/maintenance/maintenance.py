from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from apps.maintenance.models.maintenance import Maintenance
from apps.maintenance.serializers import MaintenanceSerializer
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список записей обслуживания оборудования",
        parameters=[
            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Номер страницы (≥ 1)"
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Размер страницы (по умолчанию 20, максимум 100)",
            ),
        ],
        responses={200: MaintenanceSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали одной записи обслуживания",
        responses={
            200: MaintenanceSerializer,
            404: OpenApiResponse(description="Не найдено")
        },
    ),
    create=extend_schema(
        summary="Создать новую запись обслуживания",
        request=MaintenanceSerializer,
        responses={
            201: OpenApiResponse(
                description="Создано",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 5,
                            "equipment": 12,
                            "equipment_display": "Printer A1",
                            "reporter_by": 3,
                            "reporter_display": "ivanov",
                            "assigned_by": 4,
                            "assigned_display": "petrov",
                            "description": "Проверка принтера",
                            "status": 2,
                            "status_display": "В процессе",
                            "created_at": "2025-05-31T10:15:00Z",
                            "updated_at": "2025-05-31T10:15:00Z",
                            "description_updated": "",
                            "start_time": "2025-05-31T11:00:00Z",
                            "end_time": "2025-05-31T12:00:00Z"
                        }
                    )
                ],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление записи обслуживания"),
    partial_update=extend_schema(summary="Частичное обновление записи обслуживания"),
    destroy=extend_schema(summary="Удалить запись обслуживания"),
)
class MaintenanceViewSet(viewsets.ModelViewSet):
    """
    CRUD-эндпоинт для модели **Maintenance**.

    | Операция               | Требуемая permission                 |
    |------------------------|--------------------------------------|
    | list / retrieve        | `view_maintenance`                   |
    | create                 | `add_maintenance`                    |
    | update / partial_update| `change_maintenance`                 |
    | destroy                | `delete_maintenance`                 |
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    queryset = Maintenance.objects.all().order_by("-created_at")
    serializer_class = MaintenanceSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.view_maintenance'):
            # если анонимный, IsAuthenticated упадёт раньше → 401,
            # иначе нет нужного perm → 403
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.view_maintenance'):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.add_maintenance'):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        maintenance_obj = serializer.save()
        return Response(
            MaintenanceSerializer(maintenance_obj).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.change_maintenance'):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.change_maintenance'):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('maintenance.delete_maintenance'):
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
