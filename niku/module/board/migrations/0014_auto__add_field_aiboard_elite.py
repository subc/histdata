# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AIBoard.elite'
        db.add_column(u'board_aiboard', 'elite',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AIBoard.elite'
        db.delete_column(u'board_aiboard', 'elite')


    models = {
        u'board.aiboard': {
            'Meta': {'object_name': 'AIBoard'},
            'account': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'ai_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ai_param': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'elite': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'enable': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'real': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'})
        },
        u'board.aiboarddisablehistory': {
            'Meta': {'object_name': 'AIBoardDisableHistory'},
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_position_tick': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'sum_tick': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'trade_count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'board.aiboardhistory': {
            'Meta': {'object_name': 'AIBoardHistory'},
            'after_units': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ai_board_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'before_units': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_rank_up': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_position_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'open_position_profit': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'open_position_tick': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'profit_average': ('django.db.models.fields.FloatField', [], {}),
            'profit_summary': ('django.db.models.fields.FloatField', [], {}),
            'profit_tick_average': ('django.db.models.fields.FloatField', [], {}),
            'profit_tick_summary': ('django.db.models.fields.FloatField', [], {}),
            'trade_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'trade_end_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'trade_start_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'})
        }
    }

    complete_apps = ['board']