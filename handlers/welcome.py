from aiogram import Router
from aiogram.types import Message, User
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import WELCOME_ANIMATION_URL, BOT_NAME
from handlers.states import WelcomeStates
import db
import logging

log = logging.getLogger(__name__)
router = Router()

async def format_welcome_text(template: str, user: User, chat_title: str | None = None) -> str:
    """
    يستبدل الـ placeholders {name} و {chat} بالنصّ المناسب.
    """
    name = user.full_name if user else "{name}"
    chat = chat_title or "{chat}"
    return template.replace("{name}", name).replace("{chat}", str(chat))

async def send_welcome(bot, chat_id: int, user: User, welcome_template: str | None = None, chat_title: str | None = None):
    """
    ترسل رسالة ترحيب كـ Animation (GIF) باستخدام WELCOME_ANIMATION_URL
    ويكون النص كتعليق (caption) مع استبدال المتغيرات {name} و {chat}.
    """
    if not welcome_template:
        # نص افتراضي - يمكنك تغييره أو جلبه من DB
        welcome_template = (
            "مرحبًا {name} في {chat}!\n\n"
            f"يسرّني أن أرحب بكم — هذا بوت {BOT_NAME} هنا للمساعدة."
        )

    caption = await format_welcome_text(welcome_template, user, chat_title)
    # إرسال ملف متحرك (Animation) مع التعليق
    try:
        await bot.send_animation(chat_id=chat_id, animation=WELCOME_ANIMATION_URL, caption=caption)
    except Exception:
        log.exception("Failed to send welcome animation to chat_id=%s", chat_id)
        # Fallback: إرسال نص بدون ميديا
        try:
            await bot.send_message(chat_id, caption)
        except Exception:
            log.exception("Failed to send fallback welcome message to chat_id=%s", chat_id)

# ---- State handler: استقبال نص الترحيب من المستخدم ----
@router.message(WelcomeStates.waiting_welcome)
async def process_welcome_text(message: Message, state: FSMContext):
    template = message.text.strip()
    try:
        ok = await db.set_welcome(message.chat.id, template)
        if ok:
            await message.answer("✅ تم حفظ نص الترحيب بنجاح.")
        else:
            await message.answer("⚠️ تعذّر حفظ نص الترحيب. تأكد من إعداد قاعدة البيانات ثم حاول مرة أخرى.")
    except Exception:
        await message.answer("⚠️ حدث خطأ أثناء حفظ نص الترحيب. حاول لاحقاً.")
        log.exception("Error saving welcome template")
    finally:
        await state.clear()

# أمثلة أوامر لاختبار المعاينة
@router.message(Command("show_welcome"))
async def cmd_show_welcome(message: Message):
    user = message.from_user
    template = await db.get_welcome(message.chat.id)
    await send_welcome(message.bot, message.chat.id, user, welcome_template=template, chat_title=message.chat.title)
