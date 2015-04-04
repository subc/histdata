# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AIBoardHistory.trade_stop_at'
        db.delete_column(u'board_aiboardhistory', 'trade_stop_at')

        # Adding field 'AIBoardHistory.open_position_count'
        db.add_column(u'board_aiboardhistory', 'open_position_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'AIBoardHistory.open_position_profit'
        db.add_column(u'board_aiboardhistory', 'open_position_profit',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'AIBoardHistory.open_position_tick'
        db.add_column(u'board_aiboardhistory', 'open_position_tick',
                      self.gf('django.db.models.fields.FloatField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'AIBoardHistory.trade_stop_at'
        db.add_column(u'board_aiboardhistory', 'trade_stop_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True),
                      keep_default=False)

        # Deleting field 'AIBoardHistory.open_position_count'
        db.delete_column(u'board_aiboardhistory', 'open_position_count')

        # Deleting field 'AIBoardHistory.open_position_profit'
        db.delete_column(u'board_aiboardhistory', 'open_position_profit')

        # Deleting field 'AIBoardHistory.open_position_tick'
        db.delete_column(u'board_aiboardhistory', 'open_position_tick')


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
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True'})
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