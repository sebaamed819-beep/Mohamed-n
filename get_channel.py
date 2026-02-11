"""
هذا السكربت لمعرفة ID القنوات
يشتغل على جهازك المحلي فقط
"""
from pyrogram import Client
import asyncio


async def main():
    API_ID = int(input("➜ أدخل API_ID: "))
    API_HASH = input("➜ أدخل API_HASH: ")
    SESSION = input("➜ أدخل Session String: ")

    async with Client(
        "get_id",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION
    ) as app:
        print("\n✅ تم الاتصال بنجاح!\n")

        while True:
            username = input("➜ أدخل يوزر القناة (بدون @) أو 'exit' للخروج: ")
            if username.lower() == "exit":
                break
            try:
                chat = await app.get_chat(username)
                print(f"  📌 اسم القناة: {chat.title}")
                print(f"  🆔 الـ ID: {chat.id}")
                print()
            except Exception as e:
                print(f"  ❌ خطأ: {e}\n")


asyncio.run(main())
