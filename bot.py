import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
OPENAI_API_KEY = "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"
TELEGRAM_TOKEN = "7433106210:AAF_ar95J7BljMS3lLy9MGfu9mzSJGebHxw"
BOT_USERNAME = "@DeliveryHelpTest_Bot"

# Initialization OpenAI
openai.api_key = OPENAI_API_KEY

# Food Delivery Knowledge Base
delivery_knowledge_base = {
    "вартість доставки": "Наша вартість доставки складає 49 грн. При замовленні від 300 грн доставка безкоштовна.",
    "години роботи": "Ми працюємо щодня з 09:00 до 23:00. Кур'єри доставляють замовлення у цей же час.",
    "оплата": "Ви можете оплатити замовлення готівкою кур'єру або карткою онлайн.",
    "термін доставки": "Середній час доставки - 45 хвилин. У години пік (12:00-14:00, 18:00-20:00) може бути до 60 хвилин.",
    "зона доставки": "Доставляємо по всьому місту. Точні межі можете перевірити на нашому сайті.",
    "повернення": "Якщо ви хочете повернути товар, будь ласка, зв'яжіться з нами протягом 24 годин після отримання.",
    "акції": "Зараз діє акція - кожне 5-те замовлення зі знижкою 20%. Також є програма лояльності.",
    "меню": "Наше меню включає піцу, суші, бургери, салати та напої. Повний перелік на нашому сайті.",
    "алергени": "Інформацію про алергени в стравах можна отримати у описі страви або уточнити у оператора.",
    "вегетаріанські": "У нас є спеціальний розділ вегетаріанських страв, позначений зеленим значком."
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привіт! Я чат-бот служби доставки їжі. Задайте мені своє питання!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    
    # Database Lookup Attempt
    response = None
    for keyword, answer in delivery_knowledge_base.items():
        if keyword in user_message:
            response = answer
            break
    
    # If no match is found locally - query OpenAI
    if not response:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ти чат-бот служби доставки їжі. Відповідай коротко та по суті."},
                    {"role": "user", "content": user_message}
                ]
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = "Наразі виникли технічні труднощі. Будь ласка, спробуйте пізніше."
    
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler('start', start_command))
    
    # Message Processing
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Bot Activation
    print('Бот працює...')
    app.run_polling(poll_interval=3)
