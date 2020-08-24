from application.model.ums_menu import UmsMenu, UmsRoleMenuRelation
from application.model.ums_admin import UmsAdmin, UmsRole
from datetime import datetime


class UmsMenuService(object):
    async def create_menu(self, db, schema):
        # schema.create_time = datetime.now()
        self.update_level(db, schema)
        db.add(UmsMenu(**schema))
        return db.commit()

    def update_level(self, db, schema):
        '''
            修改菜单层级
        '''
        # 没有父菜单时为一级菜单
        if schema.parent_id == 0:
            schema.level = 0
        else:
            parent_menu = db.query(UmsMenu).filter_by(parent_id=UmsMenu.parent_id).first()
            if parent_menu:
                # 存在父级菜单
                schema.level = parent_menu.level + 1
            else:
                schema.level = 0

    async def update_menu(self, db, menu_id, schema_update):
        self.update_level(db, schema_update)
        ums_menu = db.query(UmsMenu).filter_by(id=menu_id).first()
        for key in schema_update.__dict__:
            setattr(ums_menu, key, getattr(schema_update, key))
        return db.commit()
