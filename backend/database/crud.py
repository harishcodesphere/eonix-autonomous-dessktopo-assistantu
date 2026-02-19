"""
Eonix CRUD Operations
Database operations for interactions and workflows.
"""
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Interaction, Workflow
from loguru import logger


class InteractionCRUD:
    """CRUD operations for interaction history."""

    @staticmethod
    async def create(session: AsyncSession, user_input: str, ai_response: str, intent: str = None, metadata: dict = None) -> Interaction:
        interaction = Interaction(
            user_input=user_input,
            ai_response=ai_response,
            intent=intent,
            metadata_json=metadata,
            timestamp=datetime.utcnow(),
        )
        session.add(interaction)
        await session.commit()
        await session.refresh(interaction)
        logger.debug(f"Saved interaction #{interaction.id}")
        return interaction

    @staticmethod
    async def get_recent(session: AsyncSession, limit: int = 20) -> list[Interaction]:
        result = await session.execute(
            select(Interaction).order_by(Interaction.timestamp.desc()).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_intent(session: AsyncSession, intent: str, limit: int = 10) -> list[Interaction]:
        result = await session.execute(
            select(Interaction).where(Interaction.intent == intent).order_by(Interaction.timestamp.desc()).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def count(session: AsyncSession) -> int:
        result = await session.execute(select(Interaction))
        return len(result.scalars().all())


class WorkflowCRUD:
    """CRUD operations for automation workflows."""

    @staticmethod
    async def create(session: AsyncSession, name: str, definition: dict, description: str = "") -> Workflow:
        wf = Workflow(name=name, definition=definition, description=description)
        session.add(wf)
        await session.commit()
        await session.refresh(wf)
        logger.debug(f"Saved workflow: {name}")
        return wf

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Workflow]:
        result = await session.execute(select(Workflow))
        return result.scalars().all()

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str) -> Workflow | None:
        result = await session.execute(select(Workflow).where(Workflow.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_by_name(session: AsyncSession, name: str) -> bool:
        result = await session.execute(delete(Workflow).where(Workflow.name == name))
        await session.commit()
        return result.rowcount > 0
