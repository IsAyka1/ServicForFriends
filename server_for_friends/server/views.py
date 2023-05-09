from typing import Tuple

from django.db.models import Q
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from . import models
from .serializers import UserSerializer, RelationSerializer

user_param = openapi.Parameter('id', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='User ID')
user_to_param = openapi.Schema(type=openapi.TYPE_OBJECT, required=['to_id'],
                               description='User ID to interact',
                               properties={
                                   'to_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid')
                               })
user_from_param = openapi.Schema(type=openapi.TYPE_OBJECT, required=['from_id'],
                                 description='User ID whose requested',
                                 properties={
                                     'from_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid')
                                 })


def _get_user(request, id_attr: str) -> models.User:
    user_id = request.headers.get(id_attr, None)
    user = get_object_or_404(models.User, id=user_id)

    return user


class UserViewset(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = models.User.objects.all()

    def list(self, request):
        """List of all users"""
        queryset = models.User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create new user"""
        name = request.data.get('name', None)
        if name:
            user = models.User.objects.create(name=name)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        """Delete user"""
        user = get_object_or_404(models.User, id=id)
        user.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[user_param],
                         operation_description='List of friends of user',
                         responses={'200': 'Successfully fetched all friends of user',
                                    '404': 'User not found'})
    @action(detail=False, methods=['get'])
    def friends(self, request):
        user = _get_user(request, id_attr='id')

        query = Q(from_user=user)
        query.add(Q(to_user=user), Q.OR)
        query.add(Q(relation=models.FRIEND), Q.AND)
        friends_relations = models.Relation.objects.filter(query)
        all_friends = []
        for relation in friends_relations:
            if relation.from_user == user:
                all_friends.append(relation.to_user)
            elif relation.to_user == user:
                all_friends.append(relation.from_user)

        serializer = UserSerializer(all_friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[user_param],
                         operation_description='List of friends of user',
                         responses={'200': 'Successfully fetched all incoming requestes of user',
                                    '404': 'User not found'})
    @action(detail=False, methods=['get'])
    def incoming(self, request):
        user = _get_user(request, id_attr='id')

        requests_relations = models.Relation.objects.filter(to_user=user, relation=models.REQUEST)
        request_users = [relation.from_user for relation in requests_relations]
        serializer = UserSerializer(request_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[user_param],
                         operation_description='List of friends of user',
                         responses={'200': 'Successfully fetched all outgoing requestes of user',
                                    '404': 'User not found'})
    @action(detail=False, methods=['get'])
    def outgoing(self, request):
        user = _get_user(request, id_attr='id')

        requests_relations = models.Relation.objects.filter(from_user=user, relation=models.REQUEST)
        request_users = [relation.to_user for relation in requests_relations]
        serializer = UserSerializer(request_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RelationViewset(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = RelationSerializer
    queryset = models.Relation.objects.all()

    def list(self, request):
        """List of all relations"""
        queryset = models.Relation.objects.all()
        serializer = RelationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[user_param], request_body=user_to_param,
                         operation_description='Send friend request to user',
                         responses={'201': 'Request send',
                                    '202': 'You are friends now',
                                    '404': 'User not found',
                                    '409': 'Request is already sended'})
    @action(detail=False, methods=['post'])
    def send_request(self, request):
        from_user, to_user = self.__get_from_to_users(request)

        already_requested = models.Relation.objects.filter(from_user=to_user, to_user=from_user).first()
        if already_requested:
            already_requested.relation = models.FRIEND
            already_requested.save()
            relation = already_requested
            stat = status.HTTP_202_ACCEPTED
        else:
            already_requested = models.Relation.objects.filter(from_user=from_user, to_user=to_user).first()
            if already_requested:
                return Response(status=status.HTTP_409_CONFLICT)
            relation = models.Relation.objects.create(from_user=from_user, to_user=to_user, relation=models.REQUEST)
            stat = status.HTTP_201_CREATED

        serializer = RelationSerializer(relation)

        return Response(serializer.data, status=stat)

    @swagger_auto_schema(manual_parameters=[user_param], request_body=user_to_param,
                         operation_description='Accept friend request from another user',
                         responses={'200': 'Request to be friends is accepted',
                                    '404': 'User not found'})
    @action(detail=False, methods=['patch'])
    def accept_request(self, request):
        from_user, to_user = self.__get_from_to_users(request)

        requested = models.Relation.objects.filter(from_user=from_user, to_user=to_user).first()
        if not requested:
            return Response(status=status.HTTP_404_NOT_FOUND)

        requested.relation = models.FRIEND
        requested.save()

        serializer = RelationSerializer(requested)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[user_param], request_body=user_from_param,
                         operation_description='Deny friend request from another user',
                         responses={'204': 'Request to be friends is denied',
                                    '404': 'User not found'})
    @action(detail=False, methods=['patch'])
    def deny_request(self, request):
        user, from_user = self.__get_from_to_users(request, id_body_attr='from_id')

        requested = models.Relation.objects.filter(from_user=from_user, to_user=user).first()
        if not requested:
            return Response(status=status.HTTP_404_NOT_FOUND)

        requested.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(manual_parameters=[user_param], request_body=user_to_param,
                         operation_description='Delete user from friends',
                         responses={'204': 'User successfully deleted from friends',
                                    '404': 'User not found'})
    @action(detail=False, methods=['patch'])
    def delete_friend(self, request):
        from_user, to_user = self.__get_from_to_users(request)

        query = Q(from_user=from_user, to_user=to_user)
        query.add(Q(from_user=to_user, to_user=from_user), Q.OR)
        query.add(Q(relation=models.FRIEND), Q.AND)
        requested = models.Relation.objects.filter(query).first()

        if not requested:
            return Response(status=status.HTTP_404_NOT_FOUND)

        requested.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(manual_parameters=[user_param], request_body=user_to_param,
                         operation_description='Check if users are friends or requested or not friends',
                         responses={'200': 'Relations successfully found',
                                    '404': 'User not found'})
    @action(detail=False, methods=['post'])
    def check_relation(self, request):
        user, to_user = self.__get_from_to_users(request)

        query = Q(from_user=user, to_user=to_user)
        query.add(Q(from_user=to_user, to_user=user), Q.OR)
        relation = models.Relation.objects.filter(query).first()

        answer = 'nothing'
        if relation:
            if relation.relation == models.FRIEND:
                answer = relation.display_relation()
            elif relation.relation == models.REQUEST:
                answer = 'incoming request' if relation.from_user == user else 'outgoing request'

        return Response(data={'relation': answer}, status=status.HTTP_200_OK)

    def __get_from_to_users(self, request, id_body_attr='to_id') -> Tuple[models.User, models.User]:
        from_user = _get_user(request, id_attr='id')
        to_user_id = request.data.get(id_body_attr, None)
        to_user = get_object_or_404(models.User, id=to_user_id)

        return from_user, to_user


def index(request):
    return HttpResponse("Hello, world. You're at the social club.")


__all__ = ['UserViewset', 'RelationViewset']
