from django.apps import AppConfig


class RentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental'

    def ready(self):
        import rental.signals  

#  this website is terashh.. i need help building it