from django.conf.urls import include
from django.conf.urls import url
from blog.views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^archive/$',archive, name='archive'),
    url(r'^blog/$',index, name='index'),
    url(r'^article/$',article,name='article'),
    url(r'^comment_post/$',comment_post,name='comment_post'),
    url(r'^login/$',do_login,name='login'),
    url(r'^logout/$',do_logout,name='logout'),
    url(r'^reg/$',do_reg,name='reg'),
    url(r'^tag_article/$',tag_to_article,name='tag_article'),
    url(r'^articles/$',articlelist.as_view()),
    url(r'articles/(?P<pk>(\d+))/$',articledetail.as_view()),
    url(r'^users/$',UserList.as_view()),
    url(r'users/(?P<pk>(\d+))/$',UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
#登录视图
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]