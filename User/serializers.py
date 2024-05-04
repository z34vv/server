from rest_framework import serializers
from .models import User, Bag, Item, BagItem
import re


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['item_id',
                  'item_name',
                  'item_image',
                  'price',
                  'updated_at',
                  'created_at',
                  'deleted_at']


class BagItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)

    class Meta:
        model = BagItem
        fields = [
            'item',
            'quantity'
        ]


class BagSerializer(serializers.ModelSerializer):
    item = BagItemSerializer(many=True)

    class Meta:
        model = Bag
        fields = ['bag_id', 'user', 'sapphire', 'item']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id',
                  'username',
                  'email',
                  'phone',
                  'last_name',
                  'first_name',
                  'password',

                  # Profile
                  'view_timeline_permission',
                  'avatar',
                  'background',
                  'day_of_birth',
                  'age',
                  'gender',
                  'story',
                  'relationship',
                  'hometown',
                  'school',
                  'hobby',

                  'friends', 'friend_quantity',
                  'follows', 'follow_quantity',
                  'followers', 'follower_quantity',
                  'idols', 'idol_quantity',
                  'fans', 'fan_quantity',

                  # Social Title
                  # 'businessmen_rank',
                  # 'popularity_rank',
                  # 'artist_rank',
                  # 'aristocrat_rank',
                  # 'is_abaddoner',
                  # 'is_universeExplorer',
                  # 'is_globeTrotter',
                  'is_active',
                  'is_superuser',
                  'is_staff',

                  'created_at',
                  'updated_at',
                  'deleted_at',]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance

    read_only_fields = ('user_id',
                        'age',
                        'friend_quantity',
                        'follow_quantity',
                        'follower_quantity',
                        'idol_quantity',
                        'fan_quantity',
                        # 'businessmen_rank',
                        # 'popularity_rank',
                        # 'artist_rank',
                        # 'aristocrat_rank',
                        # 'is_abaddoner',
                        # 'is_universeExplorer',
                        # 'is_globeTrotter',
                        'created_at')


class DemoUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id',
                  'username',
                  'view_timeline_permission',
                  'avatar',
                  'background',
                  'friend_quantity',
                  'follow_quantity',
                  'follower_quantity',
                  'idol_quantity',
                  'fan_quantity',
                  ]
