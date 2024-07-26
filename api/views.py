from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser

from .models import Blog
from .serializers import BlogSerializer


# Create your views here.
# class BlogViewSet(viewsets.ModelViewSet):
#     queryset = Blog.objects.all().order_by('pub_date')
#     serializer_class = BlogSerializer
#

@api_view(['GET', 'POST'])
# @permission_classes([permissions.AllowAny])
def blog_list(request, format=None):
    if request.method == 'GET':
        # filtering based on title, author and date published
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        pub_date = request.query_params.get('published_date', None)

        if title:
            blogs = Blog.objects.filter(title__icontains=title)
        elif author and pub_date:
            blogs = Blog.objects.all().filter(author__icontains=author, pub_date__date=pub_date)
        elif author:
            blogs = Blog.objects.all().filter(author__icontains=author)
        elif pub_date:
            blogs = Blog.objects.all().filter(pub_date__date=pub_date)
        else:
            blogs = Blog.objects.all()

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data.__reversed__())

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BlogSerializer(blog, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)