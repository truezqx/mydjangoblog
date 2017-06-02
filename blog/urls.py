from django.conf.urls import include
from django.conf.urls import url
from blog.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from blog.myviews import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from blog.upload import upload_image
urlpatterns = [
    url(r'^archive/$',archive, name='archive'),
    url(r'^blog/$',index, name='index'),
    url(r'^article/$',article,name='article'),
    url(r'^comment_post/$',comment_post,name='comment_post'),
    url(r'^login/$',do_login,name='login'),
    url(r'^logout/$',do_logout,name='logout'),
    url(r'^reg/$',do_reg,name='reg'),
    url(r'^tag_article/$',tag_to_article,name='tag_article'),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)


#序列化


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'tags',TagViewSet)
router.register(r'Categorys',CategoryViewSet)


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api/',include(router.urls)),
    url(r'^Articles/',ArticleList.as_view()),
    
]
urlpatterns += [
    url(r'^uploads/(?P<path>.*)$',\
        'django.views.static.serve',\
        {'document_root':settings.MEDIA_ROOT,}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',upload_image,name='upload_image')
    ]
'''
article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})



    url(r'^articles/$',articlelist.as_view(),name='article-list'),
    url(r'^articles/(?P<pk>(\d+))/$',articledetail.as_view(),name='article-detail'),
    url(r'^users/$',UserList.as_view(),name='user-list'),
    url(r'^users/(?P<pk>(\d+))/$',UserDetail.as_view(),name='user-detail'),
'''



