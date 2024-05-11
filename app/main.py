from fastapi import FastAPI

from .Routers.UsersRouter.FetchUserRouter import router as fetch_user_router
from .Routers.UsersRouter.StoreUserRouter import router as store_user_router
from .Routers.UsersRouter.FindUserRouter import router as find_user_router

app = FastAPI()

# Users
app.include_router(fetch_user_router)
app.include_router(store_user_router)
app.include_router(find_user_router)
