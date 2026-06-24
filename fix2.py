with open('backend/core/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "        user.xp_to_next_level = user.xp_to_reach_level(1)\n        user.save()\n        return user",
    "        return user"
)
with open('backend/core/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
