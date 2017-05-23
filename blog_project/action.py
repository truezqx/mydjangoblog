#!/usr/lib/env python
#-*-coding:UTF-8-*-
from django.http import HttpResponse
def action(request,**kw):
    app =kw.get('app','blog')
    function = kw.get('function','index')
    try:
        mod = __import__('%s'%app,globals(),locals())
        viewobj = getattr(mod,'views')
        funcobj = getattr(viewobj,function)  
        res = funcobj(request,**kw)
        return res
    except (ImportError,AttributeError)as e:
        print(e)
        return HttpResponse('404 Not Found')
    except Exception as e:
        print(e)