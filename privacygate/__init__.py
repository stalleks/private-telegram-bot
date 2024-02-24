from aiogram import Router

from . import admin, authorizer

router = Router()
router.include_routers(admin.router, authorizer.router)