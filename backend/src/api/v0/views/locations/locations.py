from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiResponse, OpenApiExample
)

from apps.locations.models import Location                  # поправьте путь, если иной
from apps.locations.serializers.locations import LocationSerializer
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список местоположений",
        parameters=[
            OpenApiParameter("page", int, OpenApiParameter.QUERY,
                             description="Номер страницы (≥ 1)"),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY,
                             description="Размер страницы (по умолчанию 20, максимум 100)"),
        ],
        responses={200: LocationSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали местоположения",
        responses={
            200: LocationSerializer,
            404: OpenApiResponse(description="Не найдено"),
        },
    ),
    create=extend_schema(
        summary="Создать местоположение",
        request=LocationSerializer,
        responses={
            201: OpenApiResponse(
                description="Создано",
                examples=[OpenApiExample(
                    "Пример ответа",
                    value={
                        "id": 10,
                        "name": "Склад №2",
                        "description": "Склад на втором этаже"
                    },
                )],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление"),
    partial_update=extend_schema(summary="Частичное обновление"),
    destroy=extend_schema(summary="Удалить местоположение"),
)
class LocationViewSet(viewsets.ModelViewSet):
    """
    Полноценный CRUD для *Location*.

    | Операция  | Требуемое model-permission |
    |-----------|---------------------------|
    | list / retrieve | `view_location` |
    | create | `add_location` |
    | update / partial_update | `change_location` |
    | destroy | `delete_location` |
    """
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination

    # При создании возвращаем 201 и сам объект
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = serializer.save()
        return Response(
            LocationSerializer(location).data,
            status=status.HTTP_201_CREATED,
        )
