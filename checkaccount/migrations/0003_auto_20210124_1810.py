# Generated by Django 3.1.5 on 2021-01-24 15:10

import checkaccount.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkaccount', '0002_auto_20210118_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partnershipdocuments',
            name='customer',
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='activity_certificate_pdf',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='ACTIVITY_CERTIFICATE_PATH', null=True, upload_to='activity_certificates/pdfs/', verbose_name='Activity Certificate'),
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='authorized_signatures_list_pdf',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='AUTHORIZED_SIG_LIST', null=True, upload_to='authorized_signatures_list/pdfs/', verbose_name='Authorized Signatures List'),
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='board_management',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='BOARD_MANAGEMENT_PATH', null=True, upload_to='board_management/docs/', verbose_name='YONETIM KURULU YAPISI'),
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='identity_copies',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='IDENTITY_COPIES_PATH', null=True, upload_to='identity_copies/docs/', verbose_name='KIMLIK KOPYALARI'),
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='partnership_structure_identity_copies',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='PARTNERSHIP_STRUCTURE_PATH', null=True, upload_to='pstruct_identity_copies/docs/', verbose_name='ORTAKLIK YAPISI VE KIMLIK KOPYALARI'),
        ),
        migrations.AddField(
            model_name='checkaccount',
            name='tax_return_pdf',
            field=checkaccount.models.fields.DumanModelFileField(blank=True, db_column='TAX_RETURN_PATH', null=True, upload_to='tax_return/pdfs/', verbose_name='Tax Return'),
        ),
        migrations.DeleteModel(
            name='AccountDocuments',
        ),
        migrations.DeleteModel(
            name='PartnershipDocuments',
        ),
    ]