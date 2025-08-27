import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# Bot token from Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Referral storage (simple dictionary for demo)
referrals = {}
user_invites = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    args = message.text.split()
    user_id = message.from_user.id

    if user_id not in referrals:
        referrals[user_id] = None
        user_invites[user_id] = 0

    if len(args) > 1:
        ref_id = int(args[1].replace("ref_", ""))
        if ref_id != user_id and referrals[user_id] is None:
            referrals[user_id] = ref_id
            user_invites[ref_id] = user_invites.get(ref_id, 0) + 1
            await message.answer(f"✅ Aap {ref_id} ke referral se aaye ho!")

    link = f"https://t.me/{(await bot.me()).username}?start=ref_{user_id}"
    await message.answer(f"👋 Welcome {message.from_user.first_name}!\n"
                         f"Yeh aapka referral link hai:\n{link}")

@dp.message(Command("invites"))
async def cmd_invites(message: Message):
    user_id = message.from_user.id
    invites = user_invites.get(user_id, 0)
    await message.answer(f"👥 Aapne {invites} log invite kiye hain.")

@dp.message(Command("referral"))
async def cmd_referral(message: Message):
    user_id = message.from_user.id
    ref = referrals.get(user_id)
    if ref:
        await message.answer(f"🌟 Aap {ref} ke referral se aaye ho.")
    else:
        await message.answer("❌ Aapne koi referral link use nahi kiya.")

@dp.message(Command("top"))
async def cmd_top(message: Message):
    if not user_invites:
        await message.answer("Leaderboard khali hai.")
        return

    top_users = sorted(user_invites.items(), key=lambda x: x[1], reverse=True)[:10]
    text = "🏆 Top Inviters:\n"
    for uid, count in top_users:
        text += f"- {uid}: {count} invites\n"
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())