from .config import db, init_db
from .models.user import User
from .models.course import Course

__all__ = ['db', 'init_db', 'Course', 'User']