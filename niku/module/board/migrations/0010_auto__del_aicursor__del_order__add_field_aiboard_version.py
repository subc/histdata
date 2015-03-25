# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AICursor'
        db.delete_table(u'board_aicursor')

        # Deleting model 'Order'
        db.delete_table(u'board_order')

        # Adding field 'AIBoard.version'
        db.add_column(u'board_aiboard', 'version',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'AICursor'
        db.create_table(u'board_aicursor', (
            ('last_order_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ai_board_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal(u'board', ['AICursor'])

        # Adding model 'Order'
        db.create_table(u'board_order', (
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oanda_ticket_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('profit', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('confirm_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('upperBound', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('end_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True)),
            ('spread', self.gf('django.db.models.fields.FloatField')()),
            ('limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('ai_board_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('real', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('real_limit_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('buy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('prev_rate_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True)),
            ('stop_limit_rate', self.gf('django.db.models.fields.FloatField')()),
            ('_currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('units', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('lowerBound', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('error', self.gf('django.db.models.fields.TextField')(default=None, null=True)),
            ('real_open_rate', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
        ))
        db.send_create_signal(u'board', ['Order'])

        # Deleting field 'AIBoard.version'
        db.delete_column(u'board_aiboard', 'version')


    models = {
        u'board.aiboard': {
            'Meta': {'object_name': 'AIBoard'},
            'account': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'ai_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ai_param': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'enable': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['board']