from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.conf import settings
from django.db.models import Count
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password
from blog.forms import *
from rest_framework.renderers import JSONRenderer
from blog.serializers import *
from rest_framework import generics
from rest_framework import permissions
from blog.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.db.models import Q
import json
# Create your views here.


def global_setting(request):
    
    #获取文章日期列表
    archive_list = Article.objects.distinct_date()
    #标签
    tag_list = Tag.objects.all()
    search_form = SearchForm()
    #友情链接
    #根据文章评论数量进行排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()


def reply(request):
    if request.is_ajax():
        content=request.POST.get('content','')
        username=request.POST.get('username','')
        if username=='AnonymousUser':username='不愿透露姓名的围观群众'
        article_id=request.POST.get('article_id','')
        if content and article_id:
            Comment.objects.create(content=content,article_id=article_id,username=username)
    return HttpResponse(json.dumps({"content":content,"username":username,"article_id":article_id}))

#分页
def getpage(request,article_list):
    paginator = Paginator(article_list,3)   
    try:  
        page = request.GET.get('page',1)            
        article_list = paginator.page(page)
    except (InvalidPage,EmptyPage,PageNotAnInteger)as e:
        print(e)
        article_list = paginator.page(1)
    finally:
        return article_list
#首页
def index(request):
                   
    #最新文章显示并分页
    if request.GET.get('search_value',None):
        value = request.GET.get('search_value',None)
        articles = Article.objects.filter(Q(title__icontains=value)|Q(content__icontains=value)
                                              |Q(category__name=value)).order_by('-id')                        
        if not articles:
            return HttpResponse('没有相关文章')      
        #articles = getpage(request,article_list)  
        return render(request,'blogs.html',locals())
    else:       
        article_list = Article.objects.all().order_by('-id')
        articles = getpage(request,article_list)
        return render(request,'blogs.html',locals())

def archive(request):
        
    #获取用户提交的信息
    year = request.GET.get('year',None)
    month = request.GET.get('month',None)               
    #最新文章显示并分页
    article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
    articles = getpage(request,article_list)
    return render(request,'blogs.html',locals())

#点击标签进入页面
def tag_to_article(request):
    
    tag_id = request.GET.get('tag')
    articles = getpage(request,Article.objects.filter(tag=tag_id))   
    return render(request,'blogs.html',locals())

#点击文章进入页面
def article(request):
       
    id = request.GET.get('id',None)
    
    try:
        article = Article.objects.get(pk=id)
        ClickCount(request,article,id)
    except Article.DoesNotExist:
        return HttpResponse('没有这个文章')    
    
    comment_form = CommentForm({'username':'不愿透露姓名的围观群众','article':id}if not request.user.is_authenticated()
                               else{'username':request.user.username,'article':id})
    
    #获取评论
    comments = Comment.objects.filter(article=article).order_by('id')
    comment_list=[]
    for comment in comments:
        for item in comment_list:
            if not hasattr(item,'children_comment'):
                setattr(item,'children_comment',[])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)
    
    return render(request,'article.html',locals())

#点击次数
def ClickCount(request,article,id):
    click_count = article.click_count + 1
    Article.objects.filter(pk=id).update(click_count=click_count)
    

#添加评论
def comment_post(request):
    
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        Comment.objects.create(content=comment_form.cleaned_data['comment_content'],
                                         article_id=comment_form.cleaned_data['article'],
                                         username=comment_form.cleaned_data['username'])
    return redirect(request.META['HTTP_REFERER'])

#注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])

#登陆

def do_login(request):
    try:
        if request.method =='POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    try:
                        login(request,user)
                    except Exception as e:
                        print(e)
                else:
                    return HttpResponse('登陆失败')
                return redirect(request.POST.get('source_url'))
            else:
                return HttpResponse('登陆失败')
        else:
            login_form = LoginForm()
    except Exception as e:
        print(e)
    return render(request,'login.html',locals())

#注册
def do_reg(request):   
    try:
        if request.method=='POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                #注册
                user = User.objects.create(username=reg_form.cleaned_data['username'],
                                           password=make_password(reg_form.cleaned_data['password'],)
                                           )                               
                #登陆
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)                
                return redirect(request.POST.get('source_url'))
            else:
                return HttpResponse('X')
        else:
            reg_form = RegForm()
    except Exception as e:
        print(e)
    return render(request,'reg.html',locals())

#序列化

'''
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse,self).__init__(content,**kwargs)

#初始的方法
@api_view(['GET','POST'])
@csrf_exempt        
def article_list(request):
    if request.method == 'GET':
        article = Article.objects.all()
        ser = ArticleSerializer(article,many=True)
        return Response(ser.data)
    elif request.method == 'POST':
        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@csrf_exempt
def article_detail(request,pk,format=None):
    
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        ser = ArticleSerializer(article)
        return Response(ser.data)
'''
'''
#使用类
class articlelist(APIView):
    
    def get(self,request,format=None):
        article = Article.objects.all()
        ser = ArticleSerializer(article,many=True)
        return Response(ser.data)
    
    def post(self,request,format=None):
        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)


class articledetail(APIView):
    
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExit:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk,format=None):
        article = self.get_object(pk)
        ser = ArticleSerializer(article)
        return Response(ser.data)
    
    def put(self,request,pk,format=None):
        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
''' 

'''
#使用mixins简化代码
class articlelist(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self,request,*args, **kwargs):
        
        return self.list(request, *args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        
        return self.create(request, *args, **kwargs)


class articledetail(mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get(self,request,*args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)
    
    def put(self,request,*args, **kwargs):
        
        return self.update(request, *args, **kwargs)
    
    def delete(self,request,*args, **kwargs):
        
        return self.destroy(request, *args, **kwargs) 
'''
'''
#更更更简洁
class articlelist(generics.ListCreateAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    #添加权限
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
    #将代码段与用户关联
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class articledetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

class UserList(generics.ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''    
class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class ArticleViewSet(viewsets.ModelViewSet):
    
    #print(request.data)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
      
class TagViewSet(viewsets.ModelViewSet):
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer   
    
class CategoryViewSet(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  

class ArticleList(generics.ListAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        '''
        value = self.kwargs.get('value','')
        queryset = Article.objects.filter(title__icontains=value)
        return queryset
        '''
        queryset = Article.objects.all()
        value = self.request.query_params.get('value', None)
        if value is not None:
            queryset = queryset.filter(title__icontains=value)
        return queryset
    
