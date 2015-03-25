# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.ai_version'
        db.add_column(u'account_order', 'ai_version',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'Order.profit_tick'
        db.add_column(u'account_order', 'profit_tick',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.ai_version'
        db.delete_column(u'account_order', 'ai_version')

        # Deleting field 'Order.profit_tick'
        db.delete_column(u'account_order', 'profit_tick')


    models = {
        u'account.oandatransaction': {
            'Meta': {'object_name': 'OandaTransaction'},
            '_data': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'accountBalance': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'account_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'oanda_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oanda_trade_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'oanda_transaction_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'pl': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'account.order': {
            'Meta': {'object_name': 'Order'},
            '_currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ai_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'buy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_tick': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'order_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'prev_rate_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'profit': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'profit_tick': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'real_close_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_close_spread': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_limit_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_stop_limit_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'spread': ('django.db.models.fields.FloatField', [], {}),
            'stop_limit_tick': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['account']