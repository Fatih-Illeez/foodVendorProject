from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    #this function is necessary to make signals.py work
    def ready(self):
        import accounts.signals