from PyQt5.QtCore import QAbstractItemModel, Qt, QVariant, QModelIndex, QSize
from PyQt5.QtGui import QIcon
from database.t_categories import TCategories
from database.database_session import get_database_session

class CategoriesTreeModel(QAbstractItemModel):
    '''
    用于分类显示的树控件的Model
    '''
    def __init__(self, view, parent = None):
        QAbstractItemModel.__init__(self, parent)
        self._view = view
        self._db_session = get_database_session()
        self._categories = self._db_session.query(TCategories).all()
        self._root = {}
        self._category_dict = {}
        #构造数据
        self._build_data()
        
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return '分类'
        return QVariant()
        
    def rowCount(self, index = QModelIndex()):
        parent_id  = 0
        if index.isValid():
            parent_id = index.internalPointer().id
        if parent_id in self._root:
            return len(self._root[parent_id])
        return 0
        
    def columnCount(self, index = QModelIndex()):
        return 1
        
    def data(self,  index, role = Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        #用于显示的角色
        if role == Qt.DisplayRole or role == Qt.EditRole:
            category = index.internalPointer()
            return category.name
        #设置行高的角色
        if role == Qt.SizeHintRole:
            return QSize(16, 20)
        #行的图标
        if role == Qt.DecorationRole:
            return QIcon(r'resources/icons/main.png')
        #用于编辑时的编辑框默认值
        if role == Qt.EditRole:
            category = index.internalPointer()
            return category.name
        
        return QVariant()
        
    def index(self, row, column, parent = QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
            
        parent_id = 0
        if parent.isValid():
            parent_id = parent.internalPointer().id
            
        child_item = self._root[parent_id][row]
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()
        
    def parent(self, index):        
        if not index.isValid():
            return QModelIndex()
        
        child_item = index.internalPointer()
        
        parent_id = child_item.parent
        if parent_id == 0:
            return QModelIndex()
        
        parent_item = None
        if child_item.parent != 0:
            parent_item = self._category_dict[child_item.parent]
        
        return self.createIndex(self._get_index(child_item.id, parent_id), 0, parent_item)
        
    def flags(self, index):
        current_flags = QAbstractItemModel.flags(self, index)
        current_item = index.internalPointer()
        if current_item.parent == 0:
            return current_flags
        else:
            return current_flags | Qt.ItemIsEditable
            
    def setData(self, index, value, role):
        current_item = index.internalPointer()
        if role == Qt.EditRole:
            current_item.name = value
            self._update_data()
        return True
        
    def has_child(self, index):
        category_id = index.internalPointer().id
        if category_id in self._root and len(self._root[category_id]) > 0:
            return True
        return False
        
    def remove_item(self, index):
        current_item = index.internalPointer()
        self._db_session.execute('delete from t_categories where parent = %d' % current_item.id)
        self._db_session.execute('delete from t_categories where id = %d' % current_item.id)
        self._update_data(True)
        self._view_redraw()
            
    def add_item(self, name, parent):
        new_item = TCategories()
        new_item.name = name
        new_item.parent = parent.internalPointer().id
        self._db_session.add(new_item)
        self._update_data(True)
        self._view_redraw()
             
    def _get_index(self, id, parent):
        children = self._root[parent]
        index = 0
        for x in children:
            if x.id == id:
                return index
            else:
                index += 1
    
    def _build_data(self):
        self._category_dict.clear()
        self._root.clear()
        self._categories = self._db_session.query(TCategories).all()
        index = 0
        for category in self._categories:
            index += 1
            self._category_dict[category.id] = category
            if category.parent not in self._root:
                self._root[category.parent] = list()
            self._root[category.parent].append(category)
            
    def _update_data(self, update = False):
        self._db_session.commit()
        if update:
            self._build_data()
            
    def _view_redraw(self):
        #重绘临时解决方案
        self._view.collapseAll()
        self._view.expandAll()
