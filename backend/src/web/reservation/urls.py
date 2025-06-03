from django.urls import path
from web.reservation.views.reservation import ReservationListView, ReservationCreateView, ReservationUpdateView, \
    ReservationDeleteView

urlpatterns = [
    path("", ReservationListView.as_view(), name="reservation_list"),
    path("create/", ReservationCreateView.as_view(), name="reservation_create"),
    path("update/<int:pk>/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("delete/<int:pk>/", ReservationDeleteView.as_view(), name="reservation_delete"),
]