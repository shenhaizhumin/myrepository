from application.model.ums_admin import UmsPermission, UmsPermissionNode
from application.api.response import BaseError


class UmsPermissionService(object):
    async def create_permission(self, db, schema):
        count = db.add(UmsPermission(**schema.dict()))
        db.commit()
        return count

    async def update_permission(self, db, permission_id, schema_update):
        # ums_permission = db.query(UmsPermission).filter_by(id=permission_id).first()
        # if not ums_permission:
        #     raise BaseError(msg='未找到指定权限')
        # for key in schema_update.__dict__:
        #     value = getattr(schema_update, key)
        #     if value or value == 0:
        #         setattr(ums_permission, key, value)
        update_args = {k: v for k, v in schema_update.dict().items() if v}
        rows = db.query(UmsPermission).filter_by(id=permission_id).update(update_args)
        db.commit()
        return rows

    async def delete_permission(self, db, ids):
        count = db.query(UmsPermission).filter(UmsPermission.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return count

    async def permission_list(self, db):
        return db.query(UmsPermission).all()

    async def permission_tree_list(self, db):
        permission_list = db.query(UmsPermission).all()
        return [self.convert_permission_to_node(parent_permission, permission_list) for parent_permission in
                permission_list if parent_permission.pid == 0]

    def convert_permission_to_node(self, parent_permission, permission_list) -> UmsPermissionNode:
        children = []
        if '_sa_instance_state' in parent_permission.__dict__.keys():
            parent_permission.__dict__.pop('_sa_instance_state')
        node = UmsPermissionNode(**parent_permission.__dict__)
        for p in permission_list:
            if p.pid == parent_permission.id:
                children.append(self.convert_permission_to_node(p, permission_list))
        node.children = children
        return node
