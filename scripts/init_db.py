import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.models import init_db

async def main():
    print("Initializing Eonix Database...")
    try:
        await init_db()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    asyncio.run(main())
