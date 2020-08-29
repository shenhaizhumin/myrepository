from application.model.ums_admin import UmsRole, UmsAdmin, UmsAdminRoleRelation, UmsPermission, \
    UmsRolePermissionRelation
from application.model import Session
from application.api.response import BaseError, CommonPage
from application.settings import error_code
from application.model.ums_menu import UmsMenu, UmsRoleMenuRelation
from application.model.ums_resource import UmsResource, UmsRoleResourceRelation
from application.service.ums_admin_cache_service import UmsAdminCacheService as admin_cache_service

'''
/**
     * 添加角色
     */
    int create(UmsRole role);

    /**
     * 修改角色信息
     */
    int update(Long id, UmsRole role);

    /**
     * 批量删除角色
     */
    int delete(List<Long> ids);

    /**
     * 获取指定角色权限
     */
    List<UmsPermission> getPermissionList(Long roleId);

    /**
     * 修改指定角色的权限
     */
    @Transactional
    int updatePermission(Long roleId, List<Long> permissionIds);

    /**
     * 获取所有角色列表
     */
    List<UmsRole> list();

    /**
     * 分页获取角色列表
     */
    List<UmsRole> list(String keyword, Integer pageSize, Integer pageNum);

    /**
     * 根据管理员ID获取对应菜单
     */
    List<UmsMenu> getMenuList(Long adminId);

    /**
     * 获取角色相关菜单
     */
    List<UmsMenu> listMenu(Long roleId);

    /**
     * 获取角色相关资源
     */
    List<UmsResource> listResource(Long roleId);

    /**
     * 给角色分配菜单
     */
    @Transactional
    int allocMenu(Long roleId, List<Long> menuIds);

    /**
     * 给角色分配资源
     */
    @Transactional
    int allocResource(Long roleId, List<Long> resourceIds);
'''


class UmsRoleService(object):
    @classmethod
    async def create(cls, db: Session, schema):
        # 添加角色
        role = UmsRole(**schema.dict())
        db.add(role)
        db.commit()

    @classmethod
    async def update(cls, db: Session, role_id, schema_update):
        # 修改角色信息
        update_args = {k: v for k, v in schema_update.dict().items() if v}
        rows = db.query(UmsRole).filter_by(id=role_id).update(update_args)
        return rows

    @classmethod
    async def delete(cls, db: Session, role_ids):
        # 批量删除角色
        count = db.query(UmsRole).filter(UmsRole.id.in_(role_ids)).delete(synchronize_session=False)
        db.commit()
        admin_cache_service.del_resource_list_by_role_ids(role_ids)
        return count

    @classmethod
    async def get_permission_list(cls, db: Session, role_id):
        # 获取指定角色权限
        return db.query(UmsPermission).join(UmsRolePermissionRelation, UmsRolePermissionRelation.role_id == role_id) \
            .filter(UmsRolePermissionRelation.permission_id == UmsPermission.id).all()

    @classmethod
    async def update_permission(cls, db: Session, role_id, permission_ids):
        # 修改指定角色的权限
        # 开启事务
        db.begin(subtransactions=True)
        # 首先删除角色原有关联的权限
        db.query(UmsRolePermissionRelation).filter(UmsRolePermissionRelation.role_id == role_id).delete()
        # 批量插入新关系
        relation_list = [UmsRolePermissionRelation(role_id=role_id, permission_id=p_id) for p_id in permission_ids]
        db.add_all(relation_list)
        db.commit()
        return

    @classmethod
    async def list(cls, db: Session):
        # 获取所有角色列表
        return db.query(UmsRole).all()

    @classmethod
    async def list_by_keyword(cls, db: Session, keyword: str, page_size: int, page_num: int):
        # 根据角色名称分页获取角色列表
        query_set = db.query(UmsRole)
        if keyword:
            query_set = query_set.filter(UmsRole.name.like('%{}%'.format(keyword)))
        query_set = query_set.offset((page_num - 1) * page_size).limit(page_size)
        total = query_set.scalar()
        roles = query_set.all()
        total_page = query_set.count()
        return CommonPage(page_size=page_size, page_num=page_num, total=total, list=roles, total_page=total_page)

    @classmethod
    async def get_menu_list(cls, db: Session, admin_id: int):
        # menus = []
        # 根据管理员ID获取对应菜单
        # relation = db.query(UmsAdminRoleRelation).filter_by(admin_id=admin_id).first()
        # if not relation:
        #     # 根据角色id 获取menu ids
        #     menu_ids = db.query(UmsRoleMenuRelation).filter_by(role_id=relation.role_id).all()
        menus = db.query(UmsMenu) \
            .join(UmsAdminRoleRelation, UmsAdminRoleRelation.admin_id == admin_id) \
            .join(UmsRoleMenuRelation, UmsRoleMenuRelation.role_id == UmsRoleMenuRelation.role_id) \
            .filter(UmsMenu.id == UmsRoleMenuRelation.menu_id).all()
        return menus

    @classmethod
    async def list_menu(cls, db: Session, role_id):
        # 获取角色相关菜单
        return db.query(UmsMenu).join(UmsRoleMenuRelation, UmsRoleMenuRelation.role_id == role_id).filter(
            UmsRoleMenuRelation.menu_id == UmsMenu.id).all()

    @classmethod
    async def list_resource(cls, db: Session, role_id):
        # 获取角色相关资源
        return db.query(UmsResource).join(UmsRoleResourceRelation, UmsRoleResourceRelation.role_id == role_id).filter(
            UmsRoleResourceRelation.resource_id == UmsResource.id).all()

    @classmethod
    async def alloc_menu(cls, db: Session, role_id, menu_ids):
        # 给角色分配菜单
        db.begin(subtransactions=True)
        # 先删除原有关系
        db.query(UmsRoleMenuRelation).filter_by(role_id=role_id).delete(synchronize_session=False)
        # 批量插入新关系
        role_menu_relation_list = [UmsRoleMenuRelation(role_id=role_id, menu_id=menu_id) for menu_id in menu_ids]
        db.add_all(role_menu_relation_list)
        db.commit()
        return len(role_menu_relation_list)

    @classmethod
    async def alloc_resource(cls, db: Session, role_id, resource_ids):
        # 给角色分配资源
        db.begin(subtransactions=True)
        # 先删除原有关系
        db.query(UmsRoleResourceRelation).filter_by(role_id=role_id).delete(synchronize_session=False)
        # 批量插入新关系
        role_resource_relation_list = [UmsRoleResourceRelation(role_id=role_id, resource_id=resource_id) for resource_id
                                       in resource_ids]
        db.add_all(role_resource_relation_list)
        db.commit()
        admin_cache_service.del_resource_list_by_role(role_id)
        return len(role_resource_relation_list)
