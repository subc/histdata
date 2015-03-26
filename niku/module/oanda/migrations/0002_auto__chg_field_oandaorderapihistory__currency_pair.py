# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OandaOrderApiHistory._currency_pair'
        db.alter_column(u'oanda_oandaorderapihistory', '_currency_pair', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):

        # Changing field 'OandaOrderApiHistory._currency_pair'
        db.alter_column(u'oanda_oandaorderapihistory', '_currency_pair', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    models = {
        u'oanda.oandaorderapihistory': {
            'Meta': {'object_name': 'OandaOrderApiHistory'},
            '_currency_pair': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'units': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['oanda']