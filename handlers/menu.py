from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from keyboards.main import get_main_menu
from config import BOT_NAME

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
async def cb_set_welcome(query: CallbackQuery):
    await query.answer()
    # هنا يمكن تفعيل حالة FSM لتلقي نص الترحيب التالي وحفظه في DB
    await query.message.answer(
        "⚙️ تهيئة وضع ضبط الترحيب:\n\n"
        "أرسل الآن نص الترحيب الجديد. يمكنك استخدام الرموز:\n"
        " - {name} → اسم المستخدم\n"
        " - {chat} → اسم أو معرف المجموعة/المحادثة\n\n"
        " بعد الإرسال سيتم حفظ النص كمحتوى الترحيب الافتراضي."
    )

@router.callback_query(Text("show_welcome"))
async def cb_show_welcome(query: CallbackQuery):
    await query.answer()
    # استدعاء معاينة الترحيب — يُفضّل جلب نص الترحيب من DB إن وُجد
    # سنرسِل معاينة افتراضية إذا لم يوجد نص مخزن.
    await query.message.answer("جارٍ عرض معاينة الترحيب...")

@router.callback_query(Text("del_welcome"))
async def cb_del_welcome(query: CallbackQuery):
    await query.answer()
    # تنفيذ حذف نص الترحيب من DB — هنا رسالة تأكيد
    await query.message.answer(
        "🗑️ هل تريد فعلاً حذف رسالة الترحيب الافتراضية؟\n"
        "أرسل: /confirm_del_welcome للحذف أو /cancel للإلغاء."
    )

@router.callback_query(Text("add_button"))
async def cb_add_button(query: CallbackQuery):
    await query.answer()
    await query.message.answer(
        "➕ لإضافة زر جديد: أرسل البيانات بالشكل التالي:\n"
        "<text>|<url_or_action>\n\n"
        "مثال: زر جديد|https://example.com\n\n"
        "أو: زر داخلي|action_name (وسيتم معالجته حسب منطق البوت)."
    )

@router.callback_query(Text("del_button"))
async def cb_del_button(query: CallbackQuery):
    await query.answer()
    await query.message.answer("❌ لحذف زر: أرسل اسم الزر أو المعرف المرتبط به (اعتماداً على طريقة الحفظ).")

@router.callback_query(Text("list_buttons"))
async def cb_list_buttons(query: CallbackQuery):
    await query.answer()
    # جلب قائمة الأزرار من DB وعرضها — إن لم توجد أزرار نفّذ الرسالة التالية:
    await query.message.answer("📋 عرض قائمة الأزرار المرتبطة بهذه الدردشة:\n\n(لا توجد أزرار حالياً.)")

@router.callback_query(Text("add_channel"))
async def cb_add_channel(query: CallbackQuery):
    await query.answer()
    await query.message.answer("📢 لإضافة قناة: أرسل معرف القناة أو الرابط.\nمثال: @mychannel")

@router.callback_query(Text("del_channel"))
async def cb_del_channel(query: CallbackQuery):
    await query.answer()
    await query.message.answer("➖ لإزالة قناة: أرسل معرف القناة المراد إزالتها من القائمة.")

@router.callback_query(Text("list_channels"))
async def cb_list_channels(query: CallbackQuery):
    await query.answer()
    await query.message.answer("🗂️ القنوات المرتبطة بهذه المحادثة:\n\n(لا توجد قنوات مرتبطة حالياً.)")

@router.callback_query(Text("broadcast"))
async def cb_broadcast(query: CallbackQuery):
    await query.answer()
    await query.message.answer(
        "📣 إذاعة جماعية: أرسل الآن نص/ميديا الرسالة التي تريد إرسالها إلى جميع القنوات/المجموعات المرتبطة.\n\n"
        "ملاحظة: سيتم تنفيذ البث بعد تأكيدك."
    )

@router.callback_query(Text("stats"))
async def cb_stats(query: CallbackQuery):
    await query.answer()
    # مثال عرض إحصائيات مبسطة
    await query.message.answer("📊 الإحصائيات:\n- عدد القنوات المرتبطة: 0\n- عدد الأزرار: 0\n(إحصائيات افتراضية — عدّل لعرض بيانات فعلية من DB).")
