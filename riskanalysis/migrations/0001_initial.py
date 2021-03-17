# Generated by Django 3.1.5 on 2021-03-16 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
            options={
                'db_table': 'RISK_BASEMODEL',
            },
        ),
        migrations.CreateModel(
            name='DataSetModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='riskanalysis.basemodel')),
                ('limit', models.PositiveIntegerField(blank=True, db_column='LIMIT', null=True, verbose_name='Limit')),
                ('teminat_durumu', models.BooleanField(blank=True, db_column='TEMINAT_DURUMU', default=False, help_text='Teminat durumu', null=True, verbose_name='Teminat Durumu')),
                ('teminat_tutari', models.PositiveIntegerField(blank=True, db_column='TEMINAT_TUTARI', help_text='Teminat Tutarı', null=True, verbose_name='Teminat Tutarı')),
                ('vade', models.IntegerField(blank=True, db_column='VADE_GUNU', help_text='Vade Günü', null=True, verbose_name='Vade Günü')),
                ('vade_asimi_ortalamasi', models.IntegerField(blank=True, db_column='ORT_VADE_ASIMI', help_text='Vade aşımı ortalaması giriniz', null=True, verbose_name='Vade aşımı ortalaması')),
                ('odeme_sikligi', models.IntegerField(blank=True, db_column='ODEME_SIKLIGI', help_text='Ödeme sıklığı', null=True, verbose_name='Ödeme sıklığı')),
                ('ort_siparis_tutari_12ay', models.FloatField(blank=True, db_column='ORT_SIPARIS_TUTARI_12', help_text='Son 12 ay ortalama sipariş tutarı', null=True, verbose_name='Son 12 Ay Ortalama Sipariş Tutarı')),
                ('ort_siparis_tutari_1ay', models.FloatField(blank=True, db_column='ORT_SIPARIS_TUTARI_1', help_text='Son 1 ay ortalama sipariş tutarı', null=True, verbose_name='Son 1 Ay Ortalama Sipariş Tutarı')),
                ('iade_yuzdesi_1', models.PositiveSmallIntegerField(blank=True, db_column='PAYBACK_PERC_LAST', help_text='Son ay iade yuzdesi', null=True, verbose_name='Son ay iade yüzdesi')),
                ('iade_yuzdesi_12', models.FloatField(blank=True, db_column='PAYBACK_PERC_12', help_text='Son 12 ay iade yüzdesi', null=True, verbose_name='Son 12 ay iade yüzdesi')),
                ('ort_gecikme_gun_sayisi', models.SmallIntegerField(blank=True, db_column='AVG_DELAY_TIME', help_text='Ort gecikme gun sayisi', null=True, verbose_name='Ortalama gecikme gün sayısı')),
                ('ort_gecikme_gun_bakiyesi', models.IntegerField(blank=True, db_column='MATURITY_EXCEED_AVG', help_text='Ortalama gecikme gun bakiyesi', null=True, verbose_name='Ortalama Gecikme Gün Bakiyesi')),
                ('bakiye', models.PositiveIntegerField(blank=True, db_column='BALANCE', help_text='Bakiye', null=True, verbose_name='Bakiye')),
                ('general_point', models.FloatField(blank=True, db_column='GENERAL_POINT', null=True, verbose_name='Genel Puan')),
                ('musteri', models.ForeignKey(blank=True, db_column='CUSTOMER', null=True, on_delete=django.db.models.deletion.PROTECT, to='checkaccount.checkaccount', verbose_name='İlişkili Müşteri')),
            ],
            options={
                'db_table': 'RISK_DATA',
            },
            bases=('riskanalysis.basemodel',),
        ),
        migrations.CreateModel(
            name='RiskDataSetPoints',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='riskanalysis.basemodel')),
                ('point', models.FloatField(blank=True, db_column='CALC_PTS', null=True)),
                ('variable', models.CharField(blank=True, db_column='VARIABLE', max_length=100, null=True)),
                ('risk_dataset', models.ForeignKey(db_column='RELATED_RISK', null=True, on_delete=django.db.models.deletion.SET_NULL, to='riskanalysis.datasetmodel')),
            ],
            options={
                'db_table': 'RISK_DATASET_POINTS',
            },
            bases=('riskanalysis.basemodel',),
        ),
    ]
