# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AIBoard'
        db.create_table(u'board_aiboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('real', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ai_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ai_param', self.gf('utils.fields.ObjectField')(default=None, null=True)),
            ('currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('enable', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'board', ['AIBoard'])

        # Adding model 'AICursor'
        db.create_table(u'board_aicursor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ai_board_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('last_order_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal(u'board', ['AICursor'])

        # Adding model 'Order'
        db.create_table(u'board_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('order_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('end_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True)),
            ('oanda_ticket_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('ai_board_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('buy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('spread', self.gf('django.db.models.fields.FloatField')()),
            ('open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('real_open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('stop_limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('real_limit_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('real', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('profit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'board', ['Order'])


    def backwards(self, orm):
        # Deleting model 'AIBoard'
        db.delete_table(u'board_aiboard')

        # Deleting model 'AICursor'
        db.delete_table(u'board_aicursor')

        # Deleting model 'Order'
        db.delete_table(u'board_order')


    models = {
        u'board.aiboard': {
            'Meta': {'object_name': 'AIBoard'},
            'ai_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ai_param': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'enable': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'board.aicursor': {
            'Meta': {'object_name': 'AICursor'},
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_order_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'board.order': {
            'Meta': {'object_name': 'Order'},
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'buy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'oanda_ticket_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'order_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'profit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'real_limit_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'spread': ('django.db.models.fields.FloatField', [], {}),
            'stop_limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['board']