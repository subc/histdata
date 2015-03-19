# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GbpUsdMA'
        db.create_table(u'rate_gbpusdma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h1', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h4', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h24', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d10', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d75', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d200', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d25_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('low_horizontal_d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('low_horizontal_d25_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('high_horizontal_d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d5_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('low_horizontal_d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('low_horizontal_d5_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'rate', ['GbpUsdMA'])

        # Adding unique constraint on 'GbpUsdMA', fields ['start_at']
        db.create_unique(u'rate_gbpusdma', ['start_at'])

        # Adding model 'CandleGbpUsdM1Rate'
        db.create_table(u'rate_candlegbpusdm1rate', (
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
        db.send_create_signal(u'rate', ['CandleGbpUsdM1Rate'])

        # Adding unique constraint on 'CandleGbpUsdM1Rate', fields ['start_at']
        db.create_unique(u'rate_candlegbpusdm1rate', ['start_at'])

        # Adding model 'CandleGbpUsdH1Rate'
        db.create_table(u'rate_candlegbpusdh1rate', (
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
        db.send_create_signal(u'rate', ['CandleGbpUsdH1Rate'])

        # Adding unique constraint on 'CandleGbpUsdH1Rate', fields ['start_at']
        db.create_unique(u'rate_candlegbpusdh1rate', ['start_at'])

        # Adding model 'CandleAudUsdM5Rate'
        db.create_table(u'rate_candleaudusdm5rate', (
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
        db.send_create_signal(u'rate', ['CandleAudUsdM5Rate'])

        # Adding unique constraint on 'CandleAudUsdM5Rate', fields ['start_at']
        db.create_unique(u'rate_candleaudusdm5rate', ['start_at'])

        # Adding model 'CandleGbpUsdM5Rate'
        db.create_table(u'rate_candlegbpusdm5rate', (
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
        db.send_create_signal(u'rate', ['CandleGbpUsdM5Rate'])

        # Adding unique constraint on 'CandleGbpUsdM5Rate', fields ['start_at']
        db.create_unique(u'rate_candlegbpusdm5rate', ['start_at'])

        # Adding model 'CandleAudUsdDRate'
        db.create_table(u'rate_candleaudusddrate', (
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
        db.send_create_signal(u'rate', ['CandleAudUsdDRate'])

        # Adding unique constraint on 'CandleAudUsdDRate', fields ['start_at']
        db.create_unique(u'rate_candleaudusddrate', ['start_at'])

        # Adding model 'CandleAudUsdH1Rate'
        db.create_table(u'rate_candleaudusdh1rate', (
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
        db.send_create_signal(u'rate', ['CandleAudUsdH1Rate'])

        # Adding unique constraint on 'CandleAudUsdH1Rate', fields ['start_at']
        db.create_unique(u'rate_candleaudusdh1rate', ['start_at'])

        # Adding model 'CandleGbpUsdDRate'
        db.create_table(u'rate_candlegbpusddrate', (
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
        db.send_create_signal(u'rate', ['CandleGbpUsdDRate'])

        # Adding unique constraint on 'CandleGbpUsdDRate', fields ['start_at']
        db.create_unique(u'rate_candlegbpusddrate', ['start_at'])

        # Adding model 'AudUsdMA'
        db.create_table(u'rate_audusdma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('open_bid', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h1', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h4', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('h24', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d10', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d75', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('d200', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d25_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('low_horizontal_d25', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('low_horizontal_d25_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('high_horizontal_d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('high_horizontal_d5_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('low_horizontal_d5', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('low_horizontal_d5_last_at', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'rate', ['AudUsdMA'])

        # Adding unique constraint on 'AudUsdMA', fields ['start_at']
        db.create_unique(u'rate_audusdma', ['start_at'])

        # Adding model 'CandleAudUsdM1Rate'
        db.create_table(u'rate_candleaudusdm1rate', (
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
        db.send_create_signal(u'rate', ['CandleAudUsdM1Rate'])

        # Adding unique constraint on 'CandleAudUsdM1Rate', fields ['start_at']
        db.create_unique(u'rate_candleaudusdm1rate', ['start_at'])


    def backwards(self, orm):
        # Removing unique constraint on 'CandleAudUsdM1Rate', fields ['start_at']
        db.delete_unique(u'rate_candleaudusdm1rate', ['start_at'])

        # Removing unique constraint on 'AudUsdMA', fields ['start_at']
        db.delete_unique(u'rate_audusdma', ['start_at'])

        # Removing unique constraint on 'CandleGbpUsdDRate', fields ['start_at']
        db.delete_unique(u'rate_candlegbpusddrate', ['start_at'])

        # Removing unique constraint on 'CandleAudUsdH1Rate', fields ['start_at']
        db.delete_unique(u'rate_candleaudusdh1rate', ['start_at'])

        # Removing unique constraint on 'CandleAudUsdDRate', fields ['start_at']
        db.delete_unique(u'rate_candleaudusddrate', ['start_at'])

        # Removing unique constraint on 'CandleGbpUsdM5Rate', fields ['start_at']
        db.delete_unique(u'rate_candlegbpusdm5rate', ['start_at'])

        # Removing unique constraint on 'CandleAudUsdM5Rate', fields ['start_at']
        db.delete_unique(u'rate_candleaudusdm5rate', ['start_at'])

        # Removing unique constraint on 'CandleGbpUsdH1Rate', fields ['start_at']
        db.delete_unique(u'rate_candlegbpusdh1rate', ['start_at'])

        # Removing unique constraint on 'CandleGbpUsdM1Rate', fields ['start_at']
        db.delete_unique(u'rate_candlegbpusdm1rate', ['start_at'])

        # Removing unique constraint on 'GbpUsdMA', fields ['start_at']
        db.delete_unique(u'rate_gbpusdma', ['start_at'])

        # Deleting model 'GbpUsdMA'
        db.delete_table(u'rate_gbpusdma')

        # Deleting model 'CandleGbpUsdM1Rate'
        db.delete_table(u'rate_candlegbpusdm1rate')

        # Deleting model 'CandleGbpUsdH1Rate'
        db.delete_table(u'rate_candlegbpusdh1rate')

        # Deleting model 'CandleAudUsdM5Rate'
        db.delete_table(u'rate_candleaudusdm5rate')

        # Deleting model 'CandleGbpUsdM5Rate'
        db.delete_table(u'rate_candlegbpusdm5rate')

        # Deleting model 'CandleAudUsdDRate'
        db.delete_table(u'rate_candleaudusddrate')

        # Deleting model 'CandleAudUsdH1Rate'
        db.delete_table(u'rate_candleaudusdh1rate')

        # Deleting model 'CandleGbpUsdDRate'
        db.delete_table(u'rate_candlegbpusddrate')

        # Deleting model 'AudUsdMA'
        db.delete_table(u'rate_audusdma')

        # Deleting model 'CandleAudUsdM1Rate'
        db.delete_table(u'rate_candleaudusdm1rate')


    models = {
        u'rate.audusdma': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'AudUsdMA'},
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
        u'rate.candleaudusddrate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleAudUsdDRate'},
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
        u'rate.candleaudusdh1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleAudUsdH1Rate'},
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
        u'rate.candleaudusdm1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleAudUsdM1Rate'},
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
        u'rate.candleaudusdm5rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleAudUsdM5Rate'},
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
        u'rate.candlegbpusddrate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleGbpUsdDRate'},
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
        u'rate.candlegbpusdh1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleGbpUsdH1Rate'},
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
        u'rate.candlegbpusdm1rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleGbpUsdM1Rate'},
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
        u'rate.candlegbpusdm5rate': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'CandleGbpUsdM5Rate'},
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
        u'rate.gbpusdma': {
            'Meta': {'unique_together': "((u'start_at',),)", 'object_name': 'GbpUsdMA'},
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