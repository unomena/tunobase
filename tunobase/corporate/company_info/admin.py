"""
COMPANY INFO APP

This module determins which models are displayed in Django's
admin.

Classes:
    n/a

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.corporate.company_info import models

admin.site.register(models.Vacancy)
admin.site.register(models.CompanyMemberPosition)
admin.site.register(models.CompanyMember)
