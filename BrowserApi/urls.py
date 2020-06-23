from django.conf.urls import include, url
from django.contrib import admin
from browserapi import views


# Admin
# admin.autodiscover()


urlpatterns = [
    # BrowserAPI
 	url(r'^$', views.ApiRoot.as_view(), name='api-root'),

    url(r'^forum_posts/$', views.ForumPostList.as_view(), name='forumPost-list'),
    url(r'^forum_posts/(?P<pk>[0-9]+)/$', views.ForumPostDetail.as_view(), name='forumPost-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/create/$', views.UserCreate.as_view(), name='user-create'),
    url(r'^users/login/$', views.UserLogin.as_view(), name='user-login'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    url(r'^admin/', admin.site.urls),

    # Testing
    url(r'^userLoginTest', views.UserLoginTest, name='user-login-test'),
]
