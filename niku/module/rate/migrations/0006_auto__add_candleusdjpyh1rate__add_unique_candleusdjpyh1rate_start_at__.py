# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CandleUsdJpyH1Rate'
        db.create_table(u'rate_candleusdjpyh1rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')()),
            ('close_bid', self.gf('django.db.models.fields.FloatField')()),
            ('high_bid', self.gf('django.db.models.fields.FloatField')()),
            ('low_bid', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'rate', ['CandleUsdJpyH1Rate'])

        # Adding unique constraint on 'CandleUsdJpyH1Rate', fields ['start_at']
        db.create_unique(u'rate_candleusdjpyh1rate', ['start_at'])

        # Adding model 'CandleUsdJpyDRate'
        db.create_table(u'rate_candleusdjpydrate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')()),
            ('close_bid', self.gf('django.db.models.fields.FloatField')()),
            ('high_bid', self.gf('django.db.models.fields.FloatField')()),
            ('low_bid', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'rate', ['CandleUsdJpyDRate'])

        # Adding unique constraint on 'CandleUsdJpyDRate', fields ['start_at']
        db.create_unique(u'rate_candleusdjpydrate', ['start_at'])

        # Adding model 'CandleUsdJpyM1Rate'
        db.create_table(u'rate_candleusdjpym1rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')()),
            ('close_bid', self.gf('django.db.models.fields.FloatField')()),
            ('high_bid', self.gf('django.db.models.fields.FloatField')()),
            ('low_bid', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'rate', ['CandleUsdJpyM1Rate'])

        # Adding unique constraint on 'CandleUsdJpyM1Rate', fields ['start_at']
        db.create_unique(u'rate_candleusdjpym1rate', ['start_at'])

        # Adding model 'CandleUsdJpyM5Rate'
        db.create_table(u'rate_candleusdjpym5rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')()),
            ('close_bid', self.gf('django.db.models.fields.FloatField')()),
            ('high_bid', self.gf('django.db.models.fields.FloatField')()),
            ('low_bid', self.gf('django.db.models.fields.FloatField')()),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'rate', ['CandleUsdJpyM5Rate'])

        # Adding unique constraint on 'CandleUsdJpyM5Rate', fields ['start_at']
        db.create_unique(u'rate_candleusdjpym5rate', ['start_at'])

        # Adding model 'UsdJpyMA'
        db.create_table(u'rate_usdjpyma', (
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
        db.send_create_signal(u'rate', ['UsdJpyMA'])

        # Adding unique constraint on 'UsdJpyMA', fields ['start_at']
        db.create_unique(u'rate_usdjpyma', ['start_at'])


    def backwards(self, orm):
        # Removing unique constraint on 'UsdJpyMA', fields ['start_at']
        db.delete_unique(u'rate_usdjpyma', ['start_at'])

        # Removing unique constraint on 'CandleUsdJpyM5Rate', fields ['start_at']
        db.delete_unique(u'rate_candleusdjpym5rate', ['start_at'])

        # Removing unique constraint on 'CandleUsdJpyM1Rate', fields ['start_at']
        db.delete_unique(u'rate_candleusdjpym1rate', ['start_at'])

        # Removing unique constraint on 'CandleUsdJpyDRate', fields ['start_at']
        db.delete_unique(u'rate_candleusdjpydrate', ['start_at'])

        # Removing unique constraint on 'CandleUsdJpyH1Rate', fields ['start_at']
        db.delete_unique(u'rate_candleusdjpyh1rate', ['start_at'])

        # Deleting model 'CandleUsdJpyH1Rate'
        db.delete_table(u'rate_candleusdjpyh1rate')

        # Deleting model 'CandleUsdJpyDRate'
        db.delete_table(u'rate_candleusdjpydrate')

        # Deleting model 'CandleUsdJpyM1Rate'
        db.delete_table(u'rate_candleusdjpym1rate')

        # Deleting model 'CandleUsdJpyM5Rate'
        db.delete_table(u'rate_candleusdjpym5rate')

        # Deleting model 'UsdJpyMA'
        db.delete_table(u'rate_usdjpyma')


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
        u'rate.candleusdjpydrate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleUsdJpyDRate'},
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
        u'rate.candleusdjpyh1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleUsdJpyH1Rate'},
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
        u'rate.candleusdjpym1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleUsdJpyM1Rate'},
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
        u'rate.candleusdjpym5rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleUsdJpyM5Rate'},
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
        },
        u'rate.usdjpyma': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'UsdJpyMA'},
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