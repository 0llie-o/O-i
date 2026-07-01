from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.states import ButtonStates, ChannelStates, BroadcastStates
import db

router = Router()

# إضافة زر - المعالجة عبر FSM
@router.message(ButtonStates.waiting_add_button)
async def process_add_button(message: Message, state: FSMContext):
    text = message.text.strip()
    if "|" not in text:
        await message.answer("تنسيق غير صحيح. استخدم: <نص الزر>|<url أو action>")
        return
    btn_text, btn_url = [p.strip() for p in text.split("|", 1)]
    btn_id = await db.add_button(message.chat.id, btn_text, btn_url)
    await message.answer(f"✅ تم إضافة الزر بنجاح. id: {btn_id}")
    await state.clear()

@router.message(ButtonStates.waiting_del_button)
async def process_del_button(message: Message, state: FSMContext):
    text = message.text.strip()
    # حاول كـ id أولاً
    if text.isdigit():
        await db.delete_button_by_id(message.chat.id, int(text))
        await message.answer(f"✅ تم حذف الزر بالمعرّف {text} إن وُجد.")
    else:
        await db.delete_button_by_text(message.chat.id, text)
        await message.answer(f"✅ تم حذف أي زر يطابق "{text}" إن وُجد.")
    await state.clear()

@router.message(Command("list_buttons"))
async def cmd_list_buttons(message: Message):
    buttons = await db.list_buttons(message.chat.id)
    if not buttons:
        await message.answer("📋 لا توجد أزرار محفوظة حتى الآن.")
        return
    text = "📋 قائمة الأزرار:\n"
    for b in buttons:
        text += f"- id: {b['id']} | {b['text']} → {b['url']}\n"
    await message.answer(text)

# --- قنوات ---
@router.message(ChannelStates.waiting_add_channel)
async def process_add_channel(message: Message, state: FSMContext):
    channel = message.text.strip()
    await db.add_channel(message.chat.id, channel)
    await message.answer(f"✅ تم إضافة القناة: {channel}")
    await state.clear()

@router.message(ChannelStates.waiting_del_channel)
async def process_del_channel(message: Message, state: FSMContext):
    channel = message.text.strip()
    await db.delete_channel_by_text(message.chat.id, channel)
    await message.answer(f"✅ تم إزالة القناة: {channel} إن وُجدت.")
    await state.clear()

@router.message(Command("list_channels"))
async def cmd_list_channels(message: Message):
    channels = await db.list_channels(message.chat.id)
    if not channels:
        await message.answer("🗂️ لا توجد قنوات مرتبطة هذه المحادثة.")
        return
    text = "🗂️ القنوات المرتبطة:\n"
    for c in channels:
        text += f"- id: {c['id']} | {c['channel']}\n"
    await message.answer(text)

# --- إذاعة ---
@router.message(BroadcastStates.waiting_broadcast)
async def process_broadcast(message: Message, state: FSMContext):
    # الحصول على كل القنوات المميزة من DB
    targets = await db.list_all_channels()
    if not targets:
        await message.answer("⚠️ لا توجد قنوات مرتبطة للبث.")
        await state.clear()
        return

    sent = 0
    for tgt in targets:
        try:
            # إذا كانت الرسالة عبارة عن ميديا، انسخها إلى القناة
            if message.animation:
                await message.bot.send_animation(tgt, animation=message.animation.file_id, caption=message.caption or None)
            elif message.text:
                await message.bot.send_message(tgt, message.text)
            else:
                # نسخة احتياطية: إرسال النص إذا موجود
                await message.bot.send_message(tgt, message.text or "")
            sent += 1
        except Exception:
            # تجاهل الأخطاء لضمان اكتمال المحاولة
            continue

    await message.answer(f"✅ انتهى البث. تم الإرسال إلى {sent} قناة/مجلد.")
    await state.clear()
