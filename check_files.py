import os

print(f"📍 Скрипт запущен в: {os.getcwd()}")
files = os.listdir('.')
required = ["NAME.html", "NAME.json", "index.js", "lottie.js"]

for f in required:
    status = "✅ НАЙДЕН" if f in files else "❌ ОТСУТСТВУЕТ"
    print(f"{f}: {status}")