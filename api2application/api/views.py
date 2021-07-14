from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from ..models import User


@api_view(['GET', ])
def api_details_user_view(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            raise Response(status=status.HTTP_400_BAD_REQUEST)
