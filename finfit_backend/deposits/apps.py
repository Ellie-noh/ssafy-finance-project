from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DepositsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deposits'

    def ready(self):
        # post_migrate 시그널 연결
        post_migrate.connect(self.load_deposit_data, sender=self)

    def load_deposit_data(self, sender, **kwargs):
        # management command 호출
        from django.core.management import call_command
        try:
            call_command('load_deposit_data')
        except Exception as e:
            print(f"Error loading deposit data: {e}")
