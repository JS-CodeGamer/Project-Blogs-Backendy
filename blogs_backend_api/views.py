import jwt
from .models import Blogs
from rest_framework import status
from .serializers import BlogSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from blogs_microservice.settings import SECRET_KEY
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, NotFound
from rest_framework_json_api.pagination import JsonApiPageNumberPagination as PageNumberPagination


# Create your views here.
@api_view(['GET'])
def allBlogs(request, format=None):
    return Response({
        'blogs' : reverse('allBlogs', request=request, format=format)
    })


@api_view(['GET'])
def blogsList(request):
    try:
        author = jwt.decode(request.headers['Authorization'].split(" ")[-1],
                            SECRET_KEY, algorithms=["HS256"])['username']
        blogs = Blogs.objects.filter(author=author).order_by('id')
    except:
        blogs = Blogs.objects.all().order_by('id')
    paginator = PageNumberPagination()
    try:
        paginator.page_size = int(request.data['page_size'])
    except:
        paginator.page_size = 10
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def blogsListUser(request, pk=None):
    blogs = Blogs.objects.filter(author=pk).order_by('id')
    if not pk or len(blogs) == 0:
        raise NotFound(detail="No Blogs found related to user")
    paginator = PageNumberPagination()
    try:
        paginator.page_size = int(request.data['page_size'])
    except:
        paginator.page_size = 10
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
def newBlog(request):
    try:
        author = jwt.decode(request.headers['Authorization'].split(" ")[-1],
                            SECRET_KEY, algorithms=["HS256"])['username']
    except Exception as e:
        raise NotAuthenticated(detail="User not signed in.")
    serializer = BlogSerializer(data=request.data)
    serializer.initial_data["author"] = author
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def blog(request, pk=None):
    if pk:
        try:
            user = jwt.decode(request.headers['Authorization'].split(" ")[-1],
                                SECRET_KEY, algorithms=["HS256"])['username']
        except:
            user = None
        blog = Blogs.objects.get(pk=pk)
        serializer = BlogSerializer(blog)
        # GET for getting
        if request.method == "GET":
            return Response(data={**serializer.data, 'edit':(user==serializer.data["author"])})
        if not user:
            raise NotAuthenticated(detail="User not signed in.")
        if serializer.data["author"] == user:
            # PUT for updating
            if request.method == "PUT" and request.data:
                serializer = BlogSerializer(blog, data = request.data, partial=True)
                serializer.initial_data["author"] = user
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            # DELETE for deleting
            elif request.method == "DELETE":
                blog.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif user:
            raise PermissionDenied()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
