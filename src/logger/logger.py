from prisma import Prisma
from datetime import datetime
from pytz import timezone

class LoggingService:
    def __init__(self, db: Prisma):
        self.db = db

    # Adding new log
    async def log_message(self, service_id, user_id, log_level, message):
        """
        Create a log entry in the database with timezone-aware timestamp.
        """
        istanbul_tz = timezone("Europe/Istanbul")
        current_time = datetime.now(istanbul_tz)

        await self.db.log.create({
            'service_id': service_id,
            'user_id': user_id,
            'log_level': log_level,  # "INFO", "ERROR", "WARNING", "CRITICAL", "DEBUG"
            'message': message,
            'log_timestamp': current_time
        })

    # Adding new service
    async def add_service(self, is_active, service_name):
        """
        Register a new service in the system.
        """
        await self.db.services.create({
            'is_active': is_active,
            'service_name': service_name
        })
