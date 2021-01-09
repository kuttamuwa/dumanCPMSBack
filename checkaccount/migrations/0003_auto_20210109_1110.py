# Generated by Django 3.1.5 on 2021-01-09 08:10

import checkaccount.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkaccount', '0002_auto_20210109_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnershipdocuments',
            name='board_management',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='BOARD_MANAGEMENT_PATH', null=True, upload_to='board_management/docs/', verbose_name='YONETIM KURULU YAPISI'),
        ),
        migrations.AlterField(
            model_name='partnershipdocuments',
            name='identity_copies',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='IDENTITY_COPIES_PATH', null=True, upload_to='identity_copies/docs/', verbose_name='KIMLIK KOPYALARI'),
        ),
        migrations.AlterField(
            model_name='partnershipdocuments',
            name='partnership_structure_identity_copies',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='PARTNERSHIP_STRUCTURE_PATH', null=True, upload_to='pstruct_identity_copies/docs/', verbose_name='ORTAKLIK YAPISI VE KIMLIK KOPYALARI'),
        ),
    ]
