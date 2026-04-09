import asyncio

from geoalchemy2.elements import WKTElement
from sqlalchemy import text

from src.core.db import async_session_maker
from src.models.activities import ActivitiesORM
from src.models.buildings import BuildingsORM
from src.models.companies import CompaniesORM
from src.models.company_phones import CompanyPhonesORM


async def seed_data() -> None:
    async with async_session_maker() as session:
        await session.execute(
            text(
                "TRUNCATE TABLE company_phones, companies_activities, companies, activities, buildings RESTART IDENTITY CASCADE"
            )
        )

        food = ActivitiesORM(name="Еда", level=1)
        meat = ActivitiesORM(name="Мясная продукция", level=2, parent=food)
        milk = ActivitiesORM(name="Молочная продукция", level=2, parent=food)

        auto = ActivitiesORM(name="Автомобили", level=1)
        cargo = ActivitiesORM(name="Грузовые", level=2, parent=auto)
        passenger = ActivitiesORM(name="Легковые", level=2, parent=auto)
        parts = ActivitiesORM(name="Запчасти", level=3, parent=passenger)
        accessories = ActivitiesORM(name="Аксессуары", level=3, parent=passenger)

        session.add_all([food, meat, milk, auto, cargo, passenger, parts, accessories])

        b1 = BuildingsORM(
            address="г. Минск, ул. Ленина 1, офис 3",
            location=WKTElement("POINT(27.5615 53.9023)", srid=4326),
        )
        b2 = BuildingsORM(
            address="г. Минск, ул. Немига 5",
            location=WKTElement("POINT(27.5508 53.9045)", srid=4326),
        )
        b3 = BuildingsORM(
            address="г. Минск, пр-т Победителей 9",
            location=WKTElement("POINT(27.5395 53.9140)", srid=4326),
        )
        session.add_all([b1, b2, b3])

        c1 = CompaniesORM(name="Рога и Копыта", building=b1)
        c2 = CompaniesORM(name="Копыта и Рога", building=b1)
        c3 = CompaniesORM(name="Рогов и Ко", building=b2)
        c4 = CompaniesORM(name="Ведра с болтами", building=b2)
        c5 = CompaniesORM(name="Болты для ведер", building=b3)
        session.add_all([c1, c2, c3, c4, c5])

        session.add_all(
            [
                CompanyPhonesORM(company=c1, phone="375-29-111-11-11"),
                CompanyPhonesORM(company=c1, phone="375-29-222-22-22"),
                CompanyPhonesORM(company=c2, phone="375-29-333-33-33"),
                CompanyPhonesORM(company=c3, phone="375-29-444-44-44"),
                CompanyPhonesORM(company=c4, phone="375-29-555-55-55"),
                CompanyPhonesORM(company=c5, phone="375-29-666-66-66"),
            ]
        )

        c1.activities.extend([food, milk])
        c2.activities.append(meat)
        c3.activities.append(food)
        c4.activities.extend([auto, cargo])
        c5.activities.extend([parts, accessories])

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
