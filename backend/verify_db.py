import asyncio
from sqlalchemy import select
from database import sessionlocal
from anomaly.models.anomaly import Anomaly

async def check():
    async with sessionlocal() as db:
        stmt = select(Anomaly).where(Anomaly.description == "Test anomaly alert description")
        result = await db.execute(stmt)
        anomalies = result.scalars().all()
        if anomalies:
            print(f"Success! Found {len(anomalies)} anomalies in DB.")
            for a in anomalies:
                print(f"ID: {a.id}, Type: {a.anomaly_type.value}, Camera: {a.camera_id}")
        else:
            print("No anomalies found in DB.")

if __name__ == "__main__":
    asyncio.run(check())
