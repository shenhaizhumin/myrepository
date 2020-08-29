from application.model import Session
from application.settings import pwd_context

'''
 /**
     * 根据用户名获取后台管理员
     */
    UmsAdmin getAdminByUsername(String username);

    /**
     * 注册功能
     */
    UmsAdmin register(UmsAdminParam umsAdminParam);

    /**
     * 登录功能
     * @param username 用户名
     * @param password 密码
     * @return 生成的JWT的token
     */
    String login(String username,String password);

    /**
     * 刷新token的功能
     * @param oldToken 旧的token
     */
    String refreshToken(String oldToken);

    /**
     * 根据用户id获取用户
     */
    UmsAdmin getItem(Long id);

    /**
     * 根据用户名或昵称分页查询用户
     */
    List<UmsAdmin> list(String keyword, Integer pageSize, Integer pageNum);

    /**
     * 修改指定用户信息
     */
    int update(Long id, UmsAdmin admin);

    /**
     * 删除指定用户
     */
    int delete(Long id);

    /**
     * 修改用户角色关系
     */
    @Transactional
    int updateRole(Long adminId, List<Long> roleIds);

    /**
     * 获取用户对于角色
     */
    List<UmsRole> getRoleList(Long adminId);

    /**
     * 获取指定用户的可访问资源
     */
    List<UmsResource> getResourceList(Long adminId);

    /**
     * 修改用户的+-权限
     */
    @Transactional
    int updatePermission(Long adminId, List<Long> permissionIds);

    /**
     * 获取用户所有权限（包括角色权限和+-权限）
     */
    List<UmsPermission> getPermissionList(Long adminId);

    /**
     * 修改密码
     */
    int updatePassword(UpdateAdminPasswordParam updatePasswordParam);

    /**
     * 获取用户信息
     */
    UserDetails loadUserByUsername(String username);
'''
from application.model.ums_admin import UmsAdmin, UmsRole, UmsAdminRoleRelation, UmsAdminLoginLog, UmsPermission, \
    UmsAdminPermissionRelation, UmsRolePermissionRelation
from application.model.ums_resource import UmsResource, UmsRoleResourceRelation
from sqlalchemy import text
from application.api.response import BaseError
from application.service.ums_admin_cache_service import UmsAdminCacheService as admin_cache_service
from application.util.token_util import create_access_token
from application.settings import ACCESS_TOKEN_EXPIRE_SECONDS, jwt_options
import logging
import traceback
from datetime import timedelta, datetime
from application.util.token_util import generate_hash_password, refresh_token
import time

