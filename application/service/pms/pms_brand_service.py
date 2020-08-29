from application.model.pms_brand import PmsBrand
from application.api.response import CommonPage


class PmsBrandService(object):
    @classmethod
    def list_all(cls, db):
        # 获取所有品牌信息
        return db.query(PmsBrand).all()

    @classmethod
    def create_brand(cls, db, schema):
        # 新建
        schema.first_letter = schema.name[0:1]
        pms_brand = PmsBrand(**schema.dict())
        db.add(pms_brand)
        db.commit()
        return pms_brand

    @classmethod
    def update_brand(cls, db, brand_id, schema_update):
        # 更新
        args = {k: v for k, v in schema_update.dict().items() if v}
        rows = db.query(PmsBrand).filter_by(id=brand_id).update(args)
        db.commit()
        return rows

    @classmethod
    def delete_brand(cls, db, brand_id):
        rows = db.query(PmsBrand).filter_by(id=brand_id).delete(synchronize_session=False)
        db.commit()
        return rows

    @classmethod
    def delete_brands(cls, db, ids):
        # 批量删除
        rows = db.query(PmsBrand).filter(PmsBrand.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return rows

    @classmethod
    def list_brand(cls, db, keyword, page_num, page_size):
        query_set = db.query(PmsBrand)
        if keyword:
            query_set.filter(PmsBrand.name.like(f'%{keyword}%'))
        query_set = query_set.order_by(PmsBrand.sort.desc()).offset((page_num - 1) * page_size).limit(page_size)
        page_args = dict(pageNum=page_num, pageSize=page_size, total=query_set.count(),
                         list=query_set.all())
        return page_args

    @classmethod
    def get_brand(cls, db, brand_id):
        return db.query(PmsBrand).filter_by(id=brand_id).first()

    @classmethod
    def update_show_status(cls, db, show_status, ids):
        # 批量更新品牌显示隐藏
        rows = db.query(PmsBrand).filter(PmsBrand.id.in_(ids)).update({PmsBrand.show_status: show_status})
        db.commit()
        return rows

    @classmethod
    def update_factory_status(cls, db, factory_status, ids):
        # 更新 是否为品牌制造商：0->不是；1->是
        rows = db.query(PmsBrand).filter(PmsBrand.id.in_(ids)).update({PmsBrand.factory_status: factory_status})
        db.commit()
        return rows

# if __name__ == '__main__':
#     a = 'abc'
#     print(a[0:1])
