from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers import *
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    order_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('order', ask_for_product_id)],
        states={
            PRODUCT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_color)],
            COLOR: [CallbackQueryHandler(ask_for_size, pattern='^color_.*')],
            SIZE: [CallbackQueryHandler(ask_for_address, pattern='^size_.*')],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_contacts)],
            CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)]
        }, fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel_order$')], allow_reentry=True
    )

    check_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('check', ask_for_order_id)],
        states={
            ORDER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_order_status)]
        }, fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel_check$')], allow_reentry=True
    )

    application.add_handler(order_conv_handler)
    application.add_handler(check_conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
