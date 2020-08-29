from application.model.ums_resource import UmsResourceCategory
from application.api.response import BaseError


class UmsResourceCategoryService(object):

    # 查询所有后台资源分类
    async def list_all(self, db):
        return db.query(UmsResourceCategory).order_by(UmsResourceCategory.sort.desc()).all()

    # 添加后台资源分类
    async def create_category(self, db, schema):
        db.add(UmsResourceCategory(**schema.dict()))
        db.commit()

    # 修改后台资源分类
    async def update_category(self, db, category_id, schema_update):
        # ums_res_category = db.query(UmsResourceCategory).filter_by(id=category_id).first()
        # if ums_res_category:
        #     raise BaseError(msg='未找到指定分类')
        # for key in schema_update.__dict__:
        #     value = getattr(schema_update, key)
        #     if value or value == 0:
        #         setattr(ums_res_category, key, value)
        update_args = {k: v for k, v in schema_update.dict().items() if v}
        rows = db.query(UmsResourceCategory).filter_by(id=category_id).update(update_args)
        db.commit()
        return rows

    # 根据ID删除后台资源
    async def delete_category(self, db, category_id):
        count = db.query(UmsResourceCategory).filter_by(id=category_id).delete(synchronize_session=False)
        db.commit()
        return count
