'''
Created on 22 Oct 2013

@author: michael
'''
import random

from django.db import models, IntegrityError
from django.contrib.sites.models import Site
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings

from polymorphic import PolymorphicModel, PolymorphicManager

from photologue.models import ImageModel

from ckeditor.fields import RichTextField

from tunobase.core import constants

class SiteObjectsManager(models.Manager):

    def for_current_site(self):
        return self.filter(sites__id__exact=Site.objects.get_current().id)

class StateManager(SiteObjectsManager):

    def get_query_set(self):
        queryset = super(StateManager, self).get_query_set().filter(
            state__in=[constants.STATE_PUBLISHED, constants.STATE_STAGED]
        )
            
        # exclude objects in staging state if not in staging mode (settings.STAGING = False)
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(state=constants.STATE_STAGED)
        return queryset
    
class PolyManager(StateManager, PolymorphicManager):
    pass

class StateModel(models.Model):
    state = models.PositiveSmallIntegerField(
        choices=constants.STATE_CHOICES,
        default=constants.STATE_PUBLISHED
    )
    
    publish_at = models.DateTimeField(blank=True, null=True, db_index=True)
    retract_at = models.DateTimeField(blank=True, null=True)
    
    objects = SiteObjectsManager()
    permitted = StateManager()
    
    class Meta:
        ordering = ['-publish_at']
        abstract = True
                
    def save(self, *args, **kwargs):
        if not self.publish_at and self.state == constants.STATE_PUBLISHED:
            self.publish_at = timezone.now()
            
        super(StateModel, self).save(*args, **kwargs)
        
class SlugModel(models.Model):
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
    image_name = models.CharField(
        max_length=255, 
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
    
    objects = SiteObjectsManager()
    poly_objects = PolyManager()
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = DefaultImage.permitted.get_random(self.default_image_category)

        super(ContentModel, self).save(*args, **kwargs)
    
class DefaultImageManager(StateManager):

    def get_random(self, category=None):
        pre_def_images = self.filter(category=category)
        if pre_def_images:
            return random.choice(pre_def_images).image
        else:
            return None

class DefaultImage(ImageModel, StateModel):
    """
    A model to store default images for content types.
    """
    category = models.CharField(
        max_length=16,
        choices=settings.DEFAULT_IMAGE_CATEGORY_CHOICES
    )
    
    objects = models.Manager()
    permitted = DefaultImageManager()
    
    def __unicode__(self):
        return u'%s' % self.get_category_display()
    
class Banner(StateModel):
    title = models.CharField(max_length=255)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ['order']
        
    def __unicode__(self):
        return u'%s' % self.title

class ImageBanner(Banner, ImageModel):
    pass

class HTMLBanner(Banner):
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RichTextField(blank=True, null=True)
    
class BannerSet(models.Model):
    slug = models.SlugField()
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s' % self.slug
    
    @property
    def site_banners(self):
        return self.banners.filter(sites__id__exact=Site.objects.get_current().id)
    
class ImageBannerSet(BannerSet):
    banners = models.ManyToManyField(ImageBanner, related_name='banner_sets')
    
class HTMLBannerSet(BannerSet):
    banners = models.ManyToManyField(HTMLBanner, related_name='banner_sets')