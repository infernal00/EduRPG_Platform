import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Users(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email")
    coins = models.IntegerField(default=100, verbose_name="Монеты")
    xp = models.IntegerField(default=0, verbose_name="Опыт")
    hearts = models.IntegerField(default=5, verbose_name="Жизни")
    password = models.CharField(max_length=128, verbose_name="Пароль")

    def set_password(self, raw_password):
        """Хэширует пароль перед сохранением в базу данных."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Проверяет, совпадает ли введенный пароль с хэшем в базе данных."""
        return check_password(raw_password, self.password)

    def add_coins(self, amount):
        self.coins += amount
        self.save()
    
    def lose_heart(self):
        self.hearts -= 1
        self.save()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username