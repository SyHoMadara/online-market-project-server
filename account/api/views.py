from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializer import UserSerializer
from ..models import User

OK = status.HTTP_200_OK
BAD_REQUEST = status.HTTP_400_BAD_REQUEST


@api_view(['GET', 'PUT', 'DELETE'])
def user_view(request, email):
    method = request.method
    if method == 'GET':
        return get_user_view(request, email)
    elif method == 'PUT':
        return update_user_view(request, email)
    elif method == 'DELETE':
        return delete_user_view(request, email)
    else:
        return Response(status=BAD_REQUEST)


def get_user_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=OK)


def update_user_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {'error': list(), 'success': list()}
    # todo provide update data if password wasn't correct
    # password = request.data['password']
    # if password is None or password != user.password:
    #     data['error'].append('PASSWORD_PROBLEM')
    #     this_status = status.HTTP_403_FORBIDDEN
    #     return Response(data=data, status=this_status)

    serialize = UserSerializer(user, data=request.data)
    if serialize.is_valid():
        data['success'].append('UPDATE_SUCCESS')
        serialize.save()
        this_status = OK
        return Response(data=data, status=this_status)
    else:
        data['error'].append('DATA_NOT_VALID')
        this_status = BAD_REQUEST
    return Response(data=data, status=this_status)


def delete_user_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {'error': list(), 'success': list()}
    del_success = user.delete()
    if del_success:
        data['success'].append('DELETE_SUCCESS')
        this_status = OK
    else:
        data['error'].append('DELETE_FAILED')
        this_status = BAD_REQUEST
    return Response(status=this_status, data=data)

