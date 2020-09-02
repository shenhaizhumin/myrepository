from application.model.ums_resource import UmsResource
from application.api.response import BaseError


class UmsResourceService(object):
    async def create_resource(self, db, schema):
        db.add(UmsResource(**schema.dict()))
        db.commit()

    async def update_resource(self, db, resource_id, schema_update):
        update_args = {k: v for k, v in schema_update.dict().items() if v or v == 0}
        rows = db.query(UmsResource).filter_by(id=resource_id).update(update_args)
        return rows

    async def get_resource_by_id(self, db, resource_id):
        return db.query(UmsResource).filter_by(id=resource_id).first()

    async def delete_resource(self, db, resource_id):
        count = db.query(UmsResource).filter_by(id=resource_id).delete(synchronize_session=False)
        db.commit()
        return count

    async def list_all(self, db):
        return db.query(UmsResource).all()

    # 分页模糊查询
    async def list_query(self, db, category_id, name_keyword, url_keyword, page_num, page_size):
        query_set = db.query(UmsResource).filter(UmsResource.category_id == category_id)
        if name_keyword:
            query_set = query_set.filter(UmsResource.name.like('%{}%'.format(name_keyword)))
        if url_keyword:
            query_set = query_set.filter(UmsResource.url.like('%{}%'.format(url_keyword)))
        result = query_set.offset((page_num - 1) * page_size).limit(page_size).all()
        return result
