from app.middleware import app
from app.routers.authentication import authentication_router
from app.routers.user import (fetch_user_router, find_user_router,
                              store_user_router)

# Users
app.include_router(fetch_user_router.router)
app.include_router(store_user_router.router)
app.include_router(find_user_router.router)

# authentication
app.include_router(authentication_router.router)
