from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.users.models import User
from apps.users.serializers.registration import UserRegistrationSerializer


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Регистрация нового пользователя.

    После успешного создания аккаунт помечается как `is_active=False`
    (это делает сам сериализатор)
    """
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    @extend_schema(
        summary="Регистрация пользователя",
        responses={
            201: OpenApiResponse(
                description="Аккаунт создан (по умолчанию не активен)",
                examples=[
                    {
                        "detail": "Регистрация прошла успешно. Подтвердите e-mail.",
                        "user_id": 42,
                        "username": "new_user"
                    }
                ],
            ),
            400: OpenApiResponse(
                description="Ошибки валидации данных"
            ),
        },
    )
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
