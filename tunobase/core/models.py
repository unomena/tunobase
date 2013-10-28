'''
Created on 22 Oct 2013

@author: michael
'''
import random

from django.db import models, IntegrityError
from django.contrib.sites.models import Site
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models import signals
from django.conf import settings

from polymorphic import PolymorphicModel

from photologue.models import ImageModel

from ckeditor.fields import RichTextField

from tunobase.core import constants, managers

class StateModel(models.Model):
    '''
    A mixin Model for providing published State
    '''
    state = models.PositiveSmallIntegerField(
        choices=constants.STATE_CHOICES,
        default=constants.STATE_PUBLISHED
    )
    
    publish_at = models.DateTimeField(blank=True, null=True, db_index=True)
    retract_at = models.DateTimeField(blank=True, null=True)
    
    objects = models.Manager()
    permitted = managers.StateManager()
    
    class Meta:
        ordering = ['-publish_at']
        abstract = True
                
    def save(self, *args, **kwargs):
        if not self.publish_at and self.state == constants.STATE_PUBLISHED:
            self.publish_at = timezone.now()
            
        super(StateModel, self).save(*args, **kwargs)
        
class SlugModel(models.Model):
    '''
    A mixin Model for creating unique Slugs
    '''
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(editable=False, unique=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        try:
            if not self.id:
                self.slug = slugify(self.title)
                
            super(SlugModel, self).save(*args, **kwargs)
        except IntegrityError:
            if not self.id:
                self.slug = '%s-%s' % (slugify(self.title), random.randint(1, 100))
                                       
            super(SlugModel, self).save(*args, **kwargs)

class ContentModel(PolymorphicModel, ImageModel, StateModel, SlugModel):
    '''
    All Content on the Site must derive from this Model
    '''
    image_name = models.CharField(
        max_length=512, 
        blank=True, 
        null=True, 
        unique=True
    )
    
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RichTextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='created_content', 
        blank=True, 
        null=True
    )
    
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='modified_content',  
        blank=True, 
        null=True
    )
    
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    default_image_category = 'content'
    
    objects = managers.SiteObjectsManager()
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = DefaultImage.permitted.get_random(self.default_image_category)
        
        if not self.image_name:
            self.image_name = '%s %s' % (self.title, timezone.now().strftime('%Y-%m-%d'))

        super(ContentModel, self).save(*args, **kwargs)

class DefaultImage(ImageModel, StateModel):
    '''
    A model to store default images for content types.
    '''
    category = models.CharField(
        max_length=16,
        choices=settings.DEFAULT_IMAGE_CATEGORY_CHOICES
    )
    
    objects = models.Manager()
    permitted = managers.DefaultImageManager()
    
    def __unicode__(self):
        return u'%s' % self.get_category_display()
    
class Banner(StateModel):
    '''
    Abstract Banner for Site sliders
    '''
    title = models.CharField(max_length=255)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ['order']
        
    def __unicode__(self):
        return u'%s' % self.title

class ImageBanner(Banner, ImageModel):
    '''
    Image Banner for Site sliders
    '''
    pass

class HTMLBanner(Banner):
    '''
    HTML Banner for Site sliders
    '''
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RichTextField(blank=True, null=True)
    
class BannerSet(StateModel):
    '''
    Abstract Containing Model for Banners
    '''
    slug = models.SlugField()
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s' % self.slug
    
    @property
    def site_banners(self):
        return self.banners.filter(sites__id__exact=Site.objects.get_current().id)
    
class ImageBannerSet(BannerSet):
    '''
    Containing Model for Image Banners
    '''
    banners = models.ManyToManyField(ImageBanner, related_name='banner_sets')
    
class HTMLBannerSet(BannerSet):
    '''
    Containing Model for HTML Banners
    '''
    banners = models.ManyToManyField(HTMLBanner, related_name='banner_sets')