from PyQt5.QtWidgets import QWidget, QSplitter, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from views.sms_line_edit import SMSLineEdit
from views.sms_list_view import SMSListView
from views.sms_push_button import SMSPushButton
from views.sms_tree_view import SMSTreeView
from views.sms_scroll_area import SMSScrollArea
from common import get_config

class MainWindow(QWidget):
    '''
    程序主界面
    '''
    def __init__(self):
        QWidget.__init__(self)
        #主界面的布局
        self._layout_main = QHBoxLayout(self)
        #界面分隔控件
        self._splitter = QSplitter(Qt.Horizontal)
        #左侧树控件，用于显示分类信息
        self._tree_categories = SMSTreeView(self._splitter)
        # 设置树控件选择事伯
        self._tree_categories.set_select_changed_slot(self._slot_tree_select_changed)
        #用于过滤功能的编辑框
        self._layout_line_edit_with_label = QHBoxLayout()
        self._label_filter = QLabel('搜索')
        self._line_edit_filter = SMSLineEdit()
        self._layout_line_edit_with_label.addWidget(self._label_filter)
        self._layout_line_edit_with_label.addWidget(self._line_edit_filter)
        #功能区域布局
        self._layout_function_area = QHBoxLayout()
        self._button_add_item = SMSPushButton('添加')
        self._layout_function_area.addWidget(self._button_add_item)
        self._layout_function_area.addLayout(self._layout_line_edit_with_label)        
        #右侧整体布局
        self._widget_items = QWidget(self._splitter)        
        self._layout_item_area = QVBoxLayout(self._widget_items)
        self._layout_item_area.setContentsMargins(0, 0, 0, 0) #设置边距
        self._layout_item_area.addLayout(self._layout_function_area)        
        #滚动视图
        self._list_items_scroll = SMSScrollArea()
        self._list_items = SMSListView(self._list_items_scroll)
        self._list_items_scroll.set_view(self._list_items)
        #添加滚动控件
        self._list_items_scroll.setWidget(self._list_items)
        self._list_items_scroll.setWidgetResizable(True)
        self._layout_item_area.addWidget(self._list_items_scroll)
        #设置左右布局的比例
        self._splitter.setStretchFactor(1, 4)
        #将分隔控件加入布局
        self._layout_main.addWidget(self._splitter)
        #设置窗口属性
        self._config = get_config()
        self.setWindowTitle(self._config.get_window_title())
        self.setWindowIcon(QIcon(self._config.get_window_icon()))
        if self._config.get_window_is_full_screen() == 1:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setGeometry(self._config.get_window_x(), self._config.get_window_y(), 
                                    self._config.get_window_width(), self._config.get_window_height())
        #事件处理
        self._button_add_item.clicked.connect(self._list_items.add_item)
       
    def closeEvent(self, event):        
        if self.windowState() & Qt.WindowMaximized:
            self._config.set_window_is_full_screen(1)
        else:
            rect = self.geometry()
            self._config.set_window_x(rect.x())
            self._config.set_window_y(rect.y())
            self._config.set_window_width(rect.width())
            self._config.set_window_height(rect.height())
            self._config.set_window_is_full_screen(0)
        self._config.update()
        QWidget.closeEvent(self, event)
        
    def _slot_tree_select_changed(self, selected, deselected):
        index = selected.indexes()[0]
        current_item = index.internalPointer()
        self._list_items.set_category_filter(current_item.id)
        # 清空搜索框
        self._line_edit_filter.clear()
