from django.db import models

from .basemodels import BaseModel
from .fields import DumanModelFileField
from .managers import DummyCheckAccountCreator


class Cities(BaseModel):
    data_id = models.AutoField(primary_key=True)
    city_plate_number = models.PositiveSmallIntegerField(db_column='CITY_PLATE_NUMBER', unique=True,
                                                         null=True)
    name = models.CharField(max_length=100, null=True, verbose_name='Şehir', db_column='IL')

    def __str__(self):
        return self.name

    class Meta:
        pass
        #db_table = 'CITIES'


class Districts(BaseModel):
    data_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, verbose_name='İlçe', db_column='ILCE')

    def __str__(self):
        return self.name


class SysDepartments(BaseModel):
    department_name = models.CharField(max_length=50, unique=True, db_column='DEPARTMENT_NAME')

    class Meta:
        db_table = 'SYS_DEPARTMENTS'

    def __str__(self):
        return self.department_name


class Sectors(BaseModel):
    name = models.CharField(max_length=50, unique=False, db_column='SECTOR_NAME', null=True)

    class Meta:
        db_table = 'SECTORS'

    def __str__(self):
        return self.name


class SysPersonnel(BaseModel):
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME', null=True, unique=False)
    surname = models.CharField(max_length=50, db_column='SURNAME', null=True, unique=False)
    username = models.CharField(max_length=50, db_column='USERNAME', null=True, unique=False)  # True
    department = models.ForeignKey(SysDepartments, on_delete=models.CASCADE, null=True,
                                   unique=False)  # if department goes?
    position = models.CharField(max_length=50, db_column='POSITION', null=True)

    class Meta:
        db_table = 'SYS_PERSONNEL'

    def __str__(self):
        return self.username


class CheckAccount(BaseModel):
    dummy_creator = DummyCheckAccountCreator()
    objects = models.Manager()

    firm_type = models.CharField(max_length=20, choices=[('Tüzel Kişilik', 'Tüzel Kişilik'),
                                                         ('Şahıs İşletmesi', 'Şahıs İşletmesi')],
                                 verbose_name='Firma Tipi', help_text='Şahıs mı Tüzel mi olduğunu giriniz',
                                 db_column='FIRM_TYPE', null=True, default='Tüzel Kişilik')
    firm_full_name = models.CharField(max_length=100, verbose_name='Firma Adı',
                                      db_column='FIRM_FULLNAME', null=True, default='Firma Test')
    taxpayer_number = models.CharField(max_length=15, verbose_name='Kimlik No',
                                       help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise Vergi No',
                                       unique=False,
                                       db_column='TAXPAYER_NUMBER', null=True)

    birthplace = models.CharField(max_length=100, verbose_name='Doğum yeri',
                                  null=True, blank=True)
    tax_department = models.CharField(max_length=100, verbose_name='Vergi Departmanı', db_column='TAX_DEPARTMENT',
                                      null=True)
    firm_address = models.CharField(max_length=200, verbose_name='Firma Adresi', db_column='FIRM_ADDRESS', null=True)

    firm_key_contact_personnel = models.CharField(max_length=70, verbose_name='Firma İletişim', null=True, )
    sector = models.CharField(max_length=70, null=True, verbose_name='Sektör')

    city = models.CharField(max_length=70, null=True, verbose_name='Şehir')
    district = models.CharField(max_length=100, null=True, verbose_name='İlçe')

    phone_number = models.CharField(max_length=15, verbose_name='Telefon numarası',
                                    unique=False, db_column='PHONE_NUMBER', null=True)
    fax = models.CharField(max_length=15, unique=False, db_column='FAX_NUMBER', verbose_name='Fax Numarası', null=True)
    web_url = models.URLField(db_column='WEB_URL', verbose_name='Web adresi', null=True)
    email_addr = models.EmailField(verbose_name='Email adresi', unique=False, db_column='EMAIL_ADDR', null=True)

    # Account Documents ... !! Attention
    activity_certificate_pdf = DumanModelFileField(
        upload_to='activity_certificates/pdfs/',
        verbose_name='Activity Certificate',
        db_column='ACTIVITY_CERTIFICATE_PATH', null=True, blank=True)

    tax_return_pdf = DumanModelFileField(
        upload_to='tax_return/pdfs/', verbose_name='Tax Return',
        db_column='TAX_RETURN_PATH', null=True, blank=True)

    authorized_signatures_list_pdf = DumanModelFileField(
        upload_to='authorized_signatures_list/pdfs/',
        verbose_name='Authorized Signatures List',
        db_column='AUTHORIZED_SIG_LIST', null=True, blank=True)

    # klasörde depolanabilir
    partnership_structure_identity_copies = DumanModelFileField('ORTAKLIK YAPISI VE KIMLIK KOPYALARI',
                                                                upload_to='pstruct_identity_copies/docs/',
                                                                db_column='PARTNERSHIP_STRUCTURE_PATH',
                                                                null=True, blank=True)

    identity_copies = DumanModelFileField('KIMLIK KOPYALARI',
                                          upload_to='identity_copies/docs/',
                                          db_column='IDENTITY_COPIES_PATH',
                                          null=True, blank=True)

    board_management = DumanModelFileField('YONETIM KURULU YAPISI',
                                           upload_to='board_management/docs/',
                                           db_column='BOARD_MANAGEMENT_PATH',
                                           null=True, blank=True)

    class Meta:
        db_table = 'CHECKACCOUNT'

    def __str__(self):
        return self.firm_full_name

    def delete_by_type(self, _type):
        if _type == 1:
            self.activity_certificate_pdf.delete()

        elif _type == 2:
            self.tax_return_pdf.delete()

        elif _type == 3:
            self.authorized_signatures_list_pdf.delete()

        elif _type == 4:
            self.partnership_structure_identity_copies.delete()

        elif _type == 5:
            self.identity_copies.delete()

        elif _type == 6:
            self.board_management.delete()

    def check_all_field_uploaded(self):
        fields = self._get_only_file_field_names()
        uploaded_fields = []

        for f in fields:
            data = getattr(self, f.attname)
            if data.name in ("", None):
                uploaded_fields.append(False)
            else:
                uploaded_fields.append(True)

        return all(uploaded_fields)

    def _get_all_field_names(self):
        return [i for i in self._meta.get_fields()]

    def _get_only_file_field_names(self):
        return [i for i in self._meta.get_fields() if isinstance(i, DumanModelFileField)]
