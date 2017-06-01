#!/usr/lib/env python
#-*-coding:UTF-8-*-

from rest_framework import serializers
from blog.models import *

class TagSerializer(serializers.HyperlinkedModelSerializer):      
    
    class Meta:
        model = Tag
        fields = ('name','id') 

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.username')
    tag = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')
    category = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Article
        fields = ('title','content','user','category','click_count','date_publish','tag')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    #articles = serializers.HyperlinkedRelatedField(many=True, view_name='article-detail',read_only=True)    
    class Meta:
        model = User
        fields = ('id','username','articles')
        #fields = '__all __'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('content','username','date_publish','article')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name',)