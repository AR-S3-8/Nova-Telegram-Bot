import logging
from typing import Dict
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

TOKEN = ""

# alaki baraye forget pass
VALID_EMAIL = "alaki@gmail.com"
VALID_OTP = "123456"

#alaki baraye deact
VALID_EMAIL_DACT = "alaki@gmail.com"
VALID_PASSWORD_DACT = "123456"

# logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# halat haye form voroodi karbar baraye forget pass
(
    STATE_NAME,
    STATE_EMAIL,
    STATE_OTP,
    STATE_CONFIRM_ALL,
) = range(4)

# state haye deact
STATE_CONFIRM_START_DACT = 10
STATE_EMAIL_DACT = 11
STATE_PASSWORD_DACT = 12
STATE_CONFIRM_ALL_DACT = 13

# kilid ha va dokme ha
def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("مشاهده امکانات ⚙️", callback_data="menu_features")],
        [InlineKeyboardButton("حمایت مالی 💸" , callback_data="menu_donate")]
    ]
    return InlineKeyboardMarkup(keyboard)

def features_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("فراموشی رمز عبور 🔐", callback_data="menu_forget")],
        [InlineKeyboardButton("حذف حساب کاربری ❌", callback_data="menu_deactivate")],
        [InlineKeyboardButton("پروژه در یک نگاه 🧩", callback_data="menu_site")],
        [InlineKeyboardButton("ثبت بازخورد یا گزارش مشکل 📝", callback_data="menu_feedback")],
        [InlineKeyboardButton("درباره ما ℹ️", callback_data="menu_about")],
        [InlineKeyboardButton("🔙", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def about_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("هدف از ایجاد نوا 🎯", callback_data="about_goal")],
        [InlineKeyboardButton("تیم نوا 👥", callback_data="about_team")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def about_team_keyboard(members) -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(name, callback_data=f"team_member_{i}")]
          for i, name in enumerate(members, start=1)]

    kb.append([InlineKeyboardButton("درباره ما ℹ️", callback_data="back_to_about")])

    kb.append([InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")])
    return InlineKeyboardMarkup(kb)

def forget_start_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("ادامه فراموشی رمز 🔐", callback_data="start_reset")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_email_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله ✅", callback_data="confirm_email_yes"),
         InlineKeyboardButton("مرحله قبل 🔁", callback_data="back_to_email")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def confirm_otp_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله ✅", callback_data="confirm_otp_yes"),
         InlineKeyboardButton("مرحله قبل 🔁", callback_data="back_to_otp")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def confirm_all_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("درسته ✅", callback_data="confirm_all_yes"),
         InlineKeyboardButton("نادرست ❌ (دوباره وارد کن)", callback_data="confirm_all_no")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def deactive_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله، مطمئنم 🗑️", callback_data="dact_start_yes"),
         InlineKeyboardButton("خیر، منصرف شدم ❌", callback_data="dact_start_no")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def confirm_email_keyboard_dact() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله ✅", callback_data="dact_confirm_email_yes"),
         InlineKeyboardButton("مرحله قبل 🔁", callback_data="dact_back_to_start")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def confirm_password_keyboard_dact() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله ✅", callback_data="dact_confirm_password_yes"),
         InlineKeyboardButton("مرحله قبل 🔁", callback_data="dact_back_to_pass")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

def confirm_all_keyboard_dact() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله، حذف کن 🗑️", callback_data="dact_confirm_all_yes"),
         InlineKeyboardButton("خیر ❌", callback_data="dact_confirm_all_no")],
        [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
    ])

TEAM_MEMBERS = [
    "پرهام عزیزی",
    "علی زندی",
    "میثم محسنی نیکوگفتار",
    "علیرضا رسولیان",
    "محدثه جوان",
    "فاطمه رضایی توانا",
]

# Helper baraye hazf dade ha baade back to main va bastane conversation
def reset_conversation(context: ContextTypes.DEFAULT_TYPE):
    keys = [
        # forget flow
        'reset_name', 'reset_email', 'reset_otp',
        # deactivate flow
        'reset_email_dact', 'reset_password_dact',
        # generic flags
        'awaiting_feedback'
    ]
    for k in keys:
        context.user_data.pop(k, None)
    return ConversationHandler.END

