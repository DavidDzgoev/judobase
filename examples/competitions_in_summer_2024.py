import asyncio
from datetime import datetime, timezone

from judobase import Competition, JudoBase


async def main():
    async with JudoBase() as api:
        competitions: list[Competition] = await api.competitions_in_range(
            datetime(2024, 6, 1, tzinfo=timezone.utc),
            datetime(2024, 8, 31, tzinfo=timezone.utc),
        )
        print(len(competitions))  # Output: 14


asyncio.run(main())
