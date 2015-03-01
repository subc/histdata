# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeneticEliteHistory'
        db.create_table(u'genetic_geneticelitehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('genetic_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, db_index=True)),
            ('currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('profit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profit_max', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profit_min', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('elite', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('test_start_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('test_end_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'genetic', ['GeneticEliteHistory'])

        # Adding unique constraint on 'GeneticEliteHistory', fields ['genetic_id']
        db.create_unique(u'genetic_geneticelitehistory', ['genetic_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GeneticEliteHistory', fields ['genetic_id']
        db.delete_unique(u'genetic_geneticelitehistory', ['genetic_id'])

        # Deleting model 'GeneticEliteHistory'
        db.delete_table(u'genetic_geneticelitehistory')


    models = {
        u'genetic.geneticelitehistory': {
            'Meta': {'unique_together': "((u'genetic_id',),)", 'object_name': 'GeneticEliteHistory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'elite': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'genetic_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'profit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit_min': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'test_end_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'test_start_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'genetic.genetichistory': {
            'Meta': {'object_name': 'GeneticHistory'},
            'ai': ('utils.fields.ObjectField', [], {'default': 'None', 'null': 'True'}),
            'ai_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'elite': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'generation': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'profit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit_min': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['genetic']