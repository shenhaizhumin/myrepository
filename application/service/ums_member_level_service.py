from application.model.ums_member_level import UmsMemberLevel
from typing import List


class UmsMemberLevelService(object):
    async def member_list(self, db, default_status) -> List[UmsMemberLevel]:
        return db.query(UmsMemberLevel).filter_by(default_status=default_status).all()
