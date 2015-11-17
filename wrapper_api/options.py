from PySide import QtGui

class OptionsWrapper:
    
    def __init__(self, optionsWidget):
        self.__options = {}
        self.optionsWidget = optionsWidget
        
    def build(self):
        #print type(self.optionsWidget)
        for i in xrange(self.optionsWidget.rowCount()):
            key = None
            value = None
            
            if self.optionsWidget.itemAt(i, QtGui.QFormLayout.ItemRole.LabelRole) is None:
                continue
            
            key = self.optionsWidget.itemAt(i, QtGui.QFormLayout.ItemRole.LabelRole).widget().text()
            widget = self.optionsWidget.itemAt(i, QtGui.QFormLayout.ItemRole.FieldRole).widget()
            if isinstance(widget, QtGui.QLineEdit):
                value = widget.text()
            elif isinstance(widget, QtGui.QCheckBox):
                value = widget.isChecked()
            else:
                value = self.optionsWidget.itemAt(i, QtGui.QFormLayout.ItemRole.FieldRole).widget().value()
            if key != "":
                self.__options[key] = value
        
    def getOptions(self):
        return self.__options
