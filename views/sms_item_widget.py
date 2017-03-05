from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap, QFontMetrics, QPalette, QColor
from PyQt5.QtCore import Qt
from constant import *
class SMSItemWidget(QFrame):
    '''
    用于显示Items的Widget
    '''
    def __init__(self, id, parent = None):
        QFrame.__init__(self, parent)
        #元素属性
        self._item_id = 0
        self._item_image = ''
        self._item_name = ''
        self._item_category = ''
        self._item_count = 0
        self._item_quantifier = ''
        #元素总布局
        self._main_layout = QVBoxLayout()
        #设置widget的整体宽高
        self.setMaximumWidth(ITEM_WIDGET_WIDTH)
        self.setMaximumHeight(ITEM_WIDGET_HEIGHT)
        #元素图片
        self._item_image_widget = QLabel()
        self._item_image_widget.setMaximumWidth(ITEM_IMAGE_WIDTH)
        self._item_image_widget.setMaximumHeight(ITEM_IMAGE_HEIGHT)
        self._main_layout.addWidget(self._item_image_widget)
        #信息展示布局
        self._info_layout = QGridLayout()
        #名称
        self._info_layout.addWidget(QLabel('<b>名称:</b>'), 0, 0, Qt.AlignLeft)
        self._item_name_widget = QLabel()
        self._item_name_widget.setMaximumWidth(ITEM_TEXT_WIDTH)
        self._info_layout.addWidget(self._item_name_widget, 0, 1, Qt.AlignLeft)
        #分类
        self._info_layout.addWidget(QLabel('<b>分类:</b>'), 1, 0, Qt.AlignLeft)
        self._item_category_widget = QLabel()
        self._item_category_widget.setMaximumWidth(ITEM_TEXT_WIDTH)
        self._info_layout.addWidget(self._item_category_widget, 1, 1, Qt.AlignLeft)
        #数量
        self._info_layout.addWidget(QLabel('<b>库存:</b>'), 2, 0, Qt.AlignLeft)
        self._item_count_widget = QLabel()
        self._item_count_widget.setMaximumWidth(ITEM_TEXT_WIDTH)
        self._info_layout.addWidget(self._item_count_widget, 2, 1, Qt.AlignLeft)
        self._main_layout.addLayout(self._info_layout)
        #信息布局比例
        self._info_layout.setColumnStretch(0, 1)
        self._info_layout.setColumnStretch(1, 100)
        #操作布局
        self._action_layout = QHBoxLayout()
        self._item_in_action = QLabel('<a href="%d"><b>入库</b></a>' % id)
        self._item_in_action.setAlignment(Qt.AlignCenter)
        self._action_layout.addWidget(self._item_in_action)
        self._item_out_action = QLabel('<a href="%d"><b>出库</b></a>' % id)
        self._item_out_action.setAlignment(Qt.AlignCenter)
        self._action_layout.addWidget(self._item_out_action)
        self._item_modify_action = QLabel('<a href="%d"><b>修改</b></a>' % id)
        self._item_modify_action.setAlignment(Qt.AlignCenter)
        self._action_layout.addWidget(self._item_modify_action)
        self._item_remove_action = QLabel('<a href="%d"><b>删除</b></a>' % id)
        self._item_remove_action.setAlignment(Qt.AlignCenter)
        self._action_layout.addWidget(self._item_remove_action)
        self._main_layout.addLayout(self._action_layout)
        #设置当前Widget的Layout
        self.setLayout(self._main_layout)
        #绘制背景
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Background)
        self.setPalette(QPalette(QColor(240, 240, 240)))
        #边框相关
        self.setFrameShadow(QFrame.Raised)
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(5)
        
    def set_id(self, id):
        self._item_id = id
        
    def get_id(self):
        return self._item_id
        
    def set_image(self, path):
        self._item_image = path
        
    def get_image(self):
        return self._item_image
        
    def set_name(self, name):
        self._item_name = name
        
    def get_name(self):
        return self._item_name
        
    def set_category(self, category):
        self._item_category = category
        
    def get_category(self):
        return self._item_category
        
    def set_count(self, count):
        self._item_count = count
        
    def get_count(self):
        return self._item_count
        
    def set_quantifier(self, quantifier):
        self._item_quantifier = quantifier
        
    def get_quantifier(self):
        return self._item_quantifier
        
    def set_item_in_action(self, action):
        self._item_in_action.linkActivated.connect(action)
        
    def set_item_out_action(self, action):
        self._item_out_action.linkActivated.connect(action)
        
    def set_item_remove_action(self, action):
        self._item_remove_action.linkActivated.connect(action)
        
    def set_item_modify_action(self, action):
        self._item_modify_action.linkActivated.connect(action)
        
    def update(self):
        #图片
        image = QImage(self._item_image)       
        self._item_image_widget.setPixmap(QPixmap.fromImage(image.scaled(ITEM_IMAGE_WIDTH, ITEM_IMAGE_HEIGHT)))
        #名称
        font_metrics = QFontMetrics(self.font())
        self._item_name_widget.setText('<span style="color:red">%s</span>' % \
        font_metrics.elidedText(self._item_name, Qt.ElideRight, \
        self._item_name_widget.maximumWidth()))
        self._item_name_widget.setToolTip(self._item_name)
        #分类
        self._item_category_widget.setText('<span style="color:olive">%s</span>' % \
        font_metrics.elidedText(self._item_category, Qt.ElideRight, \
        self._item_category_widget.maximumWidth()))
        self._item_category_widget.setToolTip(self._item_category)
        #数量
        count_str = '%s（%s）' % (str(self._item_count), self._item_quantifier)
        self._item_count_widget.setText('<span style="color:green">%s</span>' % \
        font_metrics.elidedText(count_str, Qt.ElideRight, \
        self._item_count_widget.maximumWidth()))
        self._item_count_widget.setToolTip(count_str)
        
