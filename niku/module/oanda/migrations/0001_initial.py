# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OandaOrderApiHistory'
        db.create_table(u'oanda_oandaorderapihistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('units', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('_currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('response', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oanda', ['OandaOrderApiHistory'])


    def backwards(self, orm):
        # Deleting model 'OandaOrderApiHistory'
        db.delete_table(u'oanda_oandaorderapihistory')


    models = {
        u'oanda.oandaorderapihistory': {
            'Meta': {'object_name': 'OandaOrderApiHistory'},
            '_currency_pair': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oanda']