# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GeneticEliteHistory', fields ['genetic_id']
        db.delete_unique(u'genetic_geneticelitehistory', ['genetic_id'])

        # Deleting model 'GeneticEliteHistory'
        db.delete_table(u'genetic_geneticelitehistory')


    def backwards(self, orm):
        # Adding model 'GeneticEliteHistory'
        db.create_table(u'genetic_geneticelitehistory', (
            ('comment', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True)),
            ('profitH1_min', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profitM1_max', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('profitM5_max', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profitM5', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profitM1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('profitH1_max', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('profitM1_min', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('genetic_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, db_index=True)),
            ('profitM5_min', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('progress', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True)),
            ('elite', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profitH1', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'genetic', ['GeneticEliteHistory'])

        # Adding unique constraint on 'GeneticEliteHistory', fields ['genetic_id']
        db.create_unique(u'genetic_geneticelitehistory', ['genetic_id'])


    models = {
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