# admin_cache_service = UmsAdminCacheService()
# logger = logging.getLogger(__file__)
# logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class UmsAdminService(object):

    def to_dict(self, admin_data) -> dict:
        admin_column = ['id', 'username', 'password', 'icon', 'note', 'create_time', 'email', 'login_time', 'status']
        return dict(zip(admin_column, admin_data))

    async def get_admin_by_username(self, db: Session, username, is_login=None) -> UmsAdmin:
        # 根据用户名获取后台管理员
        ums_admin = admin_cache_service.get_admin(username)
        logging.info("ums_admin:{}".format(ums_admin))
        if ums_admin:
            # mills to datetime
            if is_login:
                # 修改登录时间
                logging.info('修改登录时间')
                db.execute('update ums_admin set login_time=now() where id=:id', {'id': ums_admin['id']})
                db.commit()
                ums_admin.update({'login_time': time.time() * 1000})
                admin_cache_service.set_admin(ums_admin)
            else:
                if ums_admin['create_time']:
                    create_time = datetime.fromtimestamp(ums_admin['create_time'] / 1000)
                    ums_admin.update({'create_time': create_time})
                if ums_admin['login_time']:
                    create_time = datetime.fromtimestamp(ums_admin['login_time'] / 1000)
                    ums_admin.update({'login_time': create_time})
            logging.info("来源于缓存：{}".format(ums_admin))
            return UmsAdmin(**ums_admin)
        else:
            ums_admin = db.query(UmsAdmin.id, UmsAdmin.username, UmsAdmin.password, UmsAdmin.icon, UmsAdmin.note,
                                 UmsAdmin.create_time, UmsAdmin.email, UmsAdmin.login_time, UmsAdmin.status).filter_by(
                username=username).first()
            if ums_admin:
                ums_admin = self.to_dict(ums_admin)
                # datetime to mills
                if ums_admin['create_time']:
                    create_time_mills = time.mktime(ums_admin['create_time'].timetuple()) * 1000
                    ums_admin.update({'create_time': create_time_mills})
                if ums_admin['login_time']:
                    login_time_mills = time.mktime(ums_admin['login_time'].timetuple()) * 1000
                    ums_admin.update({'login_time': login_time_mills})
                logging.info("来源于数据库：{}".format(ums_admin))
                admin_cache_service.set_admin(ums_admin)
                return UmsAdmin(**ums_admin)
            else:
                return None

    async def register(self, db: Session, schema):
        # 注册功能
        if db.query(UmsAdmin).filter_by(username=schema.username).first():
            raise BaseError(msg='用户名已存在')
        if db.query(UmsAdmin).filter_by(email=schema.email).first():
            raise BaseError(msg='邮箱已存在')
        schema.password = generate_hash_password(schema.password)
        ums_admin = UmsAdmin(**schema.dict())
        ums_admin.create_time = datetime.now()
        ums_admin.status = 1
        db.add(ums_admin)
        db.commit()
        return ums_admin

    async def get_admin_by_id(self, db: Session, user_id):
        # 根据用户id获取用户
        return db.query(UmsAdmin).filter_by(id=user_id).first()

    async def login(self, request, db: Session, username: str, password: str) -> str:
        logging.info("开始登录:{}-----------".format(username))
        token = None
        # 用户登录
        try:
            ums_admin = await self.loader_user_by_username(db=db, username=username, is_login=True)
            logging.info('loader_user_by_username----ums_admin:{}'.format(ums_admin.__dict__))
            if not ums_admin:
                raise BaseError(msg="用户不存在")
            # TODO 校验用户密码
            token = create_access_token(username=username, user_id=ums_admin.id,
                                        expires_delta=ACCESS_TOKEN_EXPIRE_SECONDS)
            logging.info("token:{}".format(token))
            # 登录日志
            await self.insert_login_log(db=db, username=username, request=request)
            return token
        except Exception as e:
            logging.error(traceback.format_exc())
            # logging.error(traceback.format_exc(e))
            logging.error("error:{}".format(e))
        return token

    async def insert_login_log(self, db: Session, username, request):
        ums_admin = await self.get_admin_by_username(db=db, username=username)
        log_args = {
            'admin_id': ums_admin.id,
            'create_time': datetime.now(),
            'ip': request.scope.get('client')[0],
            'address': '',
            'user_agent': request.headers.get("user-agent")
        }
        logging.info('登录日志:{}'.format(log_args))
        admin_login_log = UmsAdminLoginLog(**log_args)
        db.add(admin_login_log)
        db.commit()

    async def logout(self, username, user_id) -> bool:
        try:
            admin_cache_service.del_access_token(username, user_id)
            return True
        except Exception as e:
            logging.info("error:{}".format(e))
        return False

    async def refresh_token(self, token: str):
        # 刷新token的功能
        new_token = refresh_token(old_token=token)
        return new_token

    async def list(self, db: Session, page_num, page_size, keyword):
        # 根据用户名或昵称分页查询用户
        query_set = db.query(UmsAdmin)
        if keyword:
            query_set.filter(UmsAdmin.username.like('%{}%'.format(keyword)))
        return query_set.offset(
            (page_num - 1) * page_size).limit(
            page_size).all()

    async def update(self, db: Session, user_id, user_info) -> bool:
        # 修改指定用户信息
        user = db.query(UmsAdmin).filter_by(id=user_id).first()
        if not user:
            raise BaseError(msg='修改的用户不存在！')
        update_args = {k: v for k, v in user_info.dict() if v}
        if 'password' in update_args.keys():
            update_args.update({'password': generate_hash_password(update_args['password'])})
        rows = db.query(UmsAdmin).filter_by(id=user_id).update(update_args)
        if rows:
            admin_cache_service.delete_admin(username=user.username)
        db.commit()
        return rows

    async def delete(self, db, user_id):
        # 删除指定用户
        ums_admin = db.query(UmsAdmin).filter_by(id=user_id).first()
        # 更新缓存信息
        admin_cache_service.delete_admin(username=ums_admin.username)
        db.delete(ums_admin)
        db.commit()

    async def update_role(self, db: Session, admin_id, roles):
        # 修改用户角色关系
        # count = len(roles)
        # 先删除原来的关系
        count = db.query(UmsAdminRoleRelation).filter_by(admin_id=admin_id).delete()
        # 建立新关系
        for r_id in roles:
            db.add(UmsAdminRoleRelation(admin_id=admin_id, role_id=r_id))
        db.commit()
        # TODO admin_cache_service 删除缓存资源列表
        admin_cache_service.del_resource_list_by_role_ids(roles)
        return count

    async def get_role_list(self, db: Session, admin_id: int):
        # 获取用户对于角色
        return db.query(UmsRole).join(UmsAdminRoleRelation, UmsAdminRoleRelation.admin_id == admin_id).filter(
            UmsAdminRoleRelation.role_id == UmsRole.id).all()

    async def get_resource_list(self, db: Session):
        # 获取指定用户的可访问资源
        pass

    async def update_permission(self, db: Session, admin_id, permission_ids):
        # 修改用户的+-权限
        # 开启事务
        db.begin(subtransactions=True)
        # 删除原所有权限关系
        db.query(UmsAdminPermissionRelation).filter_by(admin_id=admin_id).delete()
        # 获取用户所有角色权限
        permission_list = db.query(UmsPermission).join(UmsAdminRoleRelation, UmsAdminRoleRelation.admin_id == admin_id) \
            .join(UmsRole, UmsRole.id == UmsAdminRoleRelation.role_id) \
            .join(UmsRolePermissionRelation, UmsRolePermissionRelation.role_id == UmsRole.id) \
            .filter(UmsPermission.id == UmsRolePermissionRelation.permission_id) \
            .all()
        role_permission_ids = [p.id for p in permission_list]
        # 在已有权限的基础上添加传递过来的权限列表(+)
        add_role_permission_list = [p_id for p_id in permission_ids if p_id not in role_permission_ids]
        # 在已有权限的基础上筛选出需要剔除的权限列表(-)
        sub_role_permission_list = [p_id for p_id in role_permission_ids if p_id not in permission_ids]

        # 执行+-权限操作 向用户与权限的关系表中添加相关数据
        admin_permission_relation_list = []
        for permission_id in add_role_permission_list:
            admin_permission_relation_list.append(
                UmsAdminPermissionRelation(admin_id=admin_id, type=1,
                                           permission_id=permission_id))
        for permission_id in sub_role_permission_list:
            admin_permission_relation_list.append(
                UmsAdminPermissionRelation(admin_id=admin_id, type=-1,
                                           permission_id=permission_id))
        db.add_all(admin_permission_relation_list)
        db.commit()
        return len(admin_permission_relation_list)

    # def covert_to_ums_admin_permission_relation(self, **kwargs):
    #     return UmsAdminPermissionRelation(**kwargs)

    async def get_permission_list(self, db: Session, admin_id):
        # 获取用户所有权限（包括角色权限和+-权限）
        # permissions = db.query(UmsPermission).join(UmsAdminRoleRelation, UmsAdminRoleRelation.admin_id == admin_id) \
        #     .join(UmsRole, UmsRole.id == UmsAdminRoleRelation.role_id) \
        #     .join(UmsRolePermissionRelation, UmsRolePermissionRelation.role_id == UmsRole.id) \
        #     .filter(UmsPermission.id == UmsRolePermissionRelation.permission_id, UmsPermission.id is not None) \
        #     .all()
        permissions = db.query(UmsPermission).join(UmsAdminPermissionRelation,
                                                   UmsAdminPermissionRelation.admin_id == admin_id) \
            .filter(UmsPermission.id == UmsAdminPermissionRelation.permission_id) \
            .all()
        return permissions

    async def update_password(self, db: Session, pwd_info) -> bool:
        # 修改密码
        user = db.query(UmsAdmin).filter_by(username=pwd_info.username).first()
        if not user:
            raise BaseError(msg='找不到指定用户!')
        if not pwd_context.verify(pwd_info.old_password, user.password):
            raise BaseError(msg='旧密码错误!')
        # 生成hash密码 修改密码
        new_password = generate_hash_password(user.new_password)
        user.password = new_password
        db.commit()
        return True

    async def loader_user_by_username(self, db: Session, username, is_login=None):
        # 获取用户信息
        ums_admin = await self.get_admin_by_username(db=db, username=username, is_login=is_login)
        if ums_admin:
            return ums_admin
        else:
            raise BaseError(msg='用户名或密码错误')
