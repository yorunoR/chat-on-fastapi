from sqladmin import Admin, ModelView

from config.settings import ADMIN_SESSION_SECRET
from libs.models import AdminUser, ChatSession, User

from .auth import AdminAuth


class AdminUserAdmin(ModelView, model=AdminUser):
    column_list = [AdminUser.id, AdminUser.email, AdminUser.is_active, AdminUser.is_superuser]
    form_columns = [AdminUser.is_active, AdminUser.is_superuser]
    column_details_exclude_list = [AdminUser.id, AdminUser.hashed_password]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.uid, User.email]


class ChatSessionAdmin(ModelView, model=ChatSession):
    column_list = [ChatSession.id, ChatSession.uid, ChatSession.label]


def init_admin(api, engine):
    admin = Admin(app=api, engine=engine, authentication_backend=AdminAuth(ADMIN_SESSION_SECRET))
    admin.add_view(AdminUserAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(ChatSessionAdmin)
