from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from api import get_colors_from_api

PRODUCT_ID, COLOR, SIZE, ADDRESS, ORDER_ID = range(5)


async def ask_for_product_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)
    await update.message.reply_text("Напишите номер товара.", reply_markup=reply_markup)
    return PRODUCT_ID


async def ask_for_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    colors = get_colors_from_api('http://localhost:5000')

    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    color_keyboard = [
        [InlineKeyboardButton("Red", callback_data='color_red')],
        [InlineKeyboardButton("Black", callback_data='color_black')],
        [InlineKeyboardButton("Blue", callback_data='color_blue')],
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(color_keyboard)
    context.user_data['product_id'] = update.message.text
    await update.message.reply_text(f"Выберите цвет товара:",
                                    reply_markup=reply_markup)
    return COLOR


async def ask_for_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    size_keyboard = [
        [InlineKeyboardButton("S", callback_data='size_s')],
        [InlineKeyboardButton("M", callback_data='size_m')],
        [InlineKeyboardButton("L", callback_data='size_l')],
        [InlineKeyboardButton("XL", callback_data='size_xl')],
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(size_keyboard)
    query = update.callback_query
    color = query.data.split('_')[-1]
    context.user_data['color'] = color
    await update.callback_query.message.reply_text(
        f"Выберите размер товара:", reply_markup=reply_markup)
    return SIZE


async def ask_for_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)
    query = update.callback_query
    size = query.data.split('_')[-1]
    context.user_data['size'] = size
    await update.callback_query.message.reply_text("Напишите адрес доставки.", reply_markup=reply_markup)
    return ADDRESS


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['address'] = update.message.text
    await update.message.reply_text(
        f"Ваш заказ создан. \nПродукт № {context.user_data['product_id']}, размер: {context.user_data['size']}, цвет: {context.user_data['color']},\nадрес доставки: {context.user_data['address']} \nНомер заказа: 789")
    return ConversationHandler.END


async def ask_for_order_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_check')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)
    await update.message.reply_text("Отправьте номер вашего заказа.", reply_markup=reply_markup)
    return ORDER_ID


async def send_order_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_id'] = update.message.text
    await update.message.reply_text(
        f"Ваш заказ № {context.user_data['order_id']} в ожидании оплаты. \nПродукт № {context.user_data['product_id']}, размер: {context.user_data['size']}, цвет: {context.user_data['color']},\nадрес доставки: {context.user_data['address']}")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message or update.callback_query.message
    if message:
        await message.reply_text("Операция отменена.")
    return ConversationHandler.END
