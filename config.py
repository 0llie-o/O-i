import os

# إعدادات عامة وبوت
BOT_NAME = "llie⚫"
WELCOME_ANIMATION_URL = "https://postimg.cc"

# استخدم متغير بيئي لرمز البوت بدل تضمينه هنا مباشرة
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# DSN لقاعدة البيانات PostgreSQL (تعديل إلى إعداداتك الحقيقية):
DB_DSN = os.getenv("DB_DSN", "postgresql://user:password@localhost:5432/dbname")
