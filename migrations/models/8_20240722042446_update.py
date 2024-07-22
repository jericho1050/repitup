from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "password" TEXT NOT NULL;
        ALTER TABLE "user" DROP COLUMN "password_hash";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "password_hash" VARCHAR(50) NOT NULL  DEFAULT 'misc';
        ALTER TABLE "user" DROP COLUMN "password";"""
