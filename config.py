import os

# إعدادات عامة وبوت
BOT_NAME = "llie⚫"
# رابط الصورة المتحركة (GIF) المباشر للعمل مع Telegram
WELCOME_ANIMATION_URL = "https://i.postimg.cc/YCJwm7xB/2ea81f452613dc740e19a5af784425ed-ezgif-com-resize.gif"

# استخدم متغير بيئي لرمز البوت بدل تضمينه هنا مباشرة
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# DSN لقاعدة البيانات PostgreSQL (تعديل إلى إعداداتك الحقيقية):
DB_DSN = os.getenv("DB_DSN", "postgresql://user:password@localhost:5432/dbname")

# Provide compatibility variable DATABASE_URL used by database/pg_db.py
# Tie DATABASE_URL to DB_DSN so both names work interchangeably
DATABASE_URL = os.getenv("DATABASE_URL", DB_DSN)

# أقصى تزامن (Concurrency) يُستخدم في بعض بيئات النشر أو تكوينات الخادم
# يمكنك تعيينه عبر متغير البيئة MAX_CONCURRENCY، أو ترك القيمة الافتراضية 100
try:
    MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "100"))
except Exception:
    MAX_CONCURRENCY = 100

# Compatibility variables expected by bot.py
try:
    MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", str(MAX_CONCURRENCY)))
except Exception:
    MAX_CONCURRENT_TASKS = MAX_CONCURRENCY

# START_FROM_LATEST determines whether to drop pending updates (True/False)
START_FROM_LATEST = os.getenv("START_FROM_LATEST", "True").lower() in ("1", "true", "yes")

# BROADCAST_ADMIN_IDS: comma-separated list in env, e.g. "12345,67890"
_broadcast_env = os.getenv("BROADCAST_ADMIN_IDS", "")
if _broadcast_env:
    try:
        BROADCAST_ADMIN_IDS = [int(x.strip()) for x in _broadcast_env.split(",") if x.strip()]
    except Exception:
        BROADCAST_ADMIN_IDS = []
else:
    BROADCAST_ADMIN_IDS = []

# Backup default requested by user
MAX_CONCURRENCY = MAX_CONCURRENCY
