from rest_framework import serializers
from django.contrib.auth import get_user_model 
from .models import Blog



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model= get_user_model()
        fields =["id", "email","username","first_name", "last_name","bio","profile_picture", "facebook", "instagram", "youtube", "twitter" ]


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields =["id", "email","username", "first_name","last_name","password"]
        extra_kwargs ={
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        password= validated_data["password"]
        
        user = get_user_model()
        new_user = user.objects.create(
            email=email,
            username= username,
            first_name = first_name,
            last_name= last_name
            )
        new_user.set_password(password)
        new_user.save()
        return new_user
    
    
    
class SimlpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name","profile_picture"]
    
class BlogSerializer(serializers.ModelSerializer):
    author = SimlpleAuthorSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "title", "slug", "content","author", "category", "feature_image", "is_draft","created_at","published_date"]
        
    
    