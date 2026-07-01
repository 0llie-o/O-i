from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu() -> InlineKeyboardMarkup:
    """
    لوحة التحكم الرئيسية - أزرار مضمنة (InlineKeyboardMarkup).
    كل زر يرسل callback_data الذي سنعالجها في handlers.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚙️ ضبط الترحيب", callback_data="set_welcome"),
            InlineKeyboardButton(text="👁️ معاينة الترحيب", callback_data="show_welcome"),
            InlineKeyboardButton(text="🗑️ حذف الترحيب", callback_data="del_welcome"),
        ],
        [
            InlineKeyboardButton(text="➕ إضافة زر", callback_data="add_button"),
            InlineKeyboardButton(text="❌ حذف زر", callback_data="del_button"),
            InlineKeyboardButton(text="📋 قائمة الأزرار", callback_data="list_buttons"),
        ],
        [
            InlineKeyboardButton(text="📢 إضافة قناة", callback_data="add_channel"),
            InlineKeyboardButton(text="➖ إزالة قناة", callback_data="del_channel"),
            InlineKeyboardButton(text="🗂️ القنوات المرتبطة", callback_data="list_channels"),
        ],
        [
            InlineKeyboardButton(text="📣 إذاعة جماعية", callback_data="broadcast"),
            InlineKeyboardButton(text="📊 الإحصائيات", callback_data="stats"),
        ],
    ])
    return keyboard
