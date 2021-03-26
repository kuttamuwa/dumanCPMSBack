from django.db import models
from faker import Faker

fake = Faker(['tr_TR'])


class BaseDummyCreator(models.Manager):
    primitive = False
    tr_choice = 'tr_TR'
    en_choice = 'en_us'

    @classmethod
    def add_en(cls):
        fake.locales.append(cls.en_choice)

    @classmethod
    def del_en(cls):
        fake.locales.remove(cls.en_choice)

    @classmethod
    def add_tr(cls):
        fake.locales.append(cls.tr_choice)

    @classmethod
    def del_tr(cls):
        fake.locales.remove(cls.tr_choice)

    def _get_max_oid(self):
        return self.model.objects.all().last().pk + 1

    def _gen_sahis_firm_name(self, **kwargs):
        if kwargs.get('username'):
            return f"{kwargs.get('username')}_{self._get_max_oid()} Şirketi"
        return fake.name()

    def _gen_tuzel_firm_name(self, **kwargs):
        if kwargs.get('username'):
            return f"{kwargs.get('username')}_{self._get_max_oid()}"

        return fake.bs()

    def gen_firm_full_name(self, firm_type='Şahıs İşletmesi'):
        if firm_type == 'Tüzel Kişilik':
            return self._gen_tuzel_firm_name()

        elif firm_type == 'Şahıs İşletmesi':
            return self._gen_sahis_firm_name()

    def gen_city(self):
        return "Ankara"

    def gen_district(self):
        return "Keçiören"

    def gen_address(self):
        return "Bağlarbaşı Mahallesi Gelendost Sokak 3-5"

    def gen_key_contact_personnel(self):
        return "Umut Üçok"

    def gen_sector(self):
        return "Gıda"

    def gen_phone_number(self):
        return ""

    def gen_fax_number(self):
        return ""

    def gen_web_url(self):
        return "https://www.dumanarge.com/"

    def gen_email_addr(self):
        return "info@dumanarge.com"


class DummyCheckAccountCreator(BaseDummyCreator):
    def gen_aburcubur_attrs(self, **kwargs):
        """


        :param kwargs:
        :return:
        """
        kwargs['birthplace'] = self.gen_city()
        kwargs['tax_department'] = self.gen_district()
        kwargs['firm_address'] = self.gen_address()
        kwargs['firm_key_contact_personnel'] = self.gen_key_contact_personnel()
        kwargs['sector'] = self.gen_sector()
        kwargs['city'] = self.gen_city()
        kwargs['district'] = self.gen_district()
        kwargs['phone_number'] = self.gen_phone_number()
        kwargs['fax'] = self.gen_fax_number()
        kwargs['web_url'] = self.gen_web_url()
        kwargs['email_addr'] = self.gen_email_addr()

        return kwargs

    def gen_user(self, firm_type='Şahıs İşletmesi', *args, **kwargs):
        kwargs['firm_full_name'] = self.gen_firm_full_name()
        kwargs = self.gen_aburcubur_attrs(**kwargs)

        obj = self.create(firm_type=firm_type, *args, **kwargs)
        print(f"Sanal hesap üretildi : {obj.firm_full_name}")
        return obj

    def check_or_create_dummy(self, adsoyad, *args, **kwargs):
        try:
            return self.get(firm_full_name=adsoyad)
        except models.ObjectDoesNotExist:
            return self.gen_user(*args, **kwargs)
