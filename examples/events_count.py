import asyncio
from collections import defaultdict

from judobase import JudoBase


async def main():
    async with JudoBase() as api:
        contests = await api.contests_by_competition_id(
            competition_id=2869,
            weight="-60",
            include_events=True,  # Include contest events in the response
        )

        throw_stats = defaultdict(lambda: {"total": 0})
        for contest in contests:
            for event in contest.events:
                for tag in event.tags:
                    name, group = tag.name, tag.group_name

                    throw_stats[name]["total"] += 1
                    throw_stats[name].setdefault(group, 0)
                    throw_stats[name][group] += 1

                    if name in {"Right", "Left"} and event.tags:
                        throw_name = event.tags[0].name
                        throw_stats[throw_name].setdefault(name, 0)
                        throw_stats[throw_name][name] += 1

        print(throw_stats["Seoi-nage"]["total"])  # Output: 5
        print(throw_stats["Seoi-nage"]["Right"])  # Output: 3
        print(
            sorted(throw_stats.items(), key=lambda x: x[1]["total"], reverse=True)[12]
        )  # Output: ('Juji-gatame', {'total': 2, 'Ippon': 2, 'Left': 2})


asyncio.run(main())
