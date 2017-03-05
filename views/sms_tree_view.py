from PyQt5.QtWidgets import QTreeView, QAction, QMenu, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import QCursor
from model.categories_tree_model import CategoriesTreeModel
from delegates.categories_tree_delegate import CategoriesTreeDelegate

class SMSTreeView(QTreeView):
    '''
    自定义树控件
    '''
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)
        #model
        self._model = CategoriesTreeModel(self)
        self.setModel(self._model)
        # selectionMode
        self._selection_model = QItemSelectionModel(self._model, self)        
        self.setSelectionModel(self._selection_model)
        #delegate
        self._delegate = CategoriesTreeDelegate(parent)
        self.setItemDelegate(self._delegate)
        #阻止双击时出现编辑框
        self.setEditTriggers(self.NoEditTriggers)
        #设置展开/收缩动画
        self.setAnimated(True)
        #展开所有
        self.expandAll()
        #开启右键自定义菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        #右键菜单信号槽
        self.customContextMenuRequested.connect(self._slot_custom_context_menu)
        #右键菜单项
        self._context_menu_add_child = QAction('添加子分类')
        self._context_menu_add_child.triggered.connect(
                                                 self._slot_context_menu_add_child)
        self._context_menu_rename = QAction('重命名')
        self._context_menu_rename.triggered.connect(
                                                 self._slot_context_menu_rename)
        self._context_menu_delete = QAction('删除该分类')
        self._context_menu_delete.triggered.connect(
                                                 self._slot_context_menu_delete)
        # 设置默认选择为 root
        self._selection_model.select(self.rootIndex(), QItemSelectionModel.SelectCurrent)
        
    def _slot_custom_context_menu(self, point):
        menu = QMenu()
        current_index = self.currentIndex()
        current_item = current_index.internalPointer()
        #添加子类 菜单项
        menu.addAction(self._context_menu_add_child)
        #重命名 菜单项 和 删除 菜单项
        if current_item.parent != 0:
            menu.addAction(self._context_menu_rename)
            menu.addAction(self._context_menu_delete)
        
        menu.exec(QCursor.pos())
        
    def _slot_context_menu_rename(self, checked):
        self.edit(self.currentIndex())            

    def _slot_context_menu_add_child(self, checked):
        current_index = self.currentIndex()
        result = QInputDialog.getText(self, '添加新分类', '请输入分类名', text = '新分类')
        if result[1]:
            if not result[0]:
                QMessageBox.critical(self, '添加失败', '分类名不能为空')
            else:
                self._model.add_item(result[0], current_index)
    
    # 2017.2.11 sqlalchemy 一执行删除就挂了，不晓得为啥子
    def _slot_context_menu_delete(self, checked):
        QMessageBox.information(self, '功能暂时不可用', 'sqlalchemy 一执行删除就挂了，不晓得为啥子')
        return 0
        current_index = self.currentIndex()
        if self._model.has_child(current_index):
            if QMessageBox.question(self, '确认', \
            '该分类下还有子分类，删除该分类将连带删除子分类，确定删除？') \
            != QMessageBox.Yes:
                return 0        
        self._model.remove_item(current_index)
        
    def set_select_changed_slot(self, slot):
        self._selection_model.selectionChanged.connect(slot)
