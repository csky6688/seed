from flask import request

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.menu import Menu as MenuModel
from seed.utils.auth import api_require_super_admin


class MenuSchema(BaseSchema):
    class Meta:
        model = MenuModel
    

class Menu(RestfulBaseView):
    """ menu
    """
    model_class = MenuModel
    schema_class = MenuSchema

    decorators = [api_require_super_admin]

    def get(self, model_id=None):
        """ GET
        """
        query_session = self.session.query(self.model_class)
        menu_data = query_session.all()


    def post(self):
        """ 更新菜单结构
        """
        menus = request.get_json()
        self._decode_menus(menus)
        return self.response_json(self.HttpErrorCode.SUCCESS)
    
    def _encode_menus(self, menu_data):
        menu_data = {'-'.join([row.parent_id, row.left_id]): row.row2dict() for row in menu_data}
        menus = []
        tree_stack = []


    def _decode_menus(self, menus, parent_id=0, left_id=0):
        if not menus:
            return

        for menu in menus:
            # 更新或插入新的菜单
            # 获取到菜单对应的ID
            left_id = current_id = self._insert_or_update_menu(menu, parent_id, left_id)
            self._decode_menus(menu.get('sub_menus', []), parent_id=current_id, left_id=0)
    
    def _insert_or_update_menu(self, menu, parent_id, left_id):
        menu.update({
            'parent_id': parent_id,
            'left_id': left_id
        })
        schema = self.schema_class()
        datas, errors = schema.load(menu)
        # if errors:
            # return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        datas.save()
        return datas.id