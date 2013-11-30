# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tagging_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True)),
        ))
        db.send_create_signal(u'tagging', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['title', 'site']
        db.create_unique(u'tagging_tag', ['title', 'site_id'])

        # Adding model 'ContentObjectTag'
        db.create_table(u'tagging_contentobjecttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_contentobjecttag', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_object_tags', to=orm['tagging.Tag'])),
        ))
        db.send_create_signal(u'tagging', ['ContentObjectTag'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['title', 'site']
        db.delete_unique(u'tagging_tag', ['title', 'site_id'])

        # Deleting model 'Tag'
        db.delete_table(u'tagging_tag')

        # Deleting model 'ContentObjectTag'
        db.delete_table(u'tagging_contentobjecttag')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tagging.contentobjecttag': {
            'Meta': {'object_name': 'ContentObjectTag'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_contentobjecttag'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_object_tags'", 'to': u"orm['tagging.Tag']"})
        },
        u'tagging.tag': {
            'Meta': {'unique_together': "[('title', 'site')]", 'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        }
    }

    complete_apps = ['tagging']