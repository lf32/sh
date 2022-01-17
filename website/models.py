from django.db import models

class Urldb(models.Model):
    data_url_str = models.CharField(max_length=25, primary_key=True)
    data_long_url = models.CharField(max_length=200)
    
    def __str(self):
        return self.data_url_str