# Handelers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start handler"""
    if update.message:
        user = update.effective_user
        text = f"سلام {user.first_name or 'کاربر'} 🌟\nبه ربات نوا خوش آمدید!"
        await update.message.reply_text(text, reply_markup=main_menu_keyboard())

# Global handler baraye back to main menu az harja
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        text = "به منوی اصلی بازگشتید.\nچه کاری می‌خواهید انجام دهید؟"
        # edit the message where the button was pressed
        try:
            await query.edit_message_text(text=text, reply_markup=main_menu_keyboard())
        except Exception:
            # fallback: send a new message
            await query.message.reply_text(text, reply_markup=main_menu_keyboard())
    else:
        # if a plain message triggered it (unlikely), send main menu
        await context.bot.send_message(chat_id=update.effective_chat.id, text="منوی اصلی:", reply_markup=main_menu_keyboard())
    # End any active conversation state for this user + clear user-scoped data
    reset_conversation(context)
    return ConversationHandler.END

async def menu_donate_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "این بخش درحال راه اندازی است ⏳ \n\n لطفا بعدا اقدام نمایید."
    try:
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))
    except Exception:
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))


# vaghti bezani امکانات
async def menu_features_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text(text="لطفا یکی از موارد زیر را انتخاب نمایید :", reply_markup=features_keyboard())
    except Exception:
        await query.message.reply_text("لطفا یکی از موارد زیر را انتخاب نمایید :", reply_markup=features_keyboard())

# About
async def menu_about_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(text="درباره کدام بخش از 'نوا' نیاز به اطلاعات دارید ؟", reply_markup=about_keyboard())
    except Exception:
        await query.message.reply_text("درباره کدام بخش از 'نوا' نیاز به اطلاعات دارید ؟", reply_markup=about_keyboard())

async def about_goal_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "هدف از ایجاد نوا:\n\n"
        "وب اپلیکیشن نوا در ابتدا با تنها یک پروژه دانشگاهی بود."
        "اما به مرور با مشارکت اعضای تیم این پروژه تبدیل به بستری ویژه با امکانات و ویژگی هایی نوین در انتقال پیام میان مخاطبین شد"
    )
    try:
        await query.edit_message_text(text=text, reply_markup=about_keyboard())
    except Exception:
        await query.message.reply_text(text, reply_markup=about_keyboard())

async def about_team_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # list team ro namayesh mide
    try:
        await query.edit_message_text(text="💎 اعضای تیم نوا :", reply_markup=about_team_keyboard(TEAM_MEMBERS))
    except Exception:
        await query.message.reply_text("💎 اعضای تیم نوا :", reply_markup=about_team_keyboard(TEAM_MEMBERS))

async def team_member_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    try:
        idx = int(data.split("_")[-1]) - 1
        name = TEAM_MEMBERS[idx]
    except Exception:
        name = "عضو ناشناخته"

    emails = {
        "علیرضا رسولیان": "alireza.rasoulian.s3@gmail.com",
        "محدثه جوان": "Mrs.mohadeseh.javan@gmail.com",
        "پرهام عزیزی": "aziziparham2020@gmail.com",
        "میثم محسنی نیکوگفتار": "meysammohseny0011@gmail.com",
        "علی زندی": "ali.zandi2020pc@gmail.com",
        "فاطمه رضایی توانا": "fatavana06@gmail.com",
    }
    email = emails.get(name, "example@example.com")
    
    github = {
        "علیرضا رسولیان": "https://github.com/AR-S3-8",
        "محدثه جوان": "https://github.com/pluto10010",
        "پرهام عزیزی": "https://github.com/BlackProgrammer-prog",
        "میثم محسنی نیکوگفتار": "https://github.com/meysam-nikoogoftar",
        "علی زندی": "https://github.com/programmer-black2",
        "فاطمه رضایی توانا": "https://github.com/Fatavana",
    }
    github = github.get(name ,"https://github.com/example")

    info = f"""اطلاعات {name}:

    - Role: Developer
    - Gmail: {email}
    - GitHub: {github}

    """

    try:
        await query.edit_message_text(text=info, reply_markup=about_team_keyboard(TEAM_MEMBERS))
    except Exception:
        await query.message.reply_text(info, reply_markup=about_team_keyboard(TEAM_MEMBERS))

