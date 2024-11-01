from fastapi import APIRouter, Depends

from app.api.schemas.user import UserFromDB, UserCreate
from app.services.user_service import UserService
from app.utils.unitofwork import UnitOfWork, IUnitOfWork


user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)


@user_router.post("/", response_model=UserFromDB)
async def create_todo(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    print(user_data)
    return await user_service.add_user(user_data)


@user_router.get("/", response_model=list[UserFromDB])
async def get_todos(todo_service: UserService = Depends(get_user_service)):
    return await todo_service.get_users()
