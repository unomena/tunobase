'''
Created on 23 Oct 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings

from ckeditor.fields import RichTextField

from tunobase.core import models as core_models, managers as core_managers
from tunobase.corporate.company_info import managers, signals

class Newsletter(models.Model):
    '''
    Newsletter to send to active recipients
    '''
    subject = models.CharField(max_length=255)
    plain_content = models.TextField(blank=True, null=True)
    rich_content = RichTextField(blank=True, null=True)
    site = models.ForeignKey(Site, blank=True, null=True)
    send_immediately = models.BooleanField(default=True)
    sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.subject
    
    def send(self):
        # Fire off signal to be received by handlers
        signals.newsletter_saved.send(
            sender=self.__class__,
            newsletter=self
        )
        self.sent = True
        self.save()
    
    def save(self, *args, **kwargs):
        if self.site is None:
            self.site = Site.objects.get_current()
        super(Newsletter, self).save(*args, **kwargs)
        
        if not self.sent and self.send_immediately:
            self.send()

class NewsletterRecipient(models.Model):
    '''
    Newsletter recipients that have subscribed
    from the Site
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        null=True
    )
    email = models.EmailField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    newsletters_received = models.ManyToManyField(
        Newsletter, 
        related_name='recipients', 
        blank=True, 
        null=True
    )
    
    active_recipients = managers.NewsletterRecipientManager()
    
    def __unicode__(self):
        return u'%s' % self.get_email()
    
    def get_email(self):
        if self.user is not None:
            return self.user.email
        
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.id and self.email:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=self.email)
                if user.is_active:
                    raise ValidationError(
                        'Email address %s already exists as a User on the system' %
                        self.email
                    )
            except User.DoesNotExist:
                pass
            
        super(NewsletterRecipient, self).save(*args, **kwargs)

class ContactMessage(models.Model):
    '''
    Contact message sent from the Site
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    message = models.TextField()
    site = models.ForeignKey(Site, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s'  % self.name
    
    def send(self):
        # Fire off signal to be received by handlers
        signals.contact_message_saved.send(
            sender=self.__class__,
            contact_message_id=self.id
        )
    
    def save(self, *args, **kwargs):
        if self.site is None:
            self.site = Site.objects.get_current()
        super(ContactMessage, self).save(*args, **kwargs)
        
        self.send()

class Vacancy(core_models.ContentModel):
    '''
    Job vacancies within the company
    '''
    external_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    default_manager = core_managers.SiteObjectsManager()
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Vacancies'
    
class CompanyMemberPosition(core_models.StateModel, core_models.SlugModel):
    '''
    Member positions within the Company
    '''
    sites = models.ManyToManyField(Site, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        ordering = ['order']

class CompanyMember(core_models.ContentModel):
    '''
    Members of the company
    '''
    default_image_category = 'company_member'
    
    positions = models.ManyToManyField(CompanyMemberPosition, related_name='company_members')
    job_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    default_manager = core_managers.SiteObjectsManager()
    
    class Meta:
        ordering = ['order']