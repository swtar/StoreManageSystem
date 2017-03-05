from PyQt5.QtWidgets import QWidget, QGridLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from model.items_list_model import ItemsListModel
from views.sms_item_widget import SMSItemWidget
from dialogs.item_info_dialog import ItemInfoDialog
from constant import *
import os
import copy as cp

class SMSListView(QWidget):
    '''
    自定义列表控件
    '''
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self._model = ItemsListModel(self)
        self._width = 250
        # 当前的分类过滤
        self._category = 1
        #主布局
        self._main_layout = QGridLayout()
        #生成数据
        self._make_data()
        self._make_items()
        # 分类过滤后的元素
        self._displayable_by_category = [v[0] for v in self._items.values()]
        # 搜索过滤后的元素
        self._displayable_by_search = cp.copy(self._displayable_by_category)
        self._show_items()
        #设置布局
        self.setLayout(self._main_layout)
        #画背景   
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Background)
        self.setPalette(QPalette(QColor(Qt.white)))
    
    # item_id => item
    def _make_data(self):
        if hasattr(self, '_data'):
            del self._data            
        self._data = dict()
        for item in self._model.get_items():
            self._data[item.id] = list()
            self._data[item.id].append(item)
            
    def _add_data(self, item):
        self._data[item.id] = list()
        self._data[item.id].append(item)
            
    # 构造出所有的元素item_widget
    def _make_items(self):
        if hasattr(self, '_items'):
            self._items.clear()
        else:
            self._items = dict()            
        for v in self._data.values():
            current_data = v[0]
            self._add_item(current_data)
            
    def _add_item(self, current_data):
        item = SMSItemWidget(current_data.id)
        item.set_id(current_data.id)
        item.set_image(current_data.image)
        item.set_name(current_data.name)
        item.set_category(self._model.get_category_name(current_data.category))
        item.set_count(current_data.count)
        item.set_quantifier(current_data.quantifier)
        #事件
        item.set_item_in_action(self.item_in)
        item.set_item_out_action(self.item_out)
        item.set_item_remove_action(self.remove_item)
        item.set_item_modify_action(self.modify_item)
        #更新显示
        item.update()
        #添加到数据
        self._items[current_data.id] = list()
        self._items[current_data.id].append(item)
        self._items[current_data.id].append(current_data.category)               
    
    def _show_items(self):        
        #计算一行中可以容纳几个元素
        item_count_in_row = (self._width / 175) - 1
        #向控件插入元素
        current_row = 0
        current_column = 0
        for item in self._displayable_by_search:
            self._main_layout.addWidget(item, current_row, current_column, Qt.AlignLeft)
            current_column += 1
            if current_column > item_count_in_row:
                current_row += 1
                current_column = 0       
       
    def _clear_items(self):
        #删除布局中的所有元素
        result = self._main_layout.takeAt(0)
        while result != None:
            result = self._main_layout.takeAt(0)
        self._main_layout.invalidate()
        
    def update_view(self, width):
        self._width = width
        self._clear_items()
        self._show_items()
    
    # 2017.2.13 23:51 妈的，删除又有问题    
    def remove_item(self, url):
        QMessageBox.information(self, '唉', '这个功能还有Bug，稍候解决')
        return 0 # 唉，不想搞了
        id = int(url)
        current_data = self._data[id][0]
        result = QMessageBox.question(self, '确认', '确认删除 %s 吗？' % current_data.name)
        if result == QMessageBox.Yes:            
            self._model.remove_item(current_data)
            #删除图片文件
            image_file_name = os.path.basename(current_data.image)
            if image_file_name != 'example.jpg':
                os.remove(current_data.image)
            # 从数据结构中删除
            if current_data.id in self._data:
                self._data[current_data.id].clear()
                del self._data[current_data.id]
            if current_data.id in self._items:
                self._items[current_data.id].clear()
                del self._items[current_data.id]    
            # 重绘
            self._clear_items()
            self._show_items()
           
    def add_item(self):
        dialog = ItemInfoDialog(ITEM_ADD_ACTION, self._model.get_categories_table(), self)
        if dialog.exec():
            infos = dialog.get_infos()
            item = self._model.add_item(infos)
            self._add_data(item)
            self._add_item(item)
            # 更新
            self.set_category_filter(self._category)
            
    def modify_item(self, url):
        id = int(url)
        categories_table = self._model.get_categories_table()
        dialog = ItemInfoDialog(ITEM_MODIFY_ACTION, categories_table, self)
        current_data = self._data[id][0]
        dialog.set_infos(current_data)
        if dialog.exec():
            new_infos = dialog.get_infos()
            current_data.name = new_infos[ITEM_NAME_INDEX]
            current_data.image = new_infos[ITEM_IMAGE_INDEX]
            current_data.category = new_infos[ITEM_CATEGORY_INDEX]
            current_data.quantifier = new_infos[ITEM_QUANTIFIER_INDEX]
            self._model.item_commit()
            current_item = self._items[current_data.id][0]
            current_item.set_name(current_data.name)
            current_item.set_image(current_data.image)
            current_item.set_category(categories_table[current_data.category])
            current_item.set_quantifier(current_data.quantifier)
            current_item.update()
        
    def item_in(self, url):
        id = int(url)
        current_data = self._data[id][0]
        result = QInputDialog.getInt(self, '%s 入库' % current_data.name, '请输入要入库的数量', 1, 1, 99999)
        if result[1]:
            current_data.count += int(result[0])
            self._model.item_commit()
            current_item = self._items[current_data.id][0]
            current_item.set_count(current_data.count)
            current_item.update()
        
    def item_out(self, url):
        id = int(url)
        current_data = self._data[id][0]
        result = QInputDialog.getInt(self, '%s 出库' % current_data.name, '请输入要出库的数量', 
                                                current_data.count, 0, current_data.count)
        if result[1] and int(result[0]) > 0:
            current_data.count -= int(result[0])
            self._model.item_commit()
            current_item = self._items[current_data.id][0]
            current_item.set_count(current_data.count)
            current_item.update()
            
    def set_category_filter(self, category):
        self._category = category
        if category == 1:
            self._displayable_by_category = [v[0] for v in self._items.values()]
        else:
            self._displayable_by_category.clear()
            for v in self._items.values():
                if v[1] == category:
                    self._displayable_by_category.append(v[0])
        self._displayable_by_search = cp.copy(self._displayable_by_category)
        self._clear_items()
        self._show_items()
