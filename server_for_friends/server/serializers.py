from rest_framework import serializers
from .models import User, Relation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', )


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('from_user', 'to_user', 'relation', )

