from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class SavedPassword(models.Model):
    website = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    saver = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.saver)+' - '+str(self.website)

    def de_encrypt(self, message, key):
        SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:;<=>?@'
        translated = ''

        for symbol in message:
            symbolIndex = SYMBOLS.find(symbol)
            if symbolIndex == -1:
                translated += symbol
            else:
                symbolIndex += key

                if symbolIndex >= len(SYMBOLS):
                    symbolIndex -= len(SYMBOLS)
                elif symbolIndex < 0:
                    symbolIndex += len(SYMBOLS)

                translated += SYMBOLS[symbolIndex]
        return translated

    def save(self, *args, **kwargs):
        decrypt_key = 13
        message = str(self.password)

        self.password = self.de_encrypt(message, decrypt_key)
        super().save()

# j@2YafCVBc10