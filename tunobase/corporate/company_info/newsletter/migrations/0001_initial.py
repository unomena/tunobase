# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RichNewsletterPart'
        db.create_table(u'newsletter_richnewsletterpart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'newsletter', ['RichNewsletterPart'])

        # Adding model 'PlainNewsletterPart'
        db.create_table(u'newsletter_plainnewsletterpart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'newsletter', ['PlainNewsletterPart'])

        # Adding model 'Newsletter'
        db.create_table(u'newsletter_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('plain_header', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='newsletter_headers', null=True, to=orm['newsletter.PlainNewsletterPart'])),
            ('plain_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('plain_footer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='newsletter_footers', null=True, to=orm['newsletter.PlainNewsletterPart'])),
            ('rich_header', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='newsletter_headers', null=True, to=orm['newsletter.RichNewsletterPart'])),
            ('rich_content', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('rich_footer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='newsletter_footers', null=True, to=orm['newsletter.RichNewsletterPart'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True)),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['Newsletter'])

        # Adding model 'NewsletterRecipient'
        db.create_table(u'newsletter_newsletterrecipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='newsletter_recipient', unique=True, null=True, to=orm['authentication.EndUser'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'newsletter', ['NewsletterRecipient'])

        # Adding M2M table for field newsletters_received on 'NewsletterRecipient'
        m2m_table_name = db.shorten_name(u'newsletter_newsletterrecipient_newsletters_received')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletterrecipient', models.ForeignKey(orm[u'newsletter.newsletterrecipient'], null=False)),
            ('newsletter', models.ForeignKey(orm[u'newsletter.newsletter'], null=False))
        ))
        db.create_unique(m2m_table_name, ['newsletterrecipient_id', 'newsletter_id'])


    def backwards(self, orm):
        # Deleting model 'RichNewsletterPart'
        db.delete_table(u'newsletter_richnewsletterpart')

        # Deleting model 'PlainNewsletterPart'
        db.delete_table(u'newsletter_plainnewsletterpart')

        # Deleting model 'Newsletter'
        db.delete_table(u'newsletter_newsletter')

        # Deleting model 'NewsletterRecipient'
        db.delete_table(u'newsletter_newsletterrecipient')

        # Removing M2M table for field newsletters_received on 'NewsletterRecipient'
        db.delete_table(db.shorten_name(u'newsletter_newsletterrecipient_newsletters_received'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authentication.enduser': {
            'Meta': {'object_name': 'EndUser'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enduser_related'", 'null': 'True', 'to': u"orm['photologue.PhotoEffect']"}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_console_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_regular_user': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'web_address': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'newsletter.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plain_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'plain_footer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'newsletter_footers'", 'null': 'True', 'to': u"orm['newsletter.PlainNewsletterPart']"}),
            'plain_header': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'newsletter_headers'", 'null': 'True', 'to': u"orm['newsletter.PlainNewsletterPart']"}),
            'rich_content': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'rich_footer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'newsletter_footers'", 'null': 'True', 'to': u"orm['newsletter.RichNewsletterPart']"}),
            'rich_header': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'newsletter_headers'", 'null': 'True', 'to': u"orm['newsletter.RichNewsletterPart']"}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'newsletter.newsletterrecipient': {
            'Meta': {'object_name': 'NewsletterRecipient'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'newsletters_received': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'recipients'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['newsletter.Newsletter']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'newsletter_recipient'", 'unique': 'True', 'null': 'True', 'to': u"orm['authentication.EndUser']"})
        },
        u'newsletter.plainnewsletterpart': {
            'Meta': {'object_name': 'PlainNewsletterPart'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'newsletter.richnewsletterpart': {
            'Meta': {'object_name': 'RichNewsletterPart'},
            'content': ('ckeditor.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['newsletter']