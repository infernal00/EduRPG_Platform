from django.contrib import admin
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'coins', 'xp', 'hearts')
    search_fields = ('username', 'email')
    list_filter = ('coins', 'hearts')
    
    # Скроем отображение хэша пароля в общем списке для красоты,
    # но оставим поле при редактировании.
    fields = ('username', 'email', 'password', 'coins', 'xp', 'hearts')

    def save_model(self, request, obj, form, change):
        """
        Переопределяем сохранение модели в админке.
        Если пароль был изменен или это новый пользователь — хэшируем его.
        """
        # Проверяем, изменился ли пароль (или это новый юзер)
        if 'password' in form.changed_data or not change:
            obj.set_password(obj.password)
            
        super().save_model(request, obj, form, change)