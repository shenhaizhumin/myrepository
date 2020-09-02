from application.model.pms_product_attribute_category import PmsProductAttribute, PmsProductAttributeCategory


class PmsProductAttributeService(object):


    @classmethod
    def get_list(cls,db,):

    @classmethod
    def create(cls, db, schema):
        # 新建商品属性
        db.add(PmsProductAttribute(**schema.dict()))
        # 新增商品属性后 需要修改商品属性分类数量
        if schema.type == 0:
            # 0->规格
            db.query(PmsProductAttributeCategory).filter(
                PmsProductAttributeCategory.id == schema.product_attribute_category_id).update(
                {PmsProductAttributeCategory.attribute_count: PmsProductAttributeCategory.attribute_count + 1})
        elif schema.type == 1:
            db.query(PmsProductAttributeCategory).filter(
                PmsProductAttributeCategory.id == schema.product_attribute_category_id).update(
                {PmsProductAttributeCategory.param_count: PmsProductAttributeCategory.param_count + 1})
        db.commit()

    @classmethod
    def update(cls, db, attr_id, schema_update):
        # 修改商品属性
        # update_args = {k: v for k, v in schema_update.dict().items() if v or v == 0}
        # rows = db.query(PmsProductAttribute).filter(PmsProductAttribute.id == attr_id).update(update_args)
        db.begin(subtransactions=True)
        product_attribute = db.query(PmsProductAttribute).filter(PmsProductAttribute.id == attr_id).first()
        # 修改商品属性
        for k, v in schema_update.dict().items():
            if v or v == 0:
                setattr(product_attribute, k, v)
        if schema_update.type or schema_update.type == 0:
            # 满足条件更新 商品属性的分类
            if product_attribute.type != schema_update.type:
                product_attribute_category = db.query(PmsProductAttributeCategory).filter_by(
                    product_attribute_category_id=product_attribute.product_attribute_category_id).first()
                if schema_update.type == 0:
                    product_attribute_category.attribute_count = product_attribute_category.attribute_count - 1
                    product_attribute_category.param_count = product_attribute_category.param_count + 1
                elif schema_update.type == 1:
                    product_attribute_category.attribute_count = product_attribute_category.attribute_count + 1
                    product_attribute_category.param_count = product_attribute_category.param_count - 1
        db.commit()
        return True
