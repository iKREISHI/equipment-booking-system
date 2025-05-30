from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiResponse, OpenApiExample
)

from apps.reservations.models import Reservation
from apps.reservations.serializers.reservations import ReservationSerializer
from api.v0.core.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(
        summary="Список бронирований",
        description=(
            "Фильтры по полям `equipment`, `renter`, `assigned_by`, `location`.\n"
            "Поиск по описанию через `?search=`.\n"
            "Постраничная отдача."
        ),
        parameters=[
            OpenApiParameter("equipment", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("renter", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("assigned_by", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("location", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("search", str, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("page", int, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY, required=False),
        ],
        responses={200: ReservationSerializer},
    ),
    retrieve=extend_schema(
        summary="Детали бронирования",
        responses={200: ReservationSerializer, 404: OpenApiResponse(description="Не найдено")},
    ),
    create=extend_schema(
        summary="Создать бронирование",
        request=ReservationSerializer,
        responses={
            201: OpenApiResponse(
                description="Бронирование создано",
                examples=[OpenApiExample(
                    "Пример ответа",
                    value={
                        "id": 5,
                        "equipment": 3,
                        "equipment_name": "Дрель Bosch",
                        "renter": 7,
                        "renter_username": "ivan",
                        "assigned_by": 1,
                        "assigned_by_username": "admin",
                        "location": 2,
                        "location_name": "Склад A",
                        "start_time": "2025-05-29T10:00:00Z",
                        "end_time": "2025-05-29T12:00:00Z",
                        "actual_return_time": None,
                        "description": "На тестовый монтаж",
                    },
                )],
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    ),
    update=extend_schema(summary="Полное обновление бронирования", request=ReservationSerializer),
    partial_update=extend_schema(summary="Частичное обновление бронирования", request=ReservationSerializer),
    destroy=extend_schema(summary="Удалить бронирование"),
)
class ReservationViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели Reservation (аренды оборудования).

    • list/retrieve — право `view_reservation`
    • create         — право `add_reservation`
    • update/patch   — право `change_reservation`
    • destroy        — право `delete_reservation`
    """
    queryset = Reservation.objects.select_related(
        "equipment", "renter", "assigned_by", "location"
    ).order_by("-start_time")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["equipment", "renter", "assigned_by", "location"]
    search_fields = ["description"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()
        return Response(
            ReservationSerializer(res).data,
            status=status.HTTP_201_CREATED
        )
