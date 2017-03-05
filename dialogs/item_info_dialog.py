from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, \
                                           QHBoxLayout, QFileDialog, QSpinBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from constant import *
import os
import shutil

class ItemInfoDialog(QDialog):
    '''
    用于元素信息修改和显示的对话框
    '''
    def __init__(self, action = ITEM_ADD_ACTION, categories_table = {}, parent = None):
        QDialog.__init__(self, parent)
        self._action = action
        self._row_index = 0
        self.setWindowTitle('修改元素信息')
        self._temp_image = ''
        #对话框的布局
        self._main_layout = QGridLayout()
        #各种组件
        #显示图片
        self._image_label = QLabel()
        self._main_layout.addWidget(self._image_label, self._row_index, 0, 1, 2, Qt.AlignCenter)
        self._row_index += 1
        self._image_label.setMaximumWidth(ITEM_IMAGE_WIDTH)
        self._image_label.setMaximumHeight(ITEM_IMAGE_HEIGHT)
        #浏览图片
        self._main_layout.addWidget(QLabel('<b>图片：</b>'), self._row_index, 0, Qt.AlignLeft)
        self._image_button = QPushButton('浏览...')
        self._main_layout.addWidget(self._image_button, self._row_index, 1, Qt.AlignLeft)
        self._row_index += 1
        #名称
        self._main_layout.addWidget(QLabel('<b>名称：</b>'), self._row_index, 0, Qt.AlignLeft)
        self._name_edit = QLineEdit()
        name_edit_layout = QHBoxLayout()
        name_edit_layout.addWidget(self._name_edit)
        self._main_layout.addLayout(name_edit_layout, self._row_index, 1, Qt.AlignLeft)
        self._row_index += 1
        #分类
        self._main_layout.addWidget(QLabel('<b>分类：</b>'), self._row_index, 0, Qt.AlignLeft)
        self._category_combo = QComboBox()
        self._category_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        category_combo_layout = QHBoxLayout()
        category_combo_layout.addWidget(self._category_combo)
        self._main_layout.addLayout(category_combo_layout, self._row_index, 1, Qt.AlignLeft)
        self._row_index += 1
        #添加分类内容
        for k, v in categories_table.items():
            self._category_combo.addItem(v, k)
        #默认数量(添加时才有)
        if self._action == ITEM_ADD_ACTION:
            self._main_layout.addWidget(QLabel('<b>数量：</b>'), self._row_index, 0, Qt.AlignLeft)
            self._count_spin = QSpinBox()
            self._count_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self._count_spin.setMinimum(1)
            self._count_spin.setMaximum(99999)
            count_spin_layout = QHBoxLayout()
            count_spin_layout.addWidget(self._count_spin)
            self._main_layout.addLayout(count_spin_layout, self._row_index, 1, Qt.AlignLeft)
            self._row_index += 1
            #设置添加时的窗口标题
            self.setWindowTitle('添加元素信息')
            #设置添加时的默认图片
            self._image = 'resources/images/example.jpg'
            self._update_image(self._image)
        #量词
        self._main_layout.addWidget(QLabel('<b>量词：</b>'), self._row_index, 0, Qt.AlignLeft)
        self._quantifier_edit = QLineEdit()
        quantifier_edit_layout = QHBoxLayout()
        quantifier_edit_layout.addWidget(self._quantifier_edit)
        self._main_layout.addLayout(quantifier_edit_layout, self._row_index, 1, Qt.AlignLeft)
        self._row_index += 1
        #操作按钮
        button_layout = QHBoxLayout()
        self._ok_button = QPushButton('确定')
        self._ok_button.setDefault(True)
        self._cancel_button = QPushButton('取消')
        button_layout.addWidget(self._ok_button, 0, Qt.AlignRight)
        button_layout.addWidget(self._cancel_button, 0, Qt.AlignRight)
        self._main_layout.addLayout(button_layout, self._row_index, 0, 1, 2, Qt.AlignRight)
        self._row_index += 1
        #设置列比例
        self._main_layout.setColumnStretch(0, 1)
        self._main_layout.setColumnStretch(1, 100)
        #设置对话框大小
        self.setMaximumWidth(ITEM_DIALOG_WIDTH)
        self.setMaximumHeight(ITEM_DIALOG_HEIGHT)
        #设置布局
        self.setLayout(self._main_layout) 
        #设置信号
        self._image_button.clicked.connect(self._get_image_path)
        self._ok_button.clicked.connect(self._ok_button_clicked)
        self._cancel_button.clicked.connect(self._cancel_button_clicked)
        #重置窗口大小
        self.resize(ITEM_DIALOG_WIDTH, ITEM_DIALOG_HEIGHT)            
        
    def set_infos(self, infos):
        #更新图片
        self._image = infos.image
        image = QImage(self._image)
        self._image_label.setPixmap(QPixmap.fromImage(image.scaled(ITEM_IMAGE_WIDTH, ITEM_IMAGE_HEIGHT)))
        #更新名称
        self._name_edit.setText(infos.name)
        #更新分类
        index = self._category_combo.findData(infos.category)
        if index == -1:
            index == 0
        #数量
        self._count = infos.count
        self._category_combo.setCurrentIndex(index)
        #更新量词
        self._quantifier_edit.setText(infos.quantifier)
        
    def get_infos(self):
        infos = list()
        infos.append(self._image)
        infos.append(self._name_edit.text())
        infos.append(self._category_combo.currentData())
        if self._action == ITEM_ADD_ACTION:
            infos.append(self._count_spin.value())
        else:
            infos.append(self._count)
        infos.append(self._quantifier_edit.text())
        return infos
        
    def _update_image(self, path):
        if path and os.path.exists(path):
            image = QImage(path)
            self._image_label.setPixmap(QPixmap.fromImage(image.scaled(ITEM_IMAGE_WIDTH, ITEM_IMAGE_HEIGHT)))
        
    def _get_image_path(self):
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        result = QFileDialog.getOpenFileName(self, '选择一个图片文件', desktop_path, '图片文件 (*.png *.gif *.jpg)')
        if result[0]:   
            self._temp_image = result[0]
            self._update_image(self._temp_image)
            
    def _ok_button_clicked(self, checked):
        #复制文件
        if not os.path.exists(r'resources/images'):
            os.makedirs(r'resources/images')        
        if self._temp_image and os.path.exists(self._temp_image):
            file_name = os.path.basename(self._temp_image)
            self._image = r'resources/images/%s' % file_name
            shutil.copy(self._temp_image, self._image)
        QDialog.done(self, 1)
        
    def _cancel_button_clicked(self, checked):
        QDialog.done(self, 0)
