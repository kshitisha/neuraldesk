import asyncio
from app.db.base import engine, Base
from app.db.models import User, Project, Prompt, Conversation, Message, ProjectFile


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully.")


if __name__ == "__main__":
    asyncio.run(create_tables())