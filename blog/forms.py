#!/usr/lib/env python
#-*-coding:UTF-8-*-

from django import forms

class RegForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','required':'required'}),
                               max_length=50,error_messages={'required':'username不能为空'})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'pasword','required':'required'}),
                               max_length=20,error_messages={'required':'pasword不能为空'})
    

class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','required':'required'}),
                               max_length=50,error_messages={'required':'username不能为空'})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'pasword','required':'required'}),
                               max_length=20,error_messages={'required':'pasword不能为空'})
    

class CommentForm(forms.Form):
    
    
    comment_content = forms.CharField(widget=forms.Textarea(attrs={'id':'comment_content','required':'required',
                                                                   'cols':'110','rows':'10'}),
                                                                   error_messages={'required':'评论不能为空'})
    article = forms.CharField(widget=forms.HiddenInput)
    username= forms.CharField(widget=forms.HiddenInput)     

class SearchForm(forms.Form):
    
    search_value = forms.CharField(widget=forms.Textarea(attrs={'id':'search_value','required':'required',
                                                                   'cols':'50','rows':'1','style':"resize:none"}),
                                                                   error_messages={'required':'内容不能为空'})  
