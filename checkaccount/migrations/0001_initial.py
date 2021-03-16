# Generated by Django 3.1.5 on 2021-03-16 10:58

import checkaccount.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckAccount',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('firm_type', models.CharField(choices=[('Tüzel Kişilik', 'Tüzel Kişilik'), ('Şahıs İşletmesi', 'Şahıs İşletmesi')], db_column='FIRM_TYPE', default='Tüzel Kişilik', help_text='Şahıs mı Tüzel mi olduğunu giriniz', max_length=20, null=True, verbose_name='Firma Tipi')),
                ('firm_full_name', models.CharField(db_column='FIRM_FULLNAME', default='Firma Test', max_length=100, null=True, verbose_name='Firma Adı')),
                ('taxpayer_number', models.CharField(db_column='TAXPAYER_NUMBER', help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise Vergi No', max_length=15, null=True, verbose_name='Kimlik No')),
                ('birthplace', models.CharField(blank=True, max_length=100, null=True, verbose_name='Doğum yeri')),
                ('tax_department', models.CharField(db_column='TAX_DEPARTMENT', max_length=100, null=True, verbose_name='Vergi Departmanı')),
                ('firm_address', models.CharField(db_column='FIRM_ADDRESS', max_length=200, null=True, verbose_name='Firma Adresi')),
                ('firm_key_contact_personnel', models.CharField(max_length=70, null=True, verbose_name='Firma İletişim')),
                ('sector', models.CharField(max_length=70, null=True, verbose_name='Sektör')),
                ('city', models.CharField(max_length=70, null=True, verbose_name='Şehir')),
                ('district', models.CharField(max_length=100, null=True, verbose_name='İlçe')),
                ('phone_number', models.CharField(db_column='PHONE_NUMBER', max_length=15, null=True, verbose_name='Telefon numarası')),
                ('fax', models.CharField(db_column='FAX_NUMBER', max_length=15, null=True, verbose_name='Fax Numarası')),
                ('web_url', models.URLField(db_column='WEB_URL', null=True, verbose_name='Web adresi')),
                ('email_addr', models.EmailField(db_column='EMAIL_ADDR', max_length=254, null=True, verbose_name='Email adresi')),
                ('activity_certificate_pdf', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='ACTIVITY_CERTIFICATE_PATH', null=True, upload_to='activity_certificates/pdfs/', verbose_name='Activity Certificate')),
                ('tax_return_pdf', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='TAX_RETURN_PATH', null=True, upload_to='tax_return/pdfs/', verbose_name='Tax Return')),
                ('authorized_signatures_list_pdf', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='AUTHORIZED_SIG_LIST', null=True, upload_to='authorized_signatures_list/pdfs/', verbose_name='Authorized Signatures List')),
                ('partnership_structure_identity_copies', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='PARTNERSHIP_STRUCTURE_PATH', null=True, upload_to='pstruct_identity_copies/docs/', verbose_name='ORTAKLIK YAPISI VE KIMLIK KOPYALARI')),
                ('identity_copies', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='IDENTITY_COPIES_PATH', null=True, upload_to='identity_copies/docs/', verbose_name='KIMLIK KOPYALARI')),
                ('board_management', checkaccount.models.fields.DumanModelFileField(blank=True, db_column='BOARD_MANAGEMENT_PATH', null=True, upload_to='board_management/docs/', verbose_name='YONETIM KURULU YAPISI')),
            ],
            options={
                'db_table': 'CHECKACCOUNT',
            },
            managers=[
                ('dummy_creator', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('city_plate_number', models.PositiveSmallIntegerField(db_column='CITY_PLATE_NUMBER', null=True, unique=True)),
                ('name', models.CharField(db_column='IL', max_length=100, null=True, verbose_name='Şehir')),
            ],
        ),
        migrations.CreateModel(
            name='Sectors',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('name', models.CharField(db_column='SECTOR_NAME', max_length=50, null=True)),
            ],
            options={
                'db_table': 'SECTORS',
            },
        ),
        migrations.CreateModel(
            name='SysDepartments',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('department_name', models.CharField(db_column='DEPARTMENT_NAME', max_length=50, unique=True)),
            ],
            options={
                'db_table': 'SYS_DEPARTMENTS',
            },
        ),
        migrations.CreateModel(
            name='SysPersonnel',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('firstname', models.CharField(db_column='FIRSTNAME', max_length=50, null=True)),
                ('surname', models.CharField(db_column='SURNAME', max_length=50, null=True)),
                ('username', models.CharField(db_column='USERNAME', max_length=50, null=True)),
                ('position', models.CharField(db_column='POSITION', max_length=50, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checkaccount.sysdepartments')),
            ],
            options={
                'db_table': 'SYS_PERSONNEL',
            },
        ),
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE', verbose_name='Created Date')),
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='ILCE', max_length=100, null=True, verbose_name='İlçe')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checkaccount.cities')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
