from app.api.schemas.user import UserCreate, UserFromDB
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserCreate) -> UserFromDB:
        user_dict: dict = user.model_dump()  # подготовка данных для внесения в БД
        async with self.uow:  # вход в контекст (если выбьет с ошибкой, то изменения откатятся)
            user_from_db = await self.uow.user.add_one(user_dict)

            user_to_return: UserFromDB = UserFromDB.model_validate(user_from_db)  # обработка полученных данных из БД для их возврата - делаем модель пидантик
            await self.uow.commit()  # это самый важный кусок кода, до этого коммита можно записать данные в 50 моделей, но если кто-то вылетит с ошибкой, все изменения откатятся! Если код дошёл сюда, то все прошло окей!
            return user_to_return

    async def get_users(self) -> list[UserFromDB]:
        async with self.uow:
            users: list = await self.uow.user.find_all()
            return [UserFromDB.model_validate(user) for user in users]