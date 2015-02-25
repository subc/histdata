# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CandleEurUsdM5Rate'
        db.create_table(u'rate_candleeurusdm5rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')()),
            ('close_bid', self.gf('django.db.models.fields.FloatField')()),
            ('high_bid', self.gf('django.db.models.fields.FloatField')()),
            ('low_bid', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'rate', ['CandleEurUsdM5Rate'])

        # Adding unique constraint on 'CandleEurUsdM5Rate', fields ['start_at']
        db.create_unique(u'rate_candleeurusdm5rate', ['start_at'])


    def backwards(self, orm):
        # Removing unique constraint on 'CandleEurUsdM5Rate', fields ['start_at']
        db.delete_unique(u'rate_candleeurusdm5rate', ['start_at'])

        # Deleting model 'CandleEurUsdM5Rate'
        db.delete_table(u'rate_candleeurusdm5rate')


    models = {
        u'rate.candleeurusdm5rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleEurUsdM5Rate'},
            'close_bid': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'high_bid': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_bid': ('django.db.models.fields.FloatField', [], {}),
            'open_bid': ('django.db.models.fields.FloatField', [], {}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '0'})
        }
    }

    complete_apps = ['rate']