# FORGET (start)
async def menu_forget_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text(text="برای فراموشی رمز عبور یکی از گزینه‌ها را انتخاب کنید:", reply_markup=forget_start_keyboard())
    except Exception:
        await query.message.reply_text("برای فراموشی رمز عبور یکی از گزینه‌ها را انتخاب کنید:", reply_markup=forget_start_keyboard())

async def start_reset_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # paksazi mavared ghabli agar boode
    reset_conversation(context)

    try:
        await query.edit_message_text(text="لطفاً «نام و نام خانوادگی» خود را وارد کنید.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
    except Exception:
        await query.message.reply_text("لطفاً «نام و نام خانوادگی» خود را وارد کنید.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
    return STATE_NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    context.user_data['reset_name'] = text
    await update.message.reply_text("نام دریافت شد ✅\nلطفاً آدرس ایمیل (Gmail) خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
    return STATE_EMAIL

async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    context.user_data['reset_email'] = email
    
    await update.message.reply_text(f"ایمیل وارد شده: {email}\nآیا ایمیل را صحیح وارد کرده‌اید؟", reply_markup=confirm_email_keyboard())
    return STATE_EMAIL

async def confirm_email_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_email_yes":
        
        try:
            await query.edit_message_text(text="لطفاً کد یکبار مصرف (OTP) ارسال شده به ایمیل را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text("لطفاً کد یکبار مصرف (OTP) ارسال شده به ایمیل را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_OTP
    elif query.data == "back_to_email":
        
        try:
            await query.edit_message_text(text="لطفاً مجدداً ایمیل خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text("لطفاً مجدداً ایمیل خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_EMAIL
    else:
        return STATE_EMAIL

async def receive_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = update.message.text.strip()
    context.user_data['reset_otp'] = otp

    await update.message.reply_text(f"کد وارد شده: {otp}\nآیا کد را درست وارد کردید؟", reply_markup=confirm_otp_keyboard())
    return STATE_OTP

async def confirm_otp_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_otp_yes":
        # kholase vooroodi ha
        name = context.user_data.get('reset_name', "<نام وارد نشده>")
        email = context.user_data.get('reset_email', "<ایمیل وارد نشده>")
        otp = context.user_data.get('reset_otp', "<کد وارد نشده>")
        summary = f"خلاصه اطلاعات:\n\nنام: {name}\nایمیل: {email}\nکد OTP: {otp}\n\nآیا این اطلاعات صحیح است؟"
        try:
            await query.edit_message_text(text=summary, reply_markup=confirm_all_keyboard())
        except Exception:
            await query.message.reply_text(summary, reply_markup=confirm_all_keyboard())
        return STATE_CONFIRM_ALL
    elif query.data == "back_to_otp":

        try:
            await query.edit_message_text(text="لطفاً مجدداً کد یکبار مصرف (OTP) را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text("لطفاً مجدداً کد یکبار مصرف (OTP) را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_OTP
    else:
        return STATE_OTP

async def confirm_all_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_all_yes":
        # baresi vooroodi haye karbar ba maghadir pishfarz
        email = context.user_data.get('reset_email', "")
        otp = context.user_data.get('reset_otp', "")
        if email == VALID_EMAIL and otp == VALID_OTP:
            
            try:
                await query.edit_message_text("اطلاعات وارد شده صحیح است ✅\nلطفاً برای تغییر رمز جدید بعداً اقدام کنید.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
            except Exception:
                await query.message.reply_text("اطلاعات وارد شده صحیح است ✅", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
            # end conversation + clear forget-data
            reset_conversation(context)
            return ConversationHandler.END
        else:

            try:
                await query.edit_message_text("اطلاعات نادرست است ❌\nلطفا مجدداً بعدا اقدام نمایید.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("بازگشت به منوی امکانات ⚙️", callback_data="back_to_features")]
                ]))
            except Exception:
                await query.message.reply_text("اطلاعات نادرست است ❌\nلطفا مجدداً بعدا اقدام نمایید.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("بازگشت به منوی امکانات ⚙️", callback_data="back_to_features")]
                ]))
            # end conversation + clear forget-data
            reset_conversation(context)
            return ConversationHandler.END
    elif query.data == "confirm_all_no":
        # shoroe mojadad ba gereftan esm va ...
        try:
            await query.edit_message_text(" لطفاً مجدداً نام و نام خانوادگی را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text("لطفاً مجدداً نام و نام خانوادگی را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_NAME
    else:
        # ensure cleanup on unexpected path
        reset_conversation(context)
        return ConversationHandler.END

async def back_to_name_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text(text="لطفاً نام و نام خانوادگی خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
    except Exception:
        await query.message.reply_text("لطفاً نام و نام خانوادگی خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
    return STATE_NAME

# Deactive
async def menu_deactivate_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Clear any previous flow data on entering deactivate flow
    reset_conversation(context)

    try:
        await query.edit_message_text(
            text="آیا از حذف حساب کاربری خود مطمئن هستید ؟ \n این عمل غیرقابل بازگشت است!",
            reply_markup=deactive_start_keyboard()
        )
    except Exception:
        await query.message.reply_text(
            "آیا از حذف حساب کاربری خود مطمئن هستید ؟ \n این عمل غیرقابل بازگشت است!",
            reply_markup=deactive_start_keyboard()
        )
    return STATE_CONFIRM_START_DACT

async def deact_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "dact_start_yes":
        # Ask for email (note: we use a different context key reset_email_dact)
        try:
            await query.edit_message_text(
                text="لطفاً ایمیل (Gmail) حساب خود را وارد کنید:",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]])
            )
        except Exception:
            await query.message.reply_text(
                "لطفاً ایمیل (Gmail) حساب خود را وارد کنید:",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]])
            )
        return STATE_EMAIL_DACT
    else:
        try:
            await query.edit_message_text("عملیات حذف حساب لغو شد.", reply_markup=main_menu_keyboard())
        except Exception:
            await query.message.reply_text("عملیات حذف حساب لغو شد.", reply_markup=main_menu_keyboard())
        return ConversationHandler.END

async def receive_email_dact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    context.user_data['reset_email_dact'] = email
    await update.message.reply_text(f"ایمیل وارد شده: {email}\nآیا این ایمیل صحیح است؟", reply_markup=confirm_email_keyboard_dact())
    return STATE_EMAIL_DACT

async def confirm_email_cb_dact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "dact_confirm_email_yes":

        try:
            await query.edit_message_text(text="لطفاً رمز عبور حساب کاربری خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text("لطفاً رمز عبور حساب کاربری خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_PASSWORD_DACT
    elif query.data == "dact_back_to_start":

        try:
            await query.edit_message_text(
                text="آیا از حذف حساب کاربری خود مطمئن هستید ؟ \n این عمل غیرقابل بازگشت است!",
                reply_markup=deactive_start_keyboard()
            )
        except Exception:
            await query.message.reply_text(
                "آیا از حذف حساب کاربری خود مطمئن هستید ؟ \n این عمل غیرقابل بازگشت است!",
                reply_markup=deactive_start_keyboard()
            )
        return STATE_CONFIRM_START_DACT
    else:
        return STATE_EMAIL_DACT

async def receive_password_dact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    context.user_data['reset_password_dact'] = password
    await update.message.reply_text(
        f"رمز وارد شده: {password}\nآیا این رمز صحیح است؟",
        reply_markup=confirm_password_keyboard_dact()
    )
    return STATE_PASSWORD_DACT

async def confirm_password_cb_dact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "dact_confirm_password_yes":
        # kholase vooroodi haye karbar
        email = context.user_data.get('reset_email_dact', "<ایمیل وارد نشده>")
        password = context.user_data.get('reset_password_dact', "<رمز وارد نشده>")
        summary = f"خلاصه اطلاعات:\n\nایمیل: {email}\nرمز: {password}\n\nآیا مایل به حذف دائم حساب خود هستید؟"
        try:
            await query.edit_message_text(text=summary, reply_markup=confirm_all_keyboard_dact())
        except Exception:
            await query.message.reply_text(summary, reply_markup=confirm_all_keyboard_dact())
        return STATE_CONFIRM_ALL_DACT

    elif query.data == "dact_back_to_pass":
        
        try:
            await query.edit_message_text(text="لطفاً رمز عبور خود را دوباره وارد کنید:", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
            ]))
        except Exception:
            await query.message.reply_text(text="لطفاً رمز عبور خود را دوباره وارد کنید:", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
            ]))
        return STATE_PASSWORD_DACT

    elif query.data == "dact_back_to_email":
        
        try:
            await query.edit_message_text(text="لطفاً مجدداً ایمیل خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        except Exception:
            await query.message.reply_text(text="لطفاً مجدداً ایمیل خود را وارد کنید:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
        return STATE_EMAIL_DACT
    else:
        return STATE_PASSWORD_DACT

async def confirm_all_cb_dact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "dact_confirm_all_yes":
        # baresi voroodi haye karbar ba mavared pishfarz
        email = context.user_data.get('reset_email_dact', "")
        password = context.user_data.get('reset_password_dact', "")
        if email == VALID_EMAIL_DACT and password == VALID_PASSWORD_DACT:

            try:
                await query.edit_message_text("حساب شما با موفقیت حذف شد ✅\nاز همراهی شما ممنونیم.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
            except Exception:
                await query.message.reply_text("حساب شما با موفقیت حذف شد ✅\nاز همراهی شما ممنونیم.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]]))
            # clear deact-related context keys + end conversation
            reset_conversation(context)
            return ConversationHandler.END
        else:
            # failure
            try:
                await query.edit_message_text("اطلاعات وارد شده صحیح نیست ❌\n لطفا مجدداً بعدا اقدام نمایدد.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("بازگشت به منوی امکانات ⚙️", callback_data="back_to_features")]
                ]))
            except Exception:
                await query.message.reply_text("اطلاعات وارد شده صحیح نیست ❌\n لطفا مجدداً بعدا اقدام نمایدد.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("بازگشت به منوی امکانات ⚙️", callback_data="back_to_features")]
                ]))
            # clear deact context + end conversation
            reset_conversation(context)
            return ConversationHandler.END
    elif query.data == "dact_confirm_all_no":

        try:
            await query.edit_message_text("عملیات حذف حساب لغو شد.\n به منوی اصلی بازگشتید.", reply_markup=main_menu_keyboard())
        except Exception:
            await query.message.reply_text("عملیات حذف حساب لغو شد.\n به منوی اصلی بازگشتید.", reply_markup=main_menu_keyboard())
        # clear any temp data + end conversation
        reset_conversation(context)
        return ConversationHandler.END
    else:
        # unexpected path: end and clear
        reset_conversation(context)
        return ConversationHandler.END
    

