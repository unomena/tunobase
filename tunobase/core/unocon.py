'''
Created on 22 Jul 2015

@author: michaelwhelehan
'''
import unoconsole

from tunobase.core import models


class TemplateAdmin(unoconsole.ModelAdmin):
    list_display = ['name', 'path', 'num_contents', 'num_images']
    list_filter = ['name', 'path']
    search_fields = ['name', 'path']


class TemplatePageAdmin(unoconsole.ModelAdmin):
    form = unoconsole.forms.TemplatePageForm


unoconsole.console.register(
    models.Template,
    TemplateAdmin,
    category="CMS"
)
unoconsole.console.register(
    models.TemplatePage,
    TemplatePageAdmin,
    category="CMS"
)
