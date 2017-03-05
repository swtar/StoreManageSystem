from PyQt5.QtWidgets import QScrollArea

class SMSScrollArea(QScrollArea):
    '''
    自定义滚动控件
    '''
    def __init__(self, parent = None):
        QScrollArea.__init__(self, parent)
        self._view = None
        
    def resizeEvent(self, event):
        content_size = self.contentsRect()
        self._view.update_view(content_size.width())
        QScrollArea.resizeEvent(self, event)
        
    def set_view(self, view):
        self._view = view
