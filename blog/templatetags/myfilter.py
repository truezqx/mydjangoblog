#!/usr/lib/env python
#-*-coding:UTF-8-*-

from django import template

register = template.Library()

@register.filter
def month_to_upper(key):
    return['一','二','三','四','五','六','七','八','九'][key.month-1]
    
#register.filter('month_to_upper',month_to_upper)