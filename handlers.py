from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from api import get_colors, get_sizes, get_order_number, get_order_status

PRODUCT_ID, COLOR, SIZE, ADDRESS, ORDER_ID, CONTACTS = range(6)


async def ask_for_product_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)

    await update.message.reply_text("Напишите номер товара.", reply_markup=reply_markup)
    return PRODUCT_ID


async def ask_for_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    product_id = update.message.text
    context.user_data['product_id'] = product_id

    data = get_colors(product_id)

    if not data:
        await update.message.reply_text(f"Неправильный номер! Напишите правильный номер товара.")
        return PRODUCT_ID

    color_keyboard = [[InlineKeyboardButton(color, callback_data=f'color_{color.lower()}') for color in data['colors']]]

    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    color_keyboard.append([cancel_button])

    reply_markup = InlineKeyboardMarkup(color_keyboard)

    await update.message.reply_text(f"Цена товара {data['price']} KZT. \nВыберите цвет товара :",
                                    reply_markup=reply_markup)
    return COLOR


async def ask_for_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    color = query.data.split('_')[-1]
    context.user_data['color'] = color

    data = get_sizes(product_id=context.user_data['product_id'], color=color)

    if not data:
        await update.callback_query.message.reply_text(
            f"На данный момент товар № {context.user_data['product_id']} нет в наличии")
        return ConversationHandler.END

    size_keyboard = []
    for size in data['sizes']:
        size_keyboard.append([InlineKeyboardButton(size, callback_data=f'size_{size.upper()}')])

    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    size_keyboard.append([cancel_button])

    reply_markup = InlineKeyboardMarkup(size_keyboard)

    await update.callback_query.message.reply_text(
        f"Выберите размер товара:", reply_markup=reply_markup)
    return SIZE


async def ask_for_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    size = query.data.split('_')[-1]
    context.user_data['size'] = size

    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)

    await update.callback_query.message.reply_text("Напишите адрес доставки. \nМожете отправить ссылку на 2GIS",
                                                   reply_markup=reply_markup)
    return ADDRESS


async def ask_for_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['address'] = update.message.text

    cancel_button = InlineKeyboardButton("Отмена", callback_data='cancel_order')
    cancel_keyboard = [
        [cancel_button]
    ]
    reply_markup = InlineKeyboardMarkup(cancel_keyboard)

    await update.message.reply_text("Напишите ваш номер телефона.",
                                    reply_markup=reply_markup)
    return CONTACTS


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['contacts'] = update.message.text

    product_id = context.user_data['product_id']
    color = context.user_data['color']
    size = context.user_data['size']
    address = context.user_data['address']
    contacts = context.user_data['contacts']

    order_number = get_order_number(product_id, color, size, address, contacts)

    if not order_number:
        await update.message.reply_text(
            f"Продукт № {product_id} на данный момент нет в наличии. Обратитесь чуть позже")
        return ConversationHandler.END

    await update.message.reply_text(
        f"Ваш заказ создан. \nПродукт № {product_id}, размер: {size}, цвет: {color},\nадрес доставки: {address} \nНапишите номер заказа сообщением в переводе\nНомер заказа: {order_number} \nНомер для перевода денег: +7 777 247 53 70, Абзал С.\nСвязаться с менеджером можно \nпо телефону +7 777 147 85 23.")
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
    order_id = context.user_data['order_id']

    data = get_order_status(order_id)

    if not data:
        await update.message.reply_text(
            f"Неправильный номер заказа!")
        return ConversationHandler.END

    await update.message.reply_text(data)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message or update.callback_query.message
    if message:
        await message.reply_text("Операция отменена.")
    return ConversationHandler.END
