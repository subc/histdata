# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OandaTransaction'
        db.create_table(u'oanda_oandatransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oanda_transaction_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('oanda_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('order_type', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('account_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('oanda_ticket_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('_data', self.gf('utils.fields.ObjectField')(default=None, null=True)),
        ))
        db.send_create_signal(u'oanda', ['OandaTransaction'])


    def backwards(self, orm):
        # Deleting model 'OandaTransaction'
        db.delete_table(u'oanda_oandatransaction')


    models = {
        u'oanda.oandatransaction': {
            'Meta': {'object_name': 'OandaTransaction'},
            '_data': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'account_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oanda_ticket_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'oanda_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oanda_transaction_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oanda']