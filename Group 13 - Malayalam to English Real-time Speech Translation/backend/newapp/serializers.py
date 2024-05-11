from django.contrib.auth.models import User
from newapp.models import Chat, Favourite
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user 


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "sender", "receiver"]
        extra_kwargs = {"sender": {"read_only": True}}


class FavouriteSerializer(serializers.ModelSerializer):
    # Serializer field for displaying username instead of ID
    favourite_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Favourite
        fields = ["id", "user", "favourite_user", "favourite_user_id"]
        extra_kwargs = {
            "user": {"read_only": True}
        }
