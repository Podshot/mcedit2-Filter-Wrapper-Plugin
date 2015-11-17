"""
    storagedrawers
"""
from PySide import QtGui, QtCore
from mcedit2.plugins import registerToolClass
import logging
from glob import glob
import os
import sys
import imp
from mcedit2.editortools import EditorTool
from mcedit2.command import SimplePerformCommand
from wrapper_api.level import LevelWrapper
from wrapper_api.options import OptionsWrapper

log = logging.getLogger(__name__)

sys.path.remove("c:\\users\\jonathan\\python\\mcedit\\mceditunified")
#print sys.modules.keys()
    
class FilterCommand(SimplePerformCommand):
    
    def __init__(self, editorSession, filterModule, levelWrapper, box, options):
        super(FilterCommand, self).__init__(editorSession)
        self.levelWrapper = levelWrapper
        self.box = box
        self.options = options
        self.filterModule = filterModule
        
    def perform(self):
        self.filterModule.perform(self.levelWrapper, self.box, self.options)

class TestTool(EditorTool):
    name = "Legacy Filter Wrapper"
    iconName = "filter"
    filters = []
    filterDictionary = {}
    pickedFilter = None
    needsReload = None
    
    def runFilter(self):
        print "Running filter..."
        if self.editorSession.currentSelection is None:
            raise Exception("There has to be Selection Box")
        options = OptionsWrapper(self.stackedWidget.currentWidget().layout())
        options.build()
        level = LevelWrapper(self.editorSession.worldEditor, self.editorSession)
        command = FilterCommand(self.editorSession, 
                                self.filterDictionary[self.pickedFilter], 
                                level, 
                                self.editorSession.currentSelection, 
                                options.getOptions())
        self.editorSession.pushCommand(command)
    
    def organizeFilters(self):
        for filt in self.filters:
            with open(filt) as filter_file:
                try:
                    module_name = filt.split(os.path.sep)[-1].replace(".py", "")
                    module = imp.load_source(module_name, filt.replace(filt, module_name), filter_file)
                    if not (hasattr(module, 'displayName')): 
                        module.displayName = module_name
                    self.filterDictionary[module.displayName] = module
                except Exception as e:
                    print "Exception: " + str(e)
                    pass
                
    def changeWidget(self, value):
        self.pickedFilter = value    
        self.stackedWidget.setCurrentIndex(self.filterDictionary.keys().index(value))
    
    def buildFilterPanel(self, filt):
        module = self.filterDictionary[filt]
        if not hasattr(module, 'inputs'):
            widget = QtGui.QWidget()
            layout = QtGui.QFormLayout()
            layout.addRow("", QtGui.QLabel("No inputs"))
            widget.setLayout(layout)
            return widget
        widget = QtGui.QWidget()
        layout = QtGui.QFormLayout()
        for input in module.inputs:
            name = input[0]
            field = None
            if isinstance(input[1], tuple):
                if isinstance(input[1][0], (int, float)):
                    if isinstance(input[1][0], int):
                        field = QtGui.QSpinBox()
                        field.setValue(input[1][0])
                        #field.valueChanged[int].connect(lambda value: self.options.setIntValue(name, value))
                    else:
                        field = QtGui.QDoubleSpinBox()
                        field.setValue(input[1][0])
                        field.setSingleStep(0.1)
                        #field.valueChanged[float].connect(lambda value: self.options.setFloatValue(name, value))
                    if len(input[1]) == 3:
                        field.setMinimum(input[1][1])
                        field.setMaximum(input[1][2])
                if input[1][0] == "string":
                    field = QtGui.QLineEdit()
                    field.setValue("=".join(input[1][1].split("=")[1:]))
                    #field.textChanged[str].connect(lambda value: self.options.setStringValue(name, value))
            elif isinstance(input[1], (str, unicode)):
                if input[1] != "label":
                    field = QtGui.QLineEdit()
                    #field.textChanged[str].connect(lambda value: self.options.setStringValue(name, value))
                else:
                    field = QtGui.QLabel(input[0])
                    name = ""
            elif isinstance(input[1], bool):
                field = QtGui.QCheckBox()
                if input[1]:
                    field.setCheckState(QtCore.Qt.Checked)
                else:
                    field.setChecked(QtCore.Qt.Unchecked)
                #field.stateChanged.connect(lambda value: self.options.setBoolValue(name, value))
            layout.addRow(name, field)
        widget.setLayout(layout)
        return widget
    

    def buildFilterPanels(self, keys):
        self.stackedWidget = widget = QtGui.QStackedWidget()
        for key in self.filterDictionary.keys():
            filter_widget = self.buildFilterPanel(key)
            widget.addWidget(filter_widget)
        return widget
    
    def toolActive(self):
        if self.needsReload:
            self.organizeFilters()
            for i in xrange(0, self.filterPicker.count()):
                self.filterPicker.removeItem(i)
            for filt in sorted(self.filterDictionary.keys()):
                self.filterPicker.addItem(filt)
    
    def toolInactive(self):
        self.needsReload = True
        
    def findFilters(self):
        if not os.path.exists(os.path.join(self.dirpath, "filters")):
            os.mkdir(os.path.join(self.dirpath, "filters"))
        for f in glob(os.path.join(self.dirpath, "filters", "*.py")):
            self.filters.append(f)
    
    def __init__(self, editorSession, *args, **kwargs):
        super(TestTool, self).__init__(editorSession, *args, **kwargs)
        self.dirpath = os.path.dirname(__file__)
        if ("mceditunified") in sys.path:
            sys.path.remove("c:\\users\\jonathan\\python\\mcedit\\mceditunified")
        #print sys.modules.keys()
        if os.path.exists(os.path.join(self.dirpath, 'wrapper_api.zip')):
            sys.path.insert(0, 'wrapper_api.zip')
            try:
                #print "Importing here?"
                #log.critical("Importing here?")
                import wrapper_api
                #print "File: " + str(wrapper_api.__file__)
                #print "Path: " + str(wrapper_api.__path__)
                sys.modules["pymclevel"] = wrapper_api
            except:
                print "Failed"
        #print sys.modules.keys()
        self.findFilters()
        self.organizeFilters()
        
        widget = QtGui.QWidget()
        self.toolWidget = widget
        
        self.filterButton = QtGui.QPushButton("Run Filter")
        self.filterButton.clicked.connect(self.runFilter)
        self.filterPicker = QtGui.QComboBox()
        for filt in sorted(self.filterDictionary.keys()):
            self.filterPicker.addItem(filt)
        self.filterPicker.activated[str].connect(self.changeWidget)
        layout = QtGui.QFormLayout()
        layout.addRow("Filter", self.filterPicker)
        layout.addRow("Inputs", self.buildFilterPanels(self.filterDictionary.keys()[0]))
        layout.addWidget(self.filterButton)
        widget.setLayout(layout)
        self.pickedFilter = self.filterPicker.currentText()
        self.needsReload = False
        
        
    
registerToolClass(TestTool)