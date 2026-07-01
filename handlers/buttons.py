from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("add_button"))
async def cmd_add_button(message: Message):
    await message.answer("➕ لإضافة زر: أرسل في رسالة واحدة بالشكل:\n<نص الزر>|<url أو action>\nمثال: زر تبرع|https://example.com")

@router.message(Command("list_buttons"))
async def cmd_list_buttons(message: Message):
    # جلب من DB في حالتك الفعلية
    await message.answer("📋 قائمة الأزرار:\n(لا توجد أزرار محفوظة حتى الآن.)")

@router.message(Command("del_button"))
async def cmd_del_button(message: Message):
    await message.answer("❌ لحذف زر: أرسل اسم الزر أو معرّفه.")
