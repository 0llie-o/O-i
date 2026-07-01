import os

# إعدادات عامة وبوت
BOT_NAME = "llie⚫"
WELCOME_ANIMATION_URL = "https://postimg.cc"

# استخدم متغير بيئي لرمز البوت بدل تضمينه هنا مباشرة
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# مثال DSN لقاعدة البيانات — عدّله إلى إعداداتك الحقيقية عند الحاجة
# DB_DSN = "postgresql://user:password@host:port/database"
