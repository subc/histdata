# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'OandaTransaction.oanda_ticket_id'
        db.delete_column(u'oanda_oandatransaction', 'oanda_ticket_id')

        # Adding field 'OandaTransaction.oanda_trade_id'
        db.add_column(u'oanda_oandatransaction', 'oanda_trade_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'OandaTransaction.oanda_ticket_id'
        db.add_column(u'oanda_oandatransaction', 'oanda_ticket_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Deleting field 'OandaTransaction.oanda_trade_id'
        db.delete_column(u'oanda_oandatransaction', 'oanda_trade_id')


    models = {
        u'oanda.oandatransaction': {
            'Meta': {'object_name': 'OandaTransaction'},
            '_data': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'account_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oanda_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oanda_trade_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'oanda_transaction_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oanda']