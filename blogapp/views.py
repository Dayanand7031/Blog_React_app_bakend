from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, BlogSerializer, UserProfileUpdateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Blog

from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(["POST"])
def register_user(request):
    serializer = RegisterSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    return Response(
        {"username": request.user.username},
        status=status.HTTP_200_OK
    )

@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def update_user_profile(request):
    user =request.user
    serializer = UserProfileUpdateSerializer(user,data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




User = get_user_model()

@api_view(["GET"])
def get_user_info(request, username):
    user = get_object_or_404(User, username=username)

    user_serializer = UserProfileUpdateSerializer(user)

    blogs = Blog.objects.filter(author=user).order_by("-created_at")
    blog_serializer = BlogSerializer(blogs, many=True)

    return Response({
        **user_serializer.data,
        "author_posts": blog_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def create_blog(request):
    serializer = BlogSerializer(data= request.data)
    
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_blog(request):
    paginator = PageNumberPagination()
    paginator.page_size = 2
    
    blogs = Blog.objects.all().order_by("-created_at")
    result_page = paginator.paginate_queryset(blogs, request)

    serializer = BlogSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def get_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET","PUT"])
@permission_classes([IsAuthenticated])
def blog_update(request,pk):
    user =request.user
    blog = Blog.objects.get(pk=pk)
    
    if blog.author != user:
        return Response({"error":"you are not the not the Author of this blog "},status=status.HTTP_403_FORBIDDEN)
    
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(["DELETE"])
def blog_delete(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    serializer = BlogSerializer(blog, data= request.data)
    
    if blog.author != user:
       return Response({"error":"you are not the not the Author of this blog "},status=status.HTTP_403_FORBIDDEN)    
    
    blog.delete()
    return Response({"message":"blog is deleted succesfully"})