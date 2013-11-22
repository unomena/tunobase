'''
Created on 22 Oct 2013

@author: michael
'''
from django.db import models, IntegrityError
from django.contrib.sites.models import Site
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models import signals
from django.conf import settings

from polymorphic import PolymorphicModel

from photologue.models import ImageModel as PhotologueImageModel

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
    
    objects = managers.CoreStateManager()
    
    class Meta:
        ordering = ['-publish_at']
        abstract = True
        
    def mark_deleted(self):
        self.state = constants.STATE_DELETED
        self.save()
                
    def save(self, *args, **kwargs):
        if not self.publish_at and self.state == constants.STATE_PUBLISHED:
            self.publish_at = timezone.now()
            
        super(StateModel, self).save(*args, **kwargs)
        
class SlugModel(models.Model):
    '''
    A mixin Model for creating unique Slugs
    '''
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, editable=False, db_index=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        params = {
            'slug': slugify(self.title),
        }
        i = 1
        
        if hasattr(self, 'site'):
            params['site'] = self.site
        elif hasattr(self, 'sites'):
            params['sites'] = self.sites.all()
        
        # Check if the same slug of this type exists
        # and increment the index until a unique slug
        # is found
        while self.__class__.objects.filter(**params).exclude(pk=self.pk).exists():
            params['slug'] = '%s-%s' % (params['slug'], i)
            i += 1
        
        self.slug = params['slug']   
        
        super(SlugModel, self).save(*args, **kwargs)
            
class AuditModel(models.Model):
    '''
    A mixin Model for auditting creations/modifications
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='%(class)s_created_content', 
        blank=True, 
        null=True
    )
    
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='%(class)s_modified_content',  
        blank=True, 
        null=True
    )
    
    class Meta:
        abstract = True
        
class ImageModel(PhotologueImageModel):
    image_name = models.CharField(
        max_length=512, 
        blank=True, 
        null=True,
    )
    
    default_image_category = 'image'
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s' % self.image_name
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = DefaultImage.objects.permitted()\
                .get_random(self.default_image_category)
        if self.image and not self.image_name:
            self.image_name = '%s %s' % \
                (self.image, timezone.now().strftime('%Y-%m-%d'))
        
        super(ImageModel, self).save(*args, **kwargs)
        
class BaseContentModel(ImageModel, StateModel, SlugModel, AuditModel):
    '''
    Base Content Model
    '''
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RichTextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    default_image_category = 'content'
    
    objects = managers.StateManager()
    
    class Meta:
        abstract = True
        ordering = ['order', '-publish_at']
    
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())
    
    
class ContentModel(PolymorphicModel, BaseContentModel):
    '''
    All Content on the Site must derive from this Model
    '''
    objects = managers.CorePolymorphicStateManager()
    
    class Meta:
        ordering = ['order', '-publish_at']
    
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())
        
class ContentBlock(ContentModel):
    '''
    Used for portlets placed throughout the Site where
    just a block of content is needed.
    '''
    
class DefaultImage(PhotologueImageModel, StateModel):
    '''
    A model to store default images for content types.
    '''
    category = models.CharField(
        max_length=16,
        choices=settings.DEFAULT_IMAGE_CATEGORY_CHOICES
    )
    
    objects = managers.DefaultImageManager()
    
    def __unicode__(self):
        return u'%s' % self.get_category_display()
    
class Banner(StateModel):
    '''
    Abstract Banner for Site sliders
    '''
    title = models.CharField(max_length=255)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['order', '-publish_at']
        
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())

class ImageBanner(Banner, ImageModel):
    '''
    Image Banner for Site sliders
    '''

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
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['order', '-publish_at']
        
    def __unicode__(self):
        return u'%s' % self.slug
    
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

class GalleryImage(ImageModel, StateModel):
    '''
    A model to store Gallery Images
    '''
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    class Meta:
        ordering = ['order', '-publish_at']
    
    def __unicode__(self):
        return u'%s %s' % (self.image, self.sites.all())
    
    @property
    def gallery(self):
        try:
            return self.galleries.all()[0]
        except IndexError:
            return None
    
class Gallery(ContentModel):
    '''
    Containing model for Gallery Images
    '''
    images = models.ManyToManyField(
        GalleryImage, 
        related_name='galleries', 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name_plural = 'galleries'
    
    def __unicode__(self):
        return u'%s' % self.title