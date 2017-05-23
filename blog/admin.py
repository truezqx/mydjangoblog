from django.contrib import admin
from blog.models import *
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    
    #fields = ('title','desc','content',)
    list_display=('title','desc','click_count',)
    list_display_links=('title','desc',)
    list_editable = ('click_count',)
    
    fieldsets = (
        (None,{
            'fields':('title','desc','content',)
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields':('click_count','is_recommend',)
            })        
        )
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
#admin.site.register(Article,ArticleAdmin)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)