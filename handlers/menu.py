from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from keyboards.main import get_main_menu
from config import BOT_NAME
from handlers.states import WelcomeStates, ButtonStates, ChannelStates, BroadcastStates
import db
import logging

log = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    رسالة البداية تعرض لوحة التحكم باللغة العربية.
    """
    text = (
        f"أهلاً وسهلاً بك في بوت {BOT_NAME}!\n\n"
        "هذه لوحة التحكم لإدارة رسالة الترحيب، الأزرار، والقنوات. "
        "استخدم الأزرار أدناه لتنفيذ الإجراءات المطلوبة."
    )
    await message.answer(text, reply_markup=get_main_menu())

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("القائمة الرئيسية:", reply_markup=get_main_menu())


# ---- التعامل مع نقرات الأزرار (callback_data) ----
@router.callback_query(Text("set_welcome"))
async def cb_set_welcome(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer(
        "⚙️ تهيئة وضع ضبط الترحيب:\n\n"
        "أرسل الآن نص الترحيب الجديد. يمكنك استخدام الرموز:\n"
        " - {name} → اسم المستخدم\n"
        " - {chat} → اسم أو معرف المجموعة/المحادثة\n\n"
        " بعد الإرسال سيتم حفظ النص كمحتوى الترحيب الافتراضي."
    )
    await state.set_state(WelcomeStates.waiting_welcome)

@router.callback_query(Text("show_welcome"))
async def cb_show_welcome(query: CallbackQuery):
    await query.answer()
    try:
        template = await db.get_welcome(query.message.chat.id)
        if not template:
            await query.message.answer("لا يوجد نص ترحيب محفوظ. يمكنك ضبط واحد عبر: ⚙️ ضبط الترحيب.")
            return
        from handlers.welcome import send_welcome
        user = query.from_user
        await query.message.answer("جارٍ عرض معاينة الترحيب...")
        await send_welcome(query.message.bot, query.message.chat.id, user, welcome_template=template, chat_title=query.message.chat.title)
    except Exception:
        await query.message.answer("⚠️ حدث خطأ أثناء جلب معاينة الترحيب. يرجى المحاولة لاحقاً.")
        log.exception("Error in show_welcome callback")

@router.callback_query(Text("del_welcome"))
async def cb_del_welcome(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer(
        "🗑️ هل تريد فعلاً حذف رسالة الترحيب الافتراضية؟\n"
        "أرسل الآن: نعم للحذف أو إلغاء/لا للإلغاء."
    )
    await state.set_state(WelcomeStates.waiting_welcome)

@router.callback_query(Text("add_button"))
async def cb_add_button(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer(
        "➕ لإضافة زر جديد: أرسل البيانات بالشكل التالي:\n"
        "<text>|<url_or_action>\n\n"
        "مثال: زر جديد|https://example.com"
    )
    await state.set_state(ButtonStates.waiting_add_button)

@router.callback_query(Text("del_button"))
async def cb_del_button(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("❌ لحذف زر: أرسل رقم المعرف (id) أ�� نص الزر لحذفه.")
    await state.set_state(ButtonStates.waiting_del_button)

@router.callback_query(Text("list_buttons"))
async def cb_list_buttons(query: CallbackQuery):
    await query.answer()
    try:
        buttons = await db.list_buttons(query.message.chat.id)
        if not buttons:
            await query.message.answer("📋 لا توجد أزرار محفوظة حالياً.")
            return
        text = "📋 قائمة الأزرار:\n"
        for b in buttons:
            text += f"- id: {b['id']} | {b['text']} → {b['url']}\n"
        await query.message.answer(text)
    except Exception:
        await query.message.answer("⚠️ حدث خطأ أثناء جلب قائمة الأزرار.")
        log.exception("Error in list_buttons callback")

@router.callback_query(Text("add_channel"))
async def cb_add_channel(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("📢 لإضافة قناة: أرسل معرف القناة أو الرابط.\nمثال: @mychannel")
    await state.set_state(ChannelStates.waiting_add_channel)

@router.callback_query(Text("del_channel"))
async def cb_del_channel(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("➖ لإزالة قناة: أرسل معرف القناة المراد إزالتها من القائمة.")
    await state.set_state(ChannelStates.waiting_del_channel)

@router.callback_query(Text("list_channels"))
async def cb_list_channels(query: CallbackQuery):
    await query.answer()
    try:
        channels = await db.list_channels(query.message.chat.id)
        if not channels:
            await query.message.answer("🗂️ لا توجد قنوات مرتبطة بهذه المحادثة.")
            return
        text = "🗂️ القنوات المرتبطة:\n"
        for c in channels:
            text += f"- id: {c['id']} | {c['channel']}\n"
        await query.message.answer(text)
    except Exception:
        await query.message.answer("⚠️ حدث خطأ أثناء جلب قائمة القنوات.")
        log.exception("Error in list_channels callback")

@router.callback_query(Text("broadcast"))
async def cb_broadcast(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer(
        "📣 إذاعة جماعية: أرسل الآن نص/ميديا الرسالة التي تريد إرسالها إلى جميع القنوات/المجموعات المرتبطة.\n\n"
        "ملاحظة: سيتم تنفيذ البث بعد إرسال الرسالة هنا وسيتم إرساله إلى جميع القنوات المسجلة."
    )
    await state.set_state(BroadcastStates.waiting_broadcast)

@router.callback_query(Text("stats"))
async def cb_stats(query: CallbackQuery):
    await query.answer()
    try:
        stats = await db.get_stats()
        await query.message.answer(
            f"📊 الإحصائيات:\n- عدد القنوات: {stats['channels']}\n- عدد الأزرار: {stats['buttons']}\n- عدد الترحيبات المحفوظة: {stats['welcomes']}"
        )
    except Exception:
        await query.message.answer("⚠️ حدث خطأ أثناء جلب الإحصائيات.")
        log.exception("Error in stats callback")
