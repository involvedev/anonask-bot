from src.bot.handlers.start import router as start
from src.bot.handlers.stats import router as stats
from src.bot.handlers.admin import router as admin


routers = [
    start,
    stats,
    admin,
]