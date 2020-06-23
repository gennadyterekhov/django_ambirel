from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.reverse import reverse
from rest_framework.renderers import JSONRenderer

# from djangorestframework.views import APIView
# from djangorestframework.response import Response
# from djangorestframework.authtoken.models import Token
# from djangorestframework import status
# from djangorestframework import generics
# from djangorestframework import permissions
# from djangorestframework import mixins
# from djangorestframework import renderers
# from djangorestframework.decorators import api_view, renderer_classes
# from djangorestframework.reverse import reverse
# from djangorestframework.renderers import JSONPRenderer, JSONRenderer


import json

from browserapi.models import ForumPost
from browserapi.serializers import ForumPostSerializer, UserSerializer
from browserapi import permissions as browserapiPermissions


# Display all APIs -------------------------------------------------

class ApiRoot(APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'forumPosts': reverse('forumPost-list', request=request, format=format)
        })



# User related APIs ------------------------------------------------

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user and request.DATA.get('password'):
            request.user.set_password(request.DATA.get('password'))
            request.user.save()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserCreate(APIView):
    #@csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            username = request.DATA.get('username')
            password = request.DATA.get('password')
            email = request.DATA.get('email')
            User.objects.create_user(username, email, password)
            #user = authenticate(username=username, password=password)
            ##login(request, user)
            #token = Token.objects.create(user=user)
            return _user_login(request, username, password, True)

        except IntegrityError:
            message = { 'error': 'That username already exists' }
            return HttpResponseBadRequest(json.dumps(message), mimetype='text/json')

        #responseData = { 'token': str(token) }
        #return HttpResponse(json.dumps(responseData))


#@api_view(['POST'])
#def UserLogin(request):
#    username = request.POST.get('username')
#    password = request.POST.get('password')
#    return _user_login(request, username, password)
class UserLogin(APIView):
    #@csrf_exempt
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        return _user_login(request, username, password)



# Post related APIs ------------------------------------------------

class ForumPostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class ForumPostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    permission_classes = (snippetsPermissions.IsOwner,)
    
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user



# Supporting Functions ---------------------------------------------

def _user_login(request, username, password, newUser=False):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            if newUser:
                token = Token.objects.create(user=user)
            else:
                try:
                    token = Token.objects.get(user=user)
                except ObjectDoesNotExist:
                    token = Token.objects.create(user=user)         # for some reason, the token doesn't exist

            response = HttpResponse(json.dumps({ 'token': str(token), 'id': user.id }))

            #if request.user.is_authenticated():
            #    response.status_code = status.HTTP_200_OK
            #else:
            #    response.status_code = status.HTTP_401_UNAUTHORIZED
            response.status_code = status.HTTP_200_OK

            return response

        else:
            return HttpResponseForbidden(content='Your account is not active.')
    else:
        return HttpResponseNotFound()



# Testing Pages ----------------------------------------------------

def UserLoginTest(request):
    return render(request, 'userLoginTest.html', { 'value': 'my value~~' })



