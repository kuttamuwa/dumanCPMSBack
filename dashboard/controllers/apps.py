from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        """
        Dashboard ayağa kalkmadan önce yapılacaklar
        :return:
        """
        return super(DashboardConfig, self).ready()