async def back_to_features_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_text(
            text="لطفاً یکی از موارد زیر را انتخاب نمایید :",
            reply_markup=features_keyboard()
        )
    except Exception:
        await query.message.reply_text(
            text="لطفاً یکی از موارد زیر را انتخاب نمایید :",
            reply_markup=features_keyboard()
        )
    # when bridging back to features, end any conversation and clear flow data
    reset_conversation(context)
    return ConversationHandler.END

async def menu_feedback_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["awaiting_feedback"] = True
    chat_id=update.effective_chat.id,
    text = "لطفاً بازخورد یا مشکل خود را به صورت یک پیام متنی ارسال کنید 📝"
    
    try:
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))
    except Exception:
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))

async def receive_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_feedback"):
        context.user_data["awaiting_feedback"] = False
        feedback = update.message.text.strip()
        user = update.effective_user

        await update.message.reply_text(
            "بازخورد شما ثبت شد ✅\nممنون از همراهی شما 🙏🏻",
            reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
            ])
        )

        channel_id = "-1003020981632"
        feedback_text = (
            f"📩 بازخورد جدید:\n\n"
            f"{feedback}\n\n"
            f"ارسال‌کننده: {user.full_name}\n"
            f"آیدی عددی: {user.id}\n"
            f"نام کاربری: @{user.username if user.username else 'ندارد'}"
        )
        await context.bot.send_message(chat_id=channel_id, text=feedback_text)

