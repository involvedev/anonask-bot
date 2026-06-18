import secrets

# Генерация уникальной ссылки для пользователя
def generate_link():
    return secrets.token_urlsafe(8)