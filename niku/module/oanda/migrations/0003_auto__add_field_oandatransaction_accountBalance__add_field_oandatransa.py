# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OandaTransaction.accountBalance'
        db.add_column(u'oanda_oandatransaction', 'accountBalance',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'OandaTransaction.pl'
        db.add_column(u'oanda_oandatransaction', 'pl',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OandaTransaction.accountBalance'
        db.delete_column(u'oanda_oandatransaction', 'accountBalance')

        # Deleting field 'OandaTransaction.pl'
        db.delete_column(u'oanda_oandatransaction', 'pl')


    models = {
        u'oanda.oandatransaction': {
            'Meta': {'object_name': 'OandaTransaction'},
            '_data': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'accountBalance': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'account_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oanda_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oanda_trade_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'oanda_transaction_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'pl': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oanda']