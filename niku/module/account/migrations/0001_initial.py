# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'account_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('order_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('confirm_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('end_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True)),
            ('prev_rate_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True)),
            ('oanda_ticket_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('ai_board_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('_currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('buy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('limit_tick', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stop_limit_tick', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('spread', self.gf('django.db.models.fields.FloatField')()),
            ('open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('lowerBound', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('upperBound', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('real_open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('stop_limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('real', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('profit', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('units', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('error', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
        ))
        db.send_create_signal(u'account', ['Order'])

        # Adding model 'OandaTransaction'
        db.create_table(u'account_oandatransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oanda_transaction_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('oanda_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('order_type', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('account_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('oanda_trade_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('accountBalance', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('pl', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('_data', self.gf('utils.fields.ObjectField')(default=None, null=True)),
        ))
        db.send_create_signal(u'account', ['OandaTransaction'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'account_order')

        # Deleting model 'OandaTransaction'
        db.delete_table(u'account_oandatransaction')


    models = {
        u'account.oandatransaction': {
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
            'pl': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'account.order': {
            'Meta': {'object_name': 'Order'},
            '_currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'buy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'confirm_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'limit_tick': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'lowerBound': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'oanda_ticket_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'order_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'prev_rate_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'profit': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'real_open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'spread': ('django.db.models.fields.FloatField', [], {}),
            'stop_limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'stop_limit_tick': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'upperBound': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['account']