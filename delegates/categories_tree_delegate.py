from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit
from PyQt5.QtCore import Qt, QSize

class CategoriesTreeDelegate(QStyledItemDelegate):
    '''
    分类显示树控件的委托
    '''
    def __init__(self, parent = 0):
        QStyledItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        return QLineEdit(parent)
        
    def setEditorData(self, editor, index):
        editor.setText(index.internalPointer().name)
        
    def setModelData(self, editor, model, index):
        if editor.text() != index.internalPointer().name:
            model.setData(index, editor.text(), Qt.EditRole)
        
    def sizeHint(self, option, index):
        return QSize(12, 20)
