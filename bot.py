"""
هذا السكربت يشتغل على جهازك المحلي فقط
لتوليد Session String لحسابك على تيليغرام
"""
from pyrogram import Client
import asyncio


async def main():
    print("=" * 50)
    print("  مولّد Session String")
    print("=" * 50)

    API_ID = int(input("\n➜ أدخل API_ID: "))
    API_HASH = input("➜ أدخل API_HASH: ")

    # سيطلب منك رقم هاتفك ثم كود التحقق
    async with Client("session_gen", api_id=API_ID, api_hash=API_HASH) as app:
        session_string = await app.export_session_string()
        print("\n" + "=" * 50)
        print("✅ تم التوليد بنجاح!")
        print("=" * 50)
        print(f"\nSession String:\n")
        print(session_string)
        print("\n⚠️  احفظ هذا النص في مكان آمن!")
        print("⚠️  لا تشاركه مع أي شخص!")
        print("=" * 50)


asyncio.run(main())
