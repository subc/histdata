# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AIBoard.account'
        db.add_column(u'board_aiboard', 'account',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AIBoard.account'
        db.delete_column(u'board_aiboard', 'account')


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
            '_currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'buy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'lowerBound': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'oanda_ticket_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'order_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'prev_rate_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            'profit': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'real_limit_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'real_open_rate': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'spread': ('django.db.models.fields.FloatField', [], {}),
            'stop_limit_rate': ('django.db.models.fields.FloatField', [], {}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'upperBound': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'})
        }
    }

    complete_apps = ['board']