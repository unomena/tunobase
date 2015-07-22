'''
CORE APP

This module sets up the core models.

'''
from unidecode import unidecode

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.contenttypes import generic

# from polymorphic import PolymorphicModel

from photologue.models import ImageModel as PhotologueImageModel

from redactor.fields import RedactorTextField

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
        if not hasattr(self, 'override_slug_save') and not self.slug:
            self.slug = slugify(unidecode(self.title))

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


class SEOModel(models.Model):
    '''
    A mixin Model for website seo
    '''
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseContentModel(ImageModel, StateModel, SlugModel, AuditModel, SEOModel):
    '''
    Base Content Model
    '''
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RedactorTextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)

    default_image_category = 'content'

    objects = managers.CoreStateManager()

    class Meta:
        abstract = True
        ordering = ['order', '-publish_at']

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())


# class PolymorphicContentModel(PolymorphicModel, BaseContentModel):
#     '''
#     All Content on the Site must derive from this Model
#     '''
#     objects = managers.CorePolymorphicStateManager()
# 
#     class Meta:
#         ordering = ['order', '-publish_at']
# 
#     def __unicode__(self):
#         return u'%s - %s' % (self.title, self.sites.all())


class ContentModel(BaseContentModel):
    '''
    All Content on the Site must derive from this Model
    '''
    leaf_content_type = models.ForeignKey(ContentType, editable=False, null=True)

    class Meta:
        ordering = ['order', '-publish_at']

    def as_leaf_class(self):
        return self.leaf_content_type.model_class().objects.get(id=self.id)

    def save(self, *args, **kwargs):
        self.leaf_content_type = ContentType.objects.get_for_model(self.__class__) if not self.leaf_content_type else self.leaf_content_type
        return super(ContentModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())


class ContentBlockSet(ContentModel):
    '''
    Containing Model for Content Blocks
    '''


class ContentBlock(ContentModel):
    '''
    Used for portlets placed throughout the Site where
    just a block of content is needed.
    '''
    alternative_title = models.CharField(max_length=255)
    content_block_parent = models.ForeignKey(
        ContentBlockSet,
        related_name='content_blocks',
        blank=True,
        null=True
    )


class Template(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='template_images_template')
    path = models.CharField(max_length=255)
    num_contents = models.PositiveSmallIntegerField(default=0)
    num_images = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.name


class TemplatePage(StateModel):
    url = models.CharField(max_length=100, unique=True, db_index=True)
    template = models.ForeignKey(
        Template,
        related_name='content_templates'
    )
    content_1 = RedactorTextField(blank=True, null=True)
    content_2 = RedactorTextField(blank=True, null=True)
    content_3 = RedactorTextField(blank=True, null=True)
    content_4 = RedactorTextField(blank=True, null=True)
    content_5 = RedactorTextField(blank=True, null=True)
    content_6 = RedactorTextField(blank=True, null=True)
    content_7 = RedactorTextField(blank=True, null=True)
    content_8 = RedactorTextField(blank=True, null=True)
    content_9 = RedactorTextField(blank=True, null=True)
    content_10 = RedactorTextField(blank=True, null=True)

    image_1 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_2 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_3 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_4 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_5 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_6 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_7 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_8 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_9 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )
    image_10 = models.ImageField(
        upload_to='template_images', blank=True, null=True
    )

    def __unicode__(self):
        return u'%s' % self.url


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
    rich_content = RedactorTextField(blank=True, null=True)


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

    default_image_category = 'gallery'

    class Meta:
        verbose_name_plural = 'galleries'

    def __unicode__(self):
        return u'%s' % self.title


class VersionSeries(models.Model):
    slug = models.SlugField(max_length=255)
    staged_slug = models.SlugField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.slug


class Version(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    series = models.ForeignKey(VersionSeries, related_name='versions')
    number = models.PositiveIntegerField()
    state = models.PositiveSmallIntegerField(
        choices=constants.STATE_CHOICES
    )
    objects = managers.VersionManager()

    def __unicode__(self):
        return u'%s' % self.series
