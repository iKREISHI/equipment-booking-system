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

from apps.equipments.models import InventoryEquipmentStatus
from apps.equipments.serializers.inventory_equipment_status import (
    InventoryEquipmentStatusSerializer,
)
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список статусов оборудования",
        parameters=[
            OpenApiParameter(
                "page", int, OpenApiParameter.QUERY, description="Номер страницы (≥ 1)"
            ),
            OpenApiParameter(
                "page_size",
                int,
                OpenApiParameter.QUERY,
                description="Размер страницы (по умолчанию 20, максимум 100)",
            ),
        ],
        responses={200: InventoryEquipmentStatusSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали статуса",
        responses={200: InventoryEquipmentStatusSerializer, 404: OpenApiResponse(description="Не найдено")},
    ),
    create=extend_schema(
        summary="Создать статус",
        request=InventoryEquipmentStatusSerializer,
        responses={
            201: OpenApiResponse(
                description="Создано",
                examples=[OpenApiExample(
                    "Пример ответа",
                    value={"id": 3, "name": "В ремонте"},
                )],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление статуса"),
    partial_update=extend_schema(summary="Частичное обновление статуса"),
    destroy=extend_schema(summary="Удалить статус"),
)
class InventoryEquipmentStatusViewSet(viewsets.ModelViewSet):
    """
    CRUD эндпоинт для **InventoryEquipmentStatus**.

    | Операция               | Требуемая permission |
    |------------------------|----------------------|
    | list / retrieve        | `view_inventoryequipmentstatus` |
    | create                 | `add_inventoryequipmentstatus` |
    | update / partial_update| `change_inventoryequipmentstatus` |
    | destroy                | `delete_inventoryequipmentstatus` |
    """
    queryset = InventoryEquipmentStatus.objects.all().order_by("id")
    serializer_class = InventoryEquipmentStatusSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination

    # При создании возвращаем 201 + сам объект
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_obj = serializer.save()

        return Response(
            InventoryEquipmentStatusSerializer(status_obj).data,
            status=status.HTTP_201_CREATED,
        )
