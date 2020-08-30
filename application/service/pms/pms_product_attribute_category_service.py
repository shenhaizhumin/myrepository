from application.model.pms_product_attribute_category import PmsProductAttributeCategory, PmsProductAttribute


class PmsProductAttributeCategoryService(object):
    @classmethod
    def create(cls, db, name):
        category = PmsProductAttributeCategory(name=name)
        db.add(category)
        db.commit()
        return category

    @classmethod
    def update(cls, db, category_id, name):
        rows = db.query(PmsProductAttributeCategory).filter_by(id=category_id).update(dict(name=name))
        db.commit()
        return rows

    @classmethod
    def delete(cls, db, category_id):
        rows = db.query(PmsProductAttributeCategory).filter_by(id=category_id).delete(synchronize_session=False)
        db.commit()
        return rows

    @classmethod
    def get_item(cls, db, category_id):
        return db.query(PmsProductAttributeCategory).filter_by(id=category_id).first()

    @classmethod
    def get_list(cls, db, page_num, page_size):
        query_set = db.query(PmsProductAttributeCategory).offset((page_num - 1) * page_size) \
            .limmit(page_size)
        return dict(pageNum=page_num, pageSize=page_size, total=query_set.count(),
                    list=query_set.all())

    @classmethod
    def get_list_with_attr(cls, db):
        from sqlalchemy import text
        # return db.execute(
        #     'select pac.*,pa.* from pms_product_attribute_category pac '
        #     'left join pms_product_attribute pa on pa.product_attribute_category_id=pac.id and pa.type=1;').fetchall()
        # return db.query(PmsProductAttributeCategory).all()
        # return db.execute(
        #     text(
        #         #    """
        #         # select pac.*,pa.* from pms_product_attribute_category pac left join pms_product_attribute pa on
        #         # pac.id=pa.product_attribute_category_id;
        #         #    """
        #         """
        #         SELECT pac.id,pac.name,pa.id as attr_id,pa.name as attr_name FROM pms_product_attribute_category pac
        #         join pms_product_attribute pa on pa.product_attribute_category_id=pac.id and pa.type=1;
        #         """
        #     )
        # ).fetchall()
        # return db.query(PmsProductAttributeCategory,PmsProductAttribute).outerjoin(PmsProductAttribute,
        #                                                   PmsProductAttribute.product_attribute_category_id == PmsProductAttributeCategory.id).all()
        return db.query(PmsProductAttributeCategory).all()
