from sqladmin import Admin, ModelView

from libs.models import AdminUser


class AdminUserAdmin(ModelView, model=AdminUser):
    column_list = [AdminUser.id, AdminUser.email, AdminUser.is_active, AdminUser.is_superuser]
    form_columns = [AdminUser.is_active, AdminUser.is_superuser]
    column_details_exclude_list = [AdminUser.id, AdminUser.hashed_password]


def init_admin(api, engine):
    # admin = Admin(app=api, engine=engine, authentication_backend=AdminAuth("sqladmin_secret"))
    admin = Admin(app=api, engine=engine)
    admin.add_view(AdminUserAdmin)
