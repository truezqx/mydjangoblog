from django.contrib import admin
from blog.models import *
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    
    #fields = ('title','desc','content',)
    list_display=('title','desc','click_count','user','category')
    list_display_links=('title','desc',)
    list_editable = ('click_count',)
    
    fieldsets = (
        (None,{
            'fields':('title','desc','content','user','category')
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields':('click_count','is_recommend','tag')
            })        
        )
    class Media:
        # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
        js = (
            'js/kindeditor-4.1.7/kindeditor-min.js',
            'js/kindeditor-4.1.7/lang/zh_CN.js',
            'js/kindeditor-4.1.7/config.js',
        )
        
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
#admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)