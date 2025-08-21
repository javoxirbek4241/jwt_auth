from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'age', 'email', 'address', 'password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password is None or password2 is None:
            raise ValidationError('parollar toliq kiritilmadi')
        if password!=password2:
            raise ValidationError('Parollar mos emas')
        return data


    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            address=validated_data.get('address', None),
            age=validated_data.get('age', None)
        )
        return user