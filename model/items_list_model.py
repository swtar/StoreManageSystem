from database.t_items import TItems
from database.t_categories import TCategories
from database.database_session import get_database_session
from constant import *

class ItemsListModel(object):
    def __init__(self, parent = None):
        self._parent = parent
        self._db_session = get_database_session(True)
        self._items = self._db_session.query(TItems).all()
        self._categories = self._db_session.query(TCategories).all()
        self._categories_table = dict()
        for category in self._categories:
            self._categories_table[category.id] = category.name
    
    def get_category_name(self, id):
        return self._categories_table.get(id, '未知分类')
    
    def get_items(self):
        return self._items

    def get_categories_table(self):
        return self._categories_table
        
    def add_item(self, infos):
        item = TItems()
        item.name = infos[ITEM_NAME_INDEX]
        item.image = infos[ITEM_IMAGE_INDEX]
        item.category = infos[ITEM_CATEGORY_INDEX]
        item.quantifier = infos[ITEM_QUANTIFIER_INDEX]
        item.description = infos[ITEM_NAME_INDEX]
        item.count = infos[ITEM_COUNT_INDEX]
        self._db_session.add(item)
        self._db_session.commit()
        return item
        
    def item_commit(self):
        self._db_session.commit()

    def remove_item(self, item):
        self._db_session.delete(item)
        self._db_session.commit()
        
    def flush_data(self):
        self._items = self._db_session.query(TItems).all()
        self._categories = self._db_session.query(TCategories).all()        
