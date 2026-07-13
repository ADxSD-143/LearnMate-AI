import asyncio


async def fetch_data():
    await asyncio.sleep(3)  # Non-blocking pause
    return "Data ready!"


async def main():
    print("Starting task...")
    # Start fetching data, but don't freeze the system
    task = asyncio.create_task(fetch_data())

    print("Moving to next task immediately...")

    data = await task
    print(data)


asyncio.run(main())