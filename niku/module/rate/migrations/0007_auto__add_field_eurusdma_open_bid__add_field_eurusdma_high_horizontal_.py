# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EurUsdMA.open_bid'
        db.add_column(u'rate_eurusdma', 'open_bid',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.high_horizontal_d25'
        db.add_column(u'rate_eurusdma', 'high_horizontal_d25',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.high_horizontal_d25_last_at'
        db.add_column(u'rate_eurusdma', 'high_horizontal_d25_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.low_horizontal_d25'
        db.add_column(u'rate_eurusdma', 'low_horizontal_d25',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.low_horizontal_d25_last_at'
        db.add_column(u'rate_eurusdma', 'low_horizontal_d25_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.high_horizontal_d5'
        db.add_column(u'rate_eurusdma', 'high_horizontal_d5',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.high_horizontal_d5_last_at'
        db.add_column(u'rate_eurusdma', 'high_horizontal_d5_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.low_horizontal_d5'
        db.add_column(u'rate_eurusdma', 'low_horizontal_d5',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'EurUsdMA.low_horizontal_d5_last_at'
        db.add_column(u'rate_eurusdma', 'low_horizontal_d5_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.open_bid'
        db.add_column(u'rate_usdjpyma', 'open_bid',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.high_horizontal_d25'
        db.add_column(u'rate_usdjpyma', 'high_horizontal_d25',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.high_horizontal_d25_last_at'
        db.add_column(u'rate_usdjpyma', 'high_horizontal_d25_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.low_horizontal_d25'
        db.add_column(u'rate_usdjpyma', 'low_horizontal_d25',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.low_horizontal_d25_last_at'
        db.add_column(u'rate_usdjpyma', 'low_horizontal_d25_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.high_horizontal_d5'
        db.add_column(u'rate_usdjpyma', 'high_horizontal_d5',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.high_horizontal_d5_last_at'
        db.add_column(u'rate_usdjpyma', 'high_horizontal_d5_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.low_horizontal_d5'
        db.add_column(u'rate_usdjpyma', 'low_horizontal_d5',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'UsdJpyMA.low_horizontal_d5_last_at'
        db.add_column(u'rate_usdjpyma', 'low_horizontal_d5_last_at',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EurUsdMA.open_bid'
        db.delete_column(u'rate_eurusdma', 'open_bid')

        # Deleting field 'EurUsdMA.high_horizontal_d25'
        db.delete_column(u'rate_eurusdma', 'high_horizontal_d25')

        # Deleting field 'EurUsdMA.high_horizontal_d25_last_at'
        db.delete_column(u'rate_eurusdma', 'high_horizontal_d25_last_at')

        # Deleting field 'EurUsdMA.low_horizontal_d25'
        db.delete_column(u'rate_eurusdma', 'low_horizontal_d25')

        # Deleting field 'EurUsdMA.low_horizontal_d25_last_at'
        db.delete_column(u'rate_eurusdma', 'low_horizontal_d25_last_at')

        # Deleting field 'EurUsdMA.high_horizontal_d5'
        db.delete_column(u'rate_eurusdma', 'high_horizontal_d5')

        # Deleting field 'EurUsdMA.high_horizontal_d5_last_at'
        db.delete_column(u'rate_eurusdma', 'high_horizontal_d5_last_at')

        # Deleting field 'EurUsdMA.low_horizontal_d5'
        db.delete_column(u'rate_eurusdma', 'low_horizontal_d5')

        # Deleting field 'EurUsdMA.low_horizontal_d5_last_at'
        db.delete_column(u'rate_eurusdma', 'low_horizontal_d5_last_at')

        # Deleting field 'UsdJpyMA.open_bid'
        db.delete_column(u'rate_usdjpyma', 'open_bid')

        # Deleting field 'UsdJpyMA.high_horizontal_d25'
        db.delete_column(u'rate_usdjpyma', 'high_horizontal_d25')

        # Deleting field 'UsdJpyMA.high_horizontal_d25_last_at'
        db.delete_column(u'rate_usdjpyma', 'high_horizontal_d25_last_at')

        # Deleting field 'UsdJpyMA.low_horizontal_d25'
        db.delete_column(u'rate_usdjpyma', 'low_horizontal_d25')

        # Deleting field 'UsdJpyMA.low_horizontal_d25_last_at'
        db.delete_column(u'rate_usdjpyma', 'low_horizontal_d25_last_at')

        # Deleting field 'UsdJpyMA.high_horizontal_d5'
        db.delete_column(u'rate_usdjpyma', 'high_horizontal_d5')

        # Deleting field 'UsdJpyMA.high_horizontal_d5_last_at'
        db.delete_column(u'rate_usdjpyma', 'high_horizontal_d5_last_at')

        # Deleting field 'UsdJpyMA.low_horizontal_d5'
        db.delete_column(u'rate_usdjpyma', 'low_horizontal_d5')

        # Deleting field 'UsdJpyMA.low_horizontal_d5_last_at'
        db.delete_column(u'rate_usdjpyma', 'low_horizontal_d5_last_at')


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
            'high_horizontal_d25': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d25_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d5': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d5_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_horizontal_d25': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d25_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d5': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d5_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_bid': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
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
            'high_horizontal_d25': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d25_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d5': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'high_horizontal_d5_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_horizontal_d25': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d25_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d5': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'low_horizontal_d5_last_at': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_bid': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rate']