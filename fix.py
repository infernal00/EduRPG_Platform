with open('backend/core/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("'avatar_url', ", "")
content = content.replace(", 'avatar_url'", "")
with open('backend/core/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - avatar_url removed')
