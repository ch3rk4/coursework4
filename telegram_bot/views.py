from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TelegramUser
from .serializers import TelegramUserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def connect_telegram(request):
    """Подключение Telegram к аккаунту."""
    chat_id = request.data.get('chat_id')
    if not chat_id:
        return Response(
            {'error': 'chat_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    telegram_user, created = TelegramUser.objects.get_or_create(
        user=request.user,
        defaults={'telegram_chat_id': chat_id}
    )

    if not created:
        telegram_user.telegram_chat_id = chat_id
        telegram_user.is_active = True
        telegram_user.save()

    serializer = TelegramUserSerializer(telegram_user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disconnect_telegram(request):
    """Отключение Telegram от аккаунта."""
    try:
        telegram_user = TelegramUser.objects.get(user=request.user)
        telegram_user.is_active = False
        telegram_user.save()
        return Response({'message': 'Telegram disconnected'})
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'Telegram not connected'},
            status=status.HTTP_404_NOT_FOUND
        )