async def menu_site_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "تمام امکانات و قابلیت های پیامرسان در یک نگاه ⚡\n\n🌐 https://aboutproject-7287c.web.app/"
    try:
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))
    except Exception:
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main")]
        ]))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("عملیات لغو شد. بازگشت به منوی اصلی.", reply_markup=main_menu_keyboard())
    # ensure any flow data is cleared on cancel
    reset_conversation(context)
    return ConversationHandler.END  
    
# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CallbackQueryHandler(back_to_main, pattern="^back_to_main$"))

    # Register handlers for top-level menu navigation
    app.add_handler(CallbackQueryHandler(menu_features_cb, pattern="^menu_features$"))
    app.add_handler(CallbackQueryHandler(menu_about_cb, pattern="^menu_about$"))
    app.add_handler(CallbackQueryHandler(menu_forget_cb, pattern="^menu_forget$"))
    app.add_handler(CallbackQueryHandler(about_goal_cb, pattern="^about_goal$"))
    app.add_handler(CallbackQueryHandler(about_team_cb, pattern="^about_team$"))
    app.add_handler(CallbackQueryHandler(team_member_cb, pattern="^team_member_"))
    app.add_handler(CallbackQueryHandler(menu_about_cb, pattern="^back_to_about$"))
    app.add_handler(CallbackQueryHandler(forget_start_keyboard, pattern="^forget_start$"))

    # Unified ConversationHandler for both forget and deactivate flows
    conv_all = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_reset_cb, pattern="^start_reset$"),
            CallbackQueryHandler(menu_deactivate_cb, pattern="^menu_deactivate$"),
        ],
        states={
            # Forget flow
            STATE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email),
                CallbackQueryHandler(confirm_email_cb, pattern="^(confirm_email_yes|back_to_email)$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_OTP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_otp),
                CallbackQueryHandler(confirm_otp_cb, pattern="^(confirm_otp_yes|back_to_otp)$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_CONFIRM_ALL: [
                CallbackQueryHandler(confirm_all_cb, pattern="^(confirm_all_yes|confirm_all_no)$"),
                CallbackQueryHandler(back_to_name_cb, pattern="^back_to_name$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            # Deactivate flow
            STATE_CONFIRM_START_DACT: [
                CallbackQueryHandler(deact_start_cb, pattern="^(dact_start_yes|dact_start_no)$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_EMAIL_DACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email_dact),
                CallbackQueryHandler(confirm_email_cb_dact, pattern="^(dact_confirm_email_yes|dact_back_to_start)$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_PASSWORD_DACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password_dact),
                CallbackQueryHandler(confirm_password_cb_dact, pattern="^(dact_confirm_password_yes|dact_back_to_pass|dact_back_to_email)$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
            STATE_CONFIRM_ALL_DACT: [
                CallbackQueryHandler(confirm_all_cb_dact, pattern="^(dact_confirm_all_yes|dact_confirm_all_no)$"),
                CallbackQueryHandler(deact_start_cb, pattern="^dact_back_to_start$"),
                CallbackQueryHandler(back_to_main, pattern="^back_to_main$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_all)

    # vaghti karbar start ro mizane
    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(CallbackQueryHandler(menu_features_cb, pattern="^menu_features$"))

    app.add_handler(CallbackQueryHandler(menu_donate_cb, pattern="^menu_donate$"))

    app.add_handler(CallbackQueryHandler(start_reset_cb, pattern="^start_reset$"))

    app.add_handler(CallbackQueryHandler(menu_site_cb, pattern="^menu_site$"))

    app.add_handler(CallbackQueryHandler(menu_feedback_cb, pattern="^menu_feedback$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_feedback))

    #baraye vaghti ke bridge zadim be bakhsh emkanat
    app.add_handler(CallbackQueryHandler(back_to_features_cb, pattern="^back_to_features$"))


    # Start the bot
    logger.info("Starting bot...")
    app.run_polling()

if __name__ == "__main__":
    main()