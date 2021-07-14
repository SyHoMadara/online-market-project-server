from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api2application.api.serializers import UserSerializer
from ..models import User


@api_view(['GET', 'UPDATE', ])
def user_view(request, email):
    if request.method == 'GET':
        return get_user_view(request, email)
    elif request.method == 'UPDATE':
        return update_user_view(request, email)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_user_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['UPDATE', ])
def update_user_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {'type': list()}
    this_status = None
    password = request.data['password']
    if password is None and password != user.password:
        data['error'].append('PASSWORD_PROBLEM')
        this_status = status.HTTP_403_FORBIDDEN
        return Response(data=data, status=this_status)

    serialize = UserSerializer(user, data=request.data)
    if serialize.is_valid():
        data['success'].append('UPDATE_SUCCESS')
        serialize.save()
        this_status = status.HTTP_202_ACCEPTED
        return Response(data=data, status=this_status)
    else:
        data['error'].append('DATA_NOT_VALID')
        this_status = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=this_status)
