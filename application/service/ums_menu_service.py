from application.model.ums_menu import UmsMenu, UmsMenuNode
from application.model.ums_admin import UmsAdmin, UmsRole
from datetime import datetime
from application.api.response import BaseError


class UmsMenuService(object):
    async def create_menu(self, db, schema):
        # schema.create_time = datetime.now()
        self.update_level(db, schema)
        db.add(UmsMenu(**schema.dict()))
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
        # ums_menu = db.query(UmsMenu).filter_by(id=menu_id).first()
        # if not ums_menu:
        #     raise BaseError(msg='未找到指定菜单')
        # for key in schema_update.__dict__:
        #     value = getattr(schema_update, key)
        #     if value or value == 0:
        #         setattr(ums_menu, key, value)
        update_args = {k: v for k, v in schema_update.dict().items() if v}
        rows = db.query(UmsMenu).filter_by(id=menu_id).update(update_args)
        db.commit()
        return rows

    async def delete_menu(self, db, menu_id):
        count = db.query(UmsMenu).filter_by(id=menu_id).delete(synchronize_session=False)
        db.commit()
        return count

    async def get_menu_by_id(self, db, menu_id):
        return db.query(UmsMenu).filter_by(id=menu_id).first()

    async def menu_list(self, db, parent_id, page_num, page_size):
        return db.query(UmsMenu).filter_by(parent_id=parent_id).order_by(UmsMenu.sort.desc()).offset(
            page_num - 1).limit(page_size).all()

    async def update_hidden(self, db, menu_id, hidden):
        count = db.query(UmsMenu).filter_by(id=menu_id).update({UmsMenu.hidden: hidden}, synchronize_session=False)
        # ums_menu.hidden = hidden
        db.commit()
        return count

    async def tree_list(self, db):
        menus = db.query(UmsMenu).all()
        # UmsMenuNode(**)
        # 获取到根结点 转换成node
        result = [self.convert_menu_node(parent_menu, menus) for parent_menu in menus if parent_menu.parent_id == 0]
        return result

    def convert_menu_node(self, ums_parent_menu, menu_list) -> UmsMenuNode:
        ums_parent_menu.__dict__.pop('_sa_instance_state')
        ums_parent_menu_node = UmsMenuNode(**ums_parent_menu.__dict__)
        children = []
        for menu in menu_list:
            # filter
            if menu.parent_id == ums_parent_menu.id:
                # map
                node = self.convert_menu_node(menu, menu_list)
                children.append(node)
        ums_parent_menu_node.children = children
        return ums_parent_menu_node
