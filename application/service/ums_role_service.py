from application.model.ums_admin import UmsRole, UmsAdmin, UmsAdminRoleRelation
from application.model import Session
from application.api.response import BaseError
from application.settings import error_code
from application.model.ums_menu import UmsMenu, UmsRoleMenuRelation

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
    async def create(cls, db: Session):
        # 添加角色
        pass

    @classmethod
    async def update(cls, db: Session):
        # 修改角色信息
        pass

    @classmethod
    async def delete(cls, db: Session):
        # 批量删除角色
        pass

    @classmethod
    async def get_permission_list(cls, db: Session):
        # 获取指定角色权限
        pass

    @classmethod
    async def update_permission(cls, db: Session):
        # 修改指定角色的权限
        pass

    @classmethod
    async def list(cls, db: Session):
        # 获取所有角色列表
        pass

    @classmethod
    async def list(cls, db: Session, keyword: str, page_size: int, page_num: int):
        # 分页获取角色列表
        pass

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
    async def list_menu(cls, db: Session):
        # 获取角色相关菜单
        pass

    @classmethod
    async def list_resource(cls, db: Session):
        # 获取角色相关资源
        pass

    @classmethod
    async def alloc_menu(cls, db: Session):
        # 给角色分配菜单
        pass

    @classmethod
    async def alloc_resource(cls, db: Session):
        # 给角色分配资源
        pass
