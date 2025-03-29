from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group


User = get_user_model() 


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','password','first_name', 'last_name','username')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(email=email, password=password, **validated_data)
        return user

class UserSerailizerViewset(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'user_type', 'user_subtype', 'email', 'enterprise_name', 'profile_id')

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'phone',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style = { 'input_type': 'password'}, trim_whitespace = False
    )
    
    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        
        if phone and password:
            if User.objects.filter(username = phone).exists():
                user = authenticate(request = self.context.get('request'), username = phone, password = password)
                # print(user)

            else:
                msg = {
                    'detail' : 'Phone number not found',
                    'status' : False,
                }    
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail' : 'Phone number and password not matching. Try again',
                    'status' : False,
                }    
                raise serializers.ValidationError(msg, code = 'authorization')

        
        else:
            msg = {
                    'detail' : 'Phone number and password not found in request',
                    'status' : False,
                }    
            raise serializers.ValidationError(msg, code = 'authorization')

        data['user'] = user
        return data    



