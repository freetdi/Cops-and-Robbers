"""
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to 
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

''' written by Lukas Larisch (2014-2018)
    e-mail: lukas.larisch@kaust.edu.sa \
    version 1.0

'''

from PyQt4 import QtGui, QtCore
import sys
import pickle
import Graph
import copy
import SetOp
import signal
from random import randint
from math import sqrt

class GraphData(object):
    def __init__(self, name=str(), idx=0):
        self.Name = name
        self.G = Graph.Graph()
        self.verticesData = list()
        self.edgesData = list()
        self.index = idx

class CopsAndRobbers(QtGui.QMainWindow):
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('./icons/icon_cop.ico'))
        self.setWindowTitle('Cops and Robbers')
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))
        self.pen.setWidth(1) 
        self.brush = QtGui.QBrush(QtGui.QColor(160,120,80))
        self.brushSelected = QtGui.QBrush(QtGui.QColor(255,0,0))
        self.brushBoard = QtGui.QBrush(QtGui.QColor(220,220,220))
        self.font = QtGui.QFont("Helvetica", 12) 
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.borderX = self.screen.width()
        self.borderY = self.screen.height()
        
        self.GroupBoxMode = QtGui.QGroupBox("Mode:",self)
        self.RadioSwitch1 = QtGui.QRadioButton("&Create Graph", self)
        self.RadioSwitch2 = QtGui.QRadioButton("&Cops and Robbers", self)
        self.RadioSwitch3 = QtGui.QRadioButton("&Decomposition", self)
        self.RadioSwitch1.setChecked(True)
        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox1.addWidget(self.RadioSwitch1)
        self.vbox1.addWidget(self.RadioSwitch2)
        self.vbox1.addWidget(self.RadioSwitch3)
        self.vbox1.addStretch(1)
        self.GroupBoxMode.setLayout(self.vbox1)
        self.GroupBoxMode.resize(300,200)
        self.GroupBoxMode.move(self.borderX-180,480)
        self.RadioSwitch1.clicked.connect(self.onActivatedGroupBoxMode)
        self.RadioSwitch2.clicked.connect(self.onActivatedGroupBoxMode)
        self.RadioSwitch3.clicked.connect(self.onActivatedGroupBoxMode)

        self.ToolbarAdd = QtGui.QAction(QtGui.QIcon('./icons/add.ico'), 'Add Graph', self)
        self.ToolbarAdd.setShortcut('Ctrl+N')
        self.connect(self.ToolbarAdd, QtCore.SIGNAL('triggered()'), self.addGraph_template)

        self.ToolbarRemove = QtGui.QAction(QtGui.QIcon('./icons/close.ico'), 'Remove Graph', self)
        self.ToolbarRemove.setShortcut('Ctrl+D')
        self.connect(self.ToolbarRemove, QtCore.SIGNAL('triggered()'), self.removeGraph)
        
        self.Toolbar = self.addToolBar('Options')
        self.Toolbar.addAction(self.ToolbarAdd)
        self.Toolbar.addAction(self.ToolbarRemove)
        self.Toolbar.setMovable(False)

        self.ComboGraphs = QtGui.QComboBox(self)
        self.ComboGraphs.move(100,5)
        self.ComboGraphs.activated[str].connect(self.onActivatedSelectGraph)
        self.ComboGraphs.show()
        
        self.ComboVertexSize = QtGui.QComboBox(self)
        self.ComboVertexSize.addItem("Tiny")
        self.ComboVertexSize.addItem("Small")
        self.ComboVertexSize.addItem("Normal")
        self.ComboVertexSize.addItem("Large")
        self.ComboVertexSize.addItem("Huge")
        self.ComboVertexSize.setCurrentIndex(2) 
        self.ComboVertexSize.move(self.borderX-150, 100)
        self.ComboVertexSize.activated[str].connect(self.onActivatedVertexSize)
        
        self.ComboCopsCount = QtGui.QComboBox(self)
        self.ComboCopsCount.addItem("1")
        self.ComboCopsCount.addItem("2")
        self.ComboCopsCount.addItem("3")
        self.ComboCopsCount.addItem("4")
        self.ComboCopsCount.addItem("5")
        self.ComboCopsCount.addItem("6")
        self.ComboCopsCount.addItem("7")
        self.ComboCopsCount.addItem("8")
        self.ComboCopsCount.addItem("9")
        self.ComboCopsCount.addItem("10")
        self.ComboCopsCount.setCurrentIndex(1) 
        self.ComboCopsCount.move(self.borderX-150, 100)
        self.ComboCopsCount.activated[str].connect(self.onActivatedCopsCount)
        self.ComboCopsCount.hide()
        
        self.ExecuteButton = QtGui.QPushButton(self)
        self.ExecuteButton.setText("Catch!")
        self.ExecuteButton.move(self.borderX-450,self.borderY-140)
        self.ExecuteButton.clicked.connect(self.onActivatedExecute)
        self.ExecuteButton.hide()
        

        self.ResetButton = QtGui.QPushButton(self)
        self.ResetButton.setText("Reset")
        self.ResetButton.move(self.borderX-300,self.borderY-140)
        self.ResetButton.clicked.connect(self.onActivatedReset)
        self.ResetButton.hide()

        #Vertex Operations
        self.ButtonCreateVertices = QtGui.QPushButton(self)
        self.ButtonCreateVertices.setText("Create Vertices")
        self.ButtonCreateVertices.resize(140,30)
        self.ButtonCreateVertices.move(self.borderX-150,150)
        self.ButtonCreateVertices.clicked.connect(self.onActivatedCreateVertices)
        
        self.ButtonDeleteVertices = QtGui.QPushButton(self)
        self.ButtonDeleteVertices.setText("Delete Vertices")
        self.ButtonDeleteVertices.resize(140,30)
        self.ButtonDeleteVertices.move(self.borderX-150,180)
        self.ButtonDeleteVertices.clicked.connect(self.onActivatedDeleteVertices)
        
        self.ButtonRelocate = QtGui.QPushButton(self)
        self.ButtonRelocate.setText("Relocate Vertices")
        self.ButtonRelocate.resize(140,30)
        self.ButtonRelocate.move(self.borderX-150,210)
        self.ButtonRelocate.clicked.connect(self.onActivatedRelocate)

        #Edge Operations
        self.ButtonCreateEdges = QtGui.QPushButton(self)
        self.ButtonCreateEdges.setText("Create Edges")
        self.ButtonCreateEdges.resize(140,30)
        self.ButtonCreateEdges.move(self.borderX-150,280)
        self.ButtonCreateEdges.clicked.connect(self.onActivatedCreateEdges)       
        
        self.ButtonDeleteEdges = QtGui.QPushButton(self)
        self.ButtonDeleteEdges.setText("Delete Edges")
        self.ButtonDeleteEdges.resize(140,30)
        self.ButtonDeleteEdges.move(self.borderX-150,310)
        self.ButtonDeleteEdges.clicked.connect(self.onActivatedDeleteEdges)
        
        
        #Graph Operations
        self.ButtonWipe = QtGui.QPushButton(self)
        self.ButtonWipe.setText("Wipe")
        self.ButtonWipe.resize(140,30)
        self.ButtonWipe.move(self.borderX-150,350)
        self.ButtonWipe.clicked.connect(self.onActivatedWipe)
        
        
        #Import/Export Operations
        self.ButtonImportData = QtGui.QPushButton(self)
        self.ButtonImportData.setText("Import from GF")
        self.ButtonImportData.resize(140,30)
        self.ButtonImportData.move(self.borderX-150,400)
        self.ButtonImportData.clicked.connect(self.onActivatedImportData)
        
        self.ButtonExportData = QtGui.QPushButton(self)
        self.ButtonExportData.setText("Export to GF")
        self.ButtonExportData.resize(140,30)
        self.ButtonExportData.move(self.borderX-150,430)
        self.ButtonExportData.clicked.connect(self.onActivatedExportData)

        self.loading_errors = list()
        
        #Grid
        self.Grid = QtGui.QCheckBox('Grid', self)
        self.Grid.resize(500,30)
        self.Grid.move(self.borderX-150, 620)
        self.Grid.clicked.connect(self.onActivatedGrid)

        #Picture
        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(0, 0, self.borderX-200, self.borderY-160)
        self.pic.hide()
              
        #Debug
        self.Debug = QtGui.QLineEdit(self)
        self.Debug.move(10,self.borderY-150)
        self.Debug.resize(500,30)
        self.Debug.setStyleSheet("QLineEdit{background-color: rgb(90, 140, 160);}")
        self.Debug.setReadOnly(True)
        
        self.Data = list()
        self.Current = GraphData()
        self.GraphsCount = 0
        self.Selected = list()
        
        self.CurrentIdx = -1
        self.MovingIdx = -1
        self.DeletionIdx = list()
        
        self.gridActive = False
        self.modus = 1
        self.size = 80
        
        self.Window = 0
        
        self.vertex_identifier_in_use = list()
        self.graph_identifier_in_use = list()
        
        #CR
        self.Red = QtGui.QPen(QtGui.QColor(200,0,0))
        self.Green = QtGui.QPen(QtGui.QColor(0,100,0))
        self.Yellow = QtGui.QPen(QtGui.QColor(200,100,0))
        self.SmallFont = QtGui.QFont("Helvetica", 8)
        self.brushCopsOld = QtGui.QBrush(QtGui.QColor(0,200,255))
        self.brushCopsNew = QtGui.QBrush(QtGui.QColor(0,0,120))
        self.brushRobber = QtGui.QBrush(QtGui.QColor(255,0,0))
        self.brushBoth = QtGui.QBrush(QtGui.QColor(255,255,0))
        self.brushCR_normal = QtGui.QBrush(QtGui.QColor(255,255,255))
        self.CopsWonFont = QtGui.QFont("Helvetica", 32)
        self.penCR = QtGui.QPen(QtGui.QColor(0,0,0))
        self.penCR.setWidth(3) 
        
        self.CopsCount = 2
        self.CopsSelectedCount = 0
        
        self.Cops = list()
        self.CopsOld = list()
        self.Vertices = self.Current.G.get_vertices()
        self.Robber = int()
        
        self.CopsWon = False
        self.isMonotone = False
        self.initTurn = True

    def next_vertex_identifier(self):
        i = 1
        while i in self.vertex_identifier_in_use:
            i+=1
        self.vertex_identifier_in_use.append(i)
        return i
        
    def next_graph_identifier(self):
        i = 1
        while ("G"+str(i)) in self.graph_identifier_in_use:
            i+=1
        self.graph_identifier_in_use.append("G"+str(i))
        return ("G"+str(i))
    
    def addGraph_template(self):
        self.onActivatedReset()
        self.Window = 0
        self.RadioSwitch1.setChecked(True)
        G = copy.deepcopy(GraphData())
        G.Name = self.next_graph_identifier()
        self.Data.append(G)
        self.GraphsCount += 1
        self.ComboGraphs.addItem(G.Name)
        self.CurrentIdx = self.GraphsCount-1
        self.ComboGraphs.setCurrentIndex(self.CurrentIdx)
        self.Current = self.Data[self.CurrentIdx]
        self.Debug.setText("added graph [" + G.Name + "]")
        self.repaint()
    
    def addGraph(self, graph):
        try:
            self.GraphsCount += 1
            graph_name = graph.Name
            if graph_name in self.graph_identifier_in_use:
                i = 1
                while (graph_name+"("+str(i)+")") in self.graph_identifier_in_use:
                    i+=i
                graph.Name = graph_name+"("+str(i)+")"
            self.Data.append(graph)
            self.ComboGraphs.addItem(graph.Name)
            self.CurrentIdx = self.GraphsCount-1
            self.ComboGraphs.setCurrentIndex(self.CurrentIdx)
            self.Current = self.Data[self.CurrentIdx]
            self.repaint()
        except:
            self.Debug.setText("[CG.addGraph]: error while loading graph")
        
    def removeGraph(self):
        if self.GraphsCount == 0:
            self.repaint()
            return None
        name = self.Current.Name
        if name == '':
            return None
        self.Data.pop(self.CurrentIdx)
        self.ComboGraphs.removeItem(self.CurrentIdx)
        self.graph_identifier_in_use.pop(self.graph_identifier_in_use.index(name))
        self.GraphsCount -=1
        self.CurrentIdx -=1
        if self.CurrentIdx >= 0:
            self.Current = self.Data[self.CurrentIdx]
            self.ComboGraphs.setCurrentIndex(self.CurrentIdx)
        else:
            self.Current = GraphData()
            self.ComboGraphs.setCurrentIndex(0)
        self.Debug.setText("removed graph [" + name + "]")
        self.onActivatedReset()
        self.repaint()
    
    def onActivatedVertexSize(self, text):
        if(text == "Tiny"):
            self.size = 40
        elif(text == "Small"):
            self.size = 60
        elif(text == "Normal"):
            self.size = 80
        elif(text == "Large"):
            self.size = 100
        elif(text == "Huge"):
            self.size = 120
        self.repaint()
    
    def paintEvent(self, event):
        if self.Window == 0:
            self.ComboCopsCount.hide()
            self.ExecuteButton.hide()
            self.ResetButton.hide()
            self.ComboVertexSize.show()
            self.ButtonCreateVertices.show()
            self.ButtonDeleteVertices.show()
            self.ButtonRelocate.show()
            self.ButtonCreateEdges.show()
            self.ButtonDeleteEdges.show()
            self.ButtonWipe.show()
            self.ButtonImportData.show()
            self.ButtonExportData.show()
            self.Grid.show()

        elif self.Window == 1:
            self.ComboVertexSize.hide()
            self.ButtonCreateVertices.hide()
            self.ButtonDeleteVertices.hide()
            self.ButtonRelocate.hide()
            self.ButtonCreateEdges.hide()
            self.ButtonDeleteEdges.hide()
            self.ButtonWipe.hide()
            self.ButtonImportData.hide()
            self.ButtonExportData.hide()
            self.Grid.hide()
            self.gridActive = False
            self.ExecuteButton.show()
            self.ResetButton.show()
            self.ComboCopsCount.show()
        else:
            self.Grid.hide()
            self.gridActive = False
            self.ComboCopsCount.hide()
            self.ExecuteButton.hide()
            self.ResetButton.hide()
            self.ComboVertexSize.hide()
            self.ButtonCreateVertices.hide()
            self.ButtonDeleteVertices.hide()
            self.ButtonRelocate.hide()
            self.ButtonCreateEdges.hide()
            self.ButtonDeleteEdges.hide()
            self.ButtonWipe.hide()
            self.ButtonImportData.hide()
            self.ButtonExportData.hide()
            
        self.paint_hud()
        if(self.Window in [0,1] and self.GraphsCount != 0 and len(self.Data) != 0):
            self.paint_graph()
            
    def paint_hud(self):
        painter = QtGui.QPainter(self)
        painter.setBrush(self.brush) 
        painter.setFont(self.font)
        self.pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(self.pen)
        #border
        painter.drawLine(0,50,self.borderX-200, 50)
        painter.drawLine(self.borderX-200, 50, self.borderX-200, self.borderY-160)
        painter.drawLine(0, self.borderY-160, self.borderX-200, self.borderY-160)
        painter.setBrush(self.brushBoard)
        painter.drawRect(0,50,self.borderX-200,self.borderY-210)
        painter.setBrush(self.brush)
        
        if self.Window == 0:
            painter.setPen(self.pen) 
            painter.drawText(self.borderX-150, 90, "Vertex Size")
        if self.Window == 1:
            painter.setPen(self.penCR) 
            painter.drawText(self.borderX-150, 90, "Cops Count")
            painter.drawText(self.borderX-180, 300, "Explanation")
            painter.setFont(self.SmallFont)
            
            painter.setBrush(self.brushCopsNew)
            painter.drawEllipse(self.borderX-190, 320,  10, 10)
            painter.drawText(self.borderX-175, 330, "current cops")
            
            painter.setBrush(self.brushCopsOld)
            painter.drawEllipse(self.borderX-190, 340,  10, 10)
            painter.drawText(self.borderX-175, 350, "cops of last round")
            
            painter.setBrush(self.brushRobber)
            painter.drawEllipse(self.borderX-190, 360,  10, 10)
            painter.drawText(self.borderX-175, 370, "the robber")
            
            painter.setBrush(self.brushBoth)
            painter.drawEllipse(self.borderX-190, 380,  10, 10)
            painter.drawText(self.borderX-175, 390, "cop and robber on the same vertex")
            
            if self.CopsWon:
                painter.setPen(self.Green)
                painter.setFont(self.CopsWonFont)
                painter.drawText(self.borderX-800,self.borderY-100, "cops won!")
                painter.setFont(self.font)
            
            painter.setFont(self.SmallFont)
            if not self.initTurn:
                if self.isMonotone:
                    painter.setPen(self.Yellow)
                    painter.drawText(self.borderX-170,650, "monotone move")
                else:
                    painter.setPen(self.Red)
                    painter.drawText(self.borderX-170,650, "non-monotone move")

        if self.Window == 2:
            painter.setPen(self.Red)
            i = 150 
            for s in self.loading_errors:
                painter.drawText(100, i, s)
                i += 20
            
        if(self.gridActive):
            self.pen.setStyle(QtCore.Qt.DotLine)
            #Y
            for i in range(1, ((self.borderX-200)//self.size)+1):
                painter.drawLine(i*self.size, 50, i*self.size, self.borderY-160)
            #X
            for i in range(1, ((self.borderY-210)//self.size)+1):
                painter.drawLine(0, 50+(i*self.size), self.borderX-200, 50+(i*self.size))
            self.pen.setStyle(QtCore.Qt.SolidLine)

    def paint_graph(self):
        painter = QtGui.QPainter(self)
        painter.setBrush(self.brush) 
        painter.setFont(self.font)
        painter.setPen(self.pen) 
        for i in range(0, len(self.Current.edgesData)):
            painter.drawLine(self.Current.edgesData[i][0],
                             self.Current.edgesData[i][1],
                             self.Current.edgesData[i][2],
                             self.Current.edgesData[i][3])
        
        for i in range(0, len(self.Current.verticesData)):
            if str(self.Current.verticesData[i][0]) in self.Selected:
                painter.setBrush(self.brushSelected)
            elif self.Current.verticesData[i][0] in self.Cops and self.Current.verticesData[i][0] != self.Robber:
                painter.setBrush(self.brushCopsNew)
            elif self.Current.verticesData[i][0] in self.CopsOld:
                painter.setBrush(self.brushCopsOld)
            elif self.Current.verticesData[i][0] not in self.Cops and self.Current.verticesData[i][0] == self.Robber:
                painter.setBrush(self.brushRobber)
            elif self.Current.verticesData[i][0] in self.Cops and self.Current.verticesData[i][0] == self.Robber:
                painter.setBrush(self.brushBoth)
            elif self.Window == 1:
                painter.setBrush(self.brushCR_normal)
                
            pos_x = self.Current.verticesData[i][1][0]
            pos_y = self.Current.verticesData[i][1][1]
            ID = str(self.Current.verticesData[i][0])
            svs = self.Current.verticesData[i][2]
            painter.drawEllipse(pos_x-svs/2, pos_y-svs/2, svs, svs)
            painter.drawText(pos_x -((svs/20)*len(ID)), pos_y+(svs/15), ID)
            
            painter.setBrush(self.brush)

    def round_to_grid(self, pos_x, pos_y, offset1, offset2):
        new_pos_x = pos_x-((pos_x-offset1) % self.size)+self.size/2
        new_pos_y = pos_y-((pos_y-offset2) % self.size)+self.size/2
        return (new_pos_x, new_pos_y)
        
    def get_clicked_vertex(self, pos_x, pos_y):
        for i in range(0, len(self.Current.verticesData)):
            v_X = self.Current.verticesData[i][1][0]
            v_Y = self.Current.verticesData[i][1][1]
            svs = self.Current.verticesData[i][2]
            if self.distance(pos_x, pos_y, v_X, v_Y) <= svs/2:
                return i
        return -1
    
    def distance(self, pos1_x, pos1_y, pos2_x, pos2_y):
        return sqrt((abs(pos2_x-pos1_x)**2)+(abs(pos2_y-pos1_y)**2))
    
    def is_overlapping(self, pos_x, pos_y):
        for i in range(0, len(self.Current.verticesData)):
            v_X = self.Current.verticesData[i][1][0]
            v_Y = self.Current.verticesData[i][1][1]
            svs = self.Current.verticesData[i][2]
            if self.distance(pos_x, pos_y, v_X, v_Y) < (svs/2 + self.size/2 + 10):
                return True
        return False
    
    def setCops(self, pos_x, pos_y):
        idx = self.get_clicked_vertex(pos_x, pos_y)
        if idx == -1:
            return None
        name = self.Current.verticesData[idx][0]
        if name in self.Cops:
            self.Cops.pop(self.Cops.index(name))
            self.CopsSelectedCount -= 1
        else:
            if self.CopsSelectedCount < self.CopsCount:
                self.Cops.append(name)
                self.CopsSelectedCount += 1
                
        self.repaint()
        
        
    #Mainloop
    def mousePressEvent(self, event):
        if self.GraphsCount == 0:
            self.Debug.setText("you have to create a graph first")
            self.repaint()
            return None
            
        if self.CopsWon:
            self.Debug.setText("reset game first")
            return None
            
        super(CopsAndRobbers, self).mousePressEvent(event)
        
        #Position
        self.offset = event.pos()
        pos_x = self.offset.x()
        pos_y = self.offset.y()
        
        #Position in Drawing Shape
        if(((self.size/2) >= self.offset.x()) 
         or (self.offset.x() >= self.borderX-200-(self.size/2)) 
         or((self.size/2)+50 >= self.offset.y()) 
         or (self.offset.y() >= self.borderY-160-(self.size/2))):
            return None
            
        if self.Window == 1:
            self.setCops(pos_x, pos_y)
        
        if self.Window == 0:
        
            #create vertices
            if self.modus == 1:
                if self.gridActive:
                    pos_x, pos_y = self.round_to_grid(pos_x, pos_y, 0, 50)
                    
                if self.is_overlapping(pos_x, pos_y):
                    self.Debug.setText("vertex not added: vertex would overlap another vertex")
                    return None
                    
                ID = self.next_vertex_identifier()
                
                pos_x = pos_x
                pos_y = pos_y
                    
                self.Current.verticesData.append([ID, [pos_x, pos_y], self.size])
                self.Current.G.add_vertex(ID)
                self.Debug.setText("added vertex: " + str(ID) + "@["+str(pos_x) +","+str(pos_y)+"]")
                    
                self.lastAction = 1
                
            #delete vertices
            elif self.modus == 2:
                idx = self.get_clicked_vertex(pos_x, pos_y)
                if idx == -1:
                    return None
                
                name = self.Current.verticesData[idx][0]
                to_delete = list()
                
                self.Current.verticesData.pop(idx)
                self.Current.G.remove_vertex(name)
                self.vertex_identifier_in_use.pop(self.vertex_identifier_in_use.index(name))
                
                for i in range(0, len(self.Current.edgesData)):
                    if self.Current.edgesData[i][4] == name or self.Current.edgesData[i][5] == name:
                        to_delete.append(i)
                
                for i in range(0, len(to_delete)):
                    self.Current.edgesData.pop(to_delete[i]-i)
                    
                self.Debug.setText("removed vertex [" + str(name) + "]")    
                
                self.lastAction = 2
            
            #relocating vertices
            elif self.modus == 3:
                idx = self.get_clicked_vertex(pos_x, pos_y)
                if len(self.Selected) == 0:
                    if idx == -1:
                        return None
                    self.Selected.append(str(self.Current.verticesData[idx][0]))
                    self.MovingIdx = idx
                else:
                    if self.is_overlapping(pos_x, pos_y):
                        self.Debug.setText("vertex not moved: vertex would overlap another vertex")
                        self.Selected = list()
                        self.repaint()
                        return None
                    name = self.Selected[0]
                    self.Selected = list()
                    self.Current.verticesData[self.MovingIdx][1][0] = pos_x
                    self.Current.verticesData[self.MovingIdx][1][1] = pos_y
                    for i in range(0, len(self.Current.edgesData)):
                        if str(self.Current.edgesData[i][4]) == name:
                            self.Current.edgesData[i][0] = pos_x
                            self.Current.edgesData[i][1] = pos_y
                        if str(self.Current.edgesData[i][5]) == name:
                            self.Current.edgesData[i][2] = pos_x
                            self.Current.edgesData[i][3] = pos_y

            elif(self.modus == 5): #edge creation
                idx = self.get_clicked_vertex(pos_x, pos_y)
                if idx == -1:
                    return None
                
                ID = str(self.Current.verticesData[idx][0])
                if ID in self.Selected:
                    self.Selected.pop(self.Selected.index(ID))
                else:
                    self.Selected.append(ID)
                
                if len(self.Selected) == 2:
                    idx1 = -1
                    idx2 = -1
                    for i in range(0, len(self.Current.verticesData)):
                        if str(self.Current.verticesData[i][0]) == self.Selected[0]:
                            idx1 = i
                            break
                    for i in range(0, len(self.Current.verticesData)):
                        if str(self.Current.verticesData[i][0]) == self.Selected[1]:
                            idx2 = i
                            break
                            
                    ID_1 = self.Current.verticesData[idx1][0]
                    ID_2 = self.Current.verticesData[idx2][0]
                    pos1_x = self.Current.verticesData[idx1][1][0]
                    pos1_y = self.Current.verticesData[idx1][1][1]
                    pos2_x = self.Current.verticesData[idx2][1][0]
                    pos2_y = self.Current.verticesData[idx2][1][1]
                    svs1 = self.Current.verticesData[idx1][2]
                    svs2 = self.Current.verticesData[idx2][2]
                            
                    tmpEdgeData1 = [pos1_x, pos1_y, pos2_x, pos2_y, ID_1, ID_2]
                                
                    tmpEdgeData2 = [pos2_x, pos2_y, pos1_x, pos1_y, ID_2, ID_1]
                                
                    if tmpEdgeData1 not in self.Current.edgesData and tmpEdgeData2 not in self.Current.edgesData:
                        self.Current.edgesData.append(tmpEdgeData1)
                        self.Current.G.add_edge(ID_1, ID_2)
                        self.Debug.setText("added edge: [" + str(ID_1) + " -- " + str(ID_2) +"]")
                    else:
                        self.Debug.setText("error: edge [" + str(ID_1) + " -- " + str(ID_2) + "] still exists!")
                    
                    self.Selected = list()

            elif(self.modus == 6): #edge deletion
                if len(self.Selected) < 2:
                    idx = self.get_clicked_vertex(pos_x, pos_y)
                    if idx == -1:
                        return None
                    name = str(self.Current.verticesData[idx][0])
                    if name not in self.Selected:
                        self.Selected.append(name)
                    else:
                        self.Selected.pop(self.Selected.index(name))
                        
                if len(self.Selected) == 2:
                    for i in range(0, len(self.Current.edgesData)):
                        if str(self.Current.edgesData[i][4]) in self.Selected and str(self.Current.edgesData[i][5]) in self.Selected:
                            self.DeletionIdx.append(i)
                    if len(self.DeletionIdx) == 0:
                        self.Debug.setText("error: there is no such edge!")
                    else:
                        for i in range(0, len(self.DeletionIdx)):
                            self.Current.edgesData.pop(self.DeletionIdx[i]-i)
                        self.Current.G.remove_edge(int(self.Selected[0]), int(self.Selected[1]))
                        self.Current.G.remove_edge(int(self.Selected[1]), int(self.Selected[0]))
                            
                        self.Debug.setText("removed edge: [" + str(self.Selected[0]) + " -- " + str(self.Selected[1]) + "]")
                
                    self.Selected = list()
                    self.DeletionIdx = list()
                                    
            self.Data[self.CurrentIdx] = copy.deepcopy(self.Current)    
        self.repaint()
    
    """ CR Funcs """
    
    #CR-Game
    def onActivatedExecute(self):
        if len(self.Vertices) == 0:
            return None
        self.initTurn = False
        intersection = SetOp.intersection(self.CopsOld, self.Cops)
        
        tmp1_graph = copy.deepcopy(self.Current.G)
        tmp1_graph.delete_vertices(intersection)
        tmp2_graph = copy.deepcopy(self.Current.G)
        tmp2_graph.delete_vertices(self.CopsOld)
        
        comp_new = tmp1_graph.get_components_DFS()
        comp_old = tmp2_graph.get_components_DFS()

        for i in range(0, len(comp_old)):
            if self.Robber in comp_old[i]:
                comp_old = SetOp.sort(comp_old[i])
                break
                    
        for i in range(0, len(comp_new)):
            if self.Robber in comp_new[i]:
                comp_new = SetOp.sort(comp_new[i])
                if comp_new == comp_old:
                    self.isMonotone = True
                else:
                    self.isMonotone = False
                    
                comp_new = SetOp.difference(comp_new, self.Cops)
                if SetOp.isEmpty(SetOp.difference(comp_new, self.Cops)):
                    self.CopsWon = True
                    self.repaint()
                    return None
                break

        self.CopsOld = copy.deepcopy(self.Cops)
        self.Cops = list()
        self.Robber = comp_new[randint(0, len(comp_new)-1)]
        self.CopsSelectedCount = 0
        self.repaint()
    
    def onActivatedReset(self):
        self.Selected = list()
        self.Cops = list()
        self.CopsOld = list()
        self.CopsWon = False
        if self.Window == 1:
            self.Vertices = self.Current.G.get_vertices()
            if len(self.Vertices) != 0:
                self.Robber = self.Vertices[randint(0, len(self.Vertices)-1)]
            else:
                self.Robber = str()
        else:
            self.Robber = str()
            
        self.initTurn = True
        self.isMonotone = False
        self.CopsSelectedCount = 0
        self.Debug.setText("")
        self.repaint()
    
    def onActivatedCopsCount(self, text):
        cnt = int(text)
        self.CopsCount = cnt
        self.onActivatedReset()
    
    
    """ CG Funcs """
    
    #On-Activation Functions
    def onActivatedCreateVertices(self):
        self.modus = 1
        
    def onActivatedDeleteVertices(self):
        self.modus = 2
        
    def onActivatedRelocate(self):
        self.modus = 3

    def onActivatedCreateEdges(self):
        self.modus = 5
    
    def onActivatedDeleteEdges(self):
        self.modus = 6
        
    def onActivatedWipe(self):
        self.Current.G = Graph.Graph(list())
        self.Current.verticesData = list()
        self.Current.edgesData = list()
        self.Debug.setText("wiped graph [" + self.Current.Name + "]")
        self.modus = 0
        self.vertex_identifier_in_use = list()
        self.repaint()
        
    def onActivatedGrid(self):
        self.gridActive = self.Grid.isChecked()
        self.repaint()

    def onActivatedSelectGraph(self, text):
        for i in range(0, len(self.Data)):
            if self.Data[i].Name == text:
                self.Current = self.Data[i]
                self.CurrentIdx = i
                self.ComboGraphs.setCurrentIndex(i)
        self.Debug.setText("changed to " + text)
        self.onActivatedReset()
        self.repaint()
        
    def onActivatedGroupBoxMode(self):
        if self.RadioSwitch1.isChecked():
            self.Window = 0
            self.pic.hide()
        if self.RadioSwitch2.isChecked():
            self.Window = 1
            self.pic.hide()
        if self.RadioSwitch3.isChecked():
            self.Window = 2

            V_T = list()
            E_T = list()
            try:
                import tdlib
                T, w = tdlib.exact_decomposition_cutset(self.Current.G)
                V_T = T.vertices()
                E_T = T.edges()
            except:
                self.loading_errors.append("unable to load pytdlib, install pytdlib (>=0.8) (included in the tarball of tdlib)")
                self.loading_errors.append("    -> ./configure")
                self.loading_errors.append("    -> make install")
                self.onActivatedReset()
                self.repaint()
                return
            try:
                import pydot
                graph = pydot.Dot(graph_type='graph')
                for bag in V_T:
                    graph.add_node(pydot.Node(str(bag)))

                i = 0
                while i < (len(E_T)-1):
                    graph.add_edge(pydot.Edge(str(V_T[E_T[i]]), str(V_T[E_T[i+1]])))
                    i +=2

                graph.write_png('tmp.png')

            except:
                self.loading_errors.append("unable to plot the treedecomposition")
                self.loading_errors.append("    -> install pydot")
                self.onActivatedReset()
                self.repaint()
                return

            self.pic.setPixmap(QtGui.QPixmap("tmp.png"))
            self.pic.setAlignment(QtCore.Qt.AlignCenter)
            self.pic.show()


        self.onActivatedReset()
        self.repaint()
    
    #Import Functions
    def onActivatedImportData(self, text):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Load graph", "", "Graph File (*.gf)")
        if(filename == ''):
            return True
        fin = open(filename, 'rb')
        if(fin):
            tmp = pickle.load(fin)
            self.addGraph(tmp)             
            self.Debug.setText("loaded " + self.Current.Name + " from " + filename)    
            try:
                self.graph_identifier_in_use.append(tmp.Name)
            except:
                pass
        else:
            self.Debug.setText("error: could not load file!")
            QtGui.QMessageBox.about(self, "Loading Data", "Error! Do you have proper permissions?")
            return False
        self.Debug.setText("loaded data from " + filename)
        QtGui.QMessageBox.about(self, "Loading Data", "Done!")
        self.repaint()
        return True
    
    #Export Functions
    def onActivatedExportData(self):
        if len(self.Data) == 0:
            return True
        name = self.Current.Name
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save graph", name+".gf", "Graph File (*.gf)")
        if filename != "":
            if(".gf" not in filename):
                filename = filename + ".gf"
            fout = open(filename, 'wb')
            if(fout):
                pickle.dump(self.Current, fout)
            else:
                self.Debug.setText("error: could not save graph!")
                QtGui.QMessageBox.about(self, "Saving graph", "Error! Do you have proper permissions?")
                return False
            self.Debug.setText("saved " + self.Current.Name + " to " + filename)
            QtGui.QMessageBox.about(self, "Saving graph", "Done!")
            fout.close()
        return True

signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QtGui.QApplication(sys.argv) 
main = CopsAndRobbers() 
mainColor = QtGui.QPalette()
mainColor.setColor(QtGui.QPalette.Background,QtCore.Qt.lightGray)
main.setPalette(mainColor) 
screen = QtGui.QDesktopWidget().screenGeometry()
main.setFixedSize(screen.width(),screen.height())
main.show()
sys.exit(app.exec_())
