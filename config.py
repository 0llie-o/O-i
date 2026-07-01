import os

# إعدادات عامة وبوت
BOT_NAME = "llie⚫"
# رابط الصورة المتحركة (GIF) المباشر للعمل مع Telegram
WELCOME_ANIMATION_URL = "https://i.postimg.cc/YCJwm7xB/2ea81f452613dc740e19a5af784425ed-ezgif-com-resize.gif"

# استخدم متغير بيئي لرمز البوت بدل تضمينه هنا مباشرة
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# DSN لقاعدة البيانات PostgreSQL (تعديل إلى إعداداتك الحقيقية):
DB_DSN = os.getenv("DB_DSN", "postgresql://user:password@localhost:5432/dbname")
