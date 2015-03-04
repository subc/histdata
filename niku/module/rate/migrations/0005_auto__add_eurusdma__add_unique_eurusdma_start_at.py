# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EurUsdMA'
        db.create_table(u'rate_eurusdma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('h1', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h4', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h24', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d10', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d75', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d200', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
        ))
        db.send_create_signal(u'rate', ['EurUsdMA'])

        # Adding unique constraint on 'EurUsdMA', fields ['start_at']
        db.create_unique(u'rate_eurusdma', ['start_at'])


    def backwards(self, orm):
        # Removing unique constraint on 'EurUsdMA', fields ['start_at']
        db.delete_unique(u'rate_eurusdma', ['start_at'])

        # Deleting model 'EurUsdMA'
        db.delete_table(u'rate_eurusdma')


    models = {
        u'rate.candleeurusddrate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleEurUsdDRate'},
            'close_bid': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_bid': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'low_bid': ('django.db.models.fields.FloatField', [], {}),
            'open_bid': ('django.db.models.fields.FloatField', [], {}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'rate.candleeurusdh1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleEurUsdH1Rate'},
            'close_bid': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_bid': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'low_bid': ('django.db.models.fields.FloatField', [], {}),
            'open_bid': ('django.db.models.fields.FloatField', [], {}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'rate.candleeurusdm1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleEurUsdM1Rate'},
            'close_bid': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_bid': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'low_bid': ('django.db.models.fields.FloatField', [], {}),
            'open_bid': ('django.db.models.fields.FloatField', [], {}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'rate.candleeurusdm5rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleEurUsdM5Rate'},
            'close_bid': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_bid': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'low_bid': ('django.db.models.fields.FloatField', [], {}),
            'open_bid': ('django.db.models.fields.FloatField', [], {}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'rate.eurusdma': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'EurUsdMA'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'd10': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'd200': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'd25': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'd5': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'd75': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'h1': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'h24': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'h4': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rate']