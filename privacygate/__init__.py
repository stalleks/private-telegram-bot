from aiogram import Router

from . import admin, authorizer, notifier

router = Router()
router.include_routers(admin.router, authorizer.router)