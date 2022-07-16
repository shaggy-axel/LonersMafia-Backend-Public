from django.forms import ValidationError
from rest_framework import serializers, status

from utils.customserializers import DynamicFieldsModelSerializer

from . import models
from user.models import User


class SpaceSerializer(DynamicFieldsModelSerializer):

    rules = serializers.SerializerMethodField()
    mods = serializers.SerializerMethodField()

    class Meta:

        model = models.Space
        exclude = ('created_by', 'created_datetime')
        extra_kwargs = {
            'created_by': {'read_only': True}
        }

    def validate(self, attrs):

        if 'name' in attrs:

            attrs['name'] = attrs['name'].strip()
            
            if len(attrs['name']) < 3:
                raise ValidationError('must have atleast 3 characters')

        return super().validate(attrs)

    def get_rules(self, obj):
        """
            gets the rules for the space
        """
        return RuleSerializer(models.Rule.objects.filter(space=obj), many=True).data

    def get_is_staff(self, obj):
        """
            returns if the user is staff 
        """
        return User.objects.filter(id=self.context['request'].id, staff=True).exists()

    def get_mods(self, obj):
        """
            gets moderators of the space
        """
        return ModeratorSerializer(models.Moderator.objects.filter(space=obj), many=True).data

    def is_mod(self, obj):
        """
            returns true if the user is a modertor
        """

        return models.Moderator.objects.filter(space=obj, user=self.context['request'].user.id).exists()


class RuleSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Rule
        fields = '__all__'


class ModeratorSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Moderator
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    is_staff = serializers.SerializerMethodField() # lets user know if the message is from staff/moderator
    is_mod = serializers.SerializerMethodField() # lets user know if the message is from mod

    # reactions_count = serializers.SerializerMethodField()
    # reactions = serializers.SerializerMethodField()

    class Meta:

        model = models.Message
        fields = '__all__'

        extra_kwargs = {
            'datetime': {'read_only': True},
            'user': {'read_only': True},
        }

    def get_is_mod(self, obj):
        """
            returns true if the user is a modertor
        """
        return models.Moderator.objects.filter(space=obj.space, user=self.context['request'].user.id).exists()

    def get_is_staff(self, obj):
        """
            returns if the user is staff 
        """
        return User.objects.filter(id=self.context['request'].user.id, is_staff=True).exists()


    # def get_reactions(self, obj):

    #     """
    #         gets the list of reaction by the user
    #     """
    #     return ReactionSerializer(Reaction.objects.filter()).data


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Reaction
        fields = '__all__'

    def validate(self, attrs):

        if models.Reaction.objects.filter(user=self.context['request'].user, 
                            message=attrs['id'], reaction=attrs['reaction']).exists():
            
            raise ValidationError('The user has already reacted to this message', code=status.HTTP_400_BAD_REQUEST)

        return super().validate(attrs)