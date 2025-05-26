from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.equipments.serializers.inventory_equipment import InventoryEquipmentSerializer
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список инвентарного оборудования",
        description=(
            "Поддерживает фильтры:\n"
            "- `owner` — ID владельца\n"
            "- `status` — ID статуса\n"
            "- `location` — ID местоположения\n"
            "\nИ поиск по `name` или `inventory_number` через `?search=`."
        ),
        parameters=[
            OpenApiParameter("owner", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("status", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("location", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("search", str, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("page", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, required=False),
        ],
        responses={200: InventoryEquipmentSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали оборудования",
        responses={200: InventoryEquipmentSerializer, 404: OpenApiResponse(description="Не найдено")},
    ),
    create=extend_schema(
        summary="Создать оборудование",
        request=InventoryEquipmentSerializer,
        responses={
            201: OpenApiResponse(
                description="Создано",
                examples=[OpenApiExample(
                    "Пример",
                    value={
                        "id": 1,
                        "owner": 4,
                        "owner_username": "john",
                        "name": "Дрель Bosch",
                        "inventory_number": "EQ-001",
                        "location": 2,
                        "location_name": "Склад 1",
                        "status": 1,
                        "status_name": "В работе",
                        "description": "Аккумуляторная дрель",
                        "photo": None,
                        "registration_date": "2025-05-26",
                        "created_at": "2025-05-26",
                        "updated_at": "2025-05-26",
                    },
                )],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление оборудования"),
    partial_update=extend_schema(summary="Частичное обновление оборудования"),
    destroy=extend_schema(summary="Удалить оборудование"),
)
class InventoryEquipmentViewSet(viewsets.ModelViewSet):
    """
    CRUD-эндпоинт для **InventoryEquipment**.

    | Операция               | Model-permission |
    |------------------------|------------------|
    | list / retrieve        | `view_inventoryequipment` |
    | create                 | `add_inventoryequipment` |
    | update / partial_update| `change_inventoryequipment` |
    | destroy                | `delete_inventoryequipment` |
    """
    queryset = (
        InventoryEquipment.objects
        .select_related("owner", "status", "location")
        .order_by("id")
    )
    serializer_class = InventoryEquipmentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination

    # фильтры и поиск
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["owner", "status", "location"]
    search_fields = ["name", "inventory_number"]

    # при создании возвращаем сам объект (201)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        equip = serializer.save()
        return Response(
            InventoryEquipmentSerializer(equip).data,
            status=status.HTTP_201_CREATED,
        )
