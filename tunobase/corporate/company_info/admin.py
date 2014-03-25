"""
COMPANY INFO APP

This module determins which models are displayed in Django's
admin.

"""
from django.contrib import admin

from tunobase.core.admin import SiteListAdminMixin
from tunobase.corporate.company_info import models

class CompanyMemberAdmin(admin.ModelAdmin, SiteListAdminMixin):

    list_display = (
            'title', 'state', 'slug', 'site_list'
    )
    list_filter = ('title', 'state',)
    search_fields = ('title',)

admin.site.register(models.Vacancy)
admin.site.register(models.CompanyMemberPosition, CompanyMemberAdmin)
admin.site.register(models.CompanyMember, CompanyMemberAdmin)
