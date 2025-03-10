import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class CardScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.card = None
        self.second_card = None
        self.setSceneRect(0, 0, 400, 300)  
        self.setup_scene()
        
    def setup_scene(self):
        pixmap = QPixmap("carte.png")
        scaled_pixmap = pixmap.scaled(80, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        self.card = self.addPixmap(scaled_pixmap)
        self.card.setPos(50, 50)  
            
    def mousePressEvent(self, event):
        if self.card:
            pos = event.scenePos()
            self.card.setPos(pos.x() - self.card.pixmap().width()/2,
                           pos.y() - self.card.pixmap().height()/2)
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C and not self.second_card:
            pixmap = QPixmap("carte.png")
            scaled_pixmap = pixmap.scaled(80, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
            self.second_card = self.addPixmap(scaled_pixmap)
            self.second_card.setPos(150, 50)  
        elif event.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down] and self.second_card:
            dx = 0
            dy = 0
            if event.key() == Qt.Key_Left:
                dx = -5  
            elif event.key() == Qt.Key_Right:
                dx = 5
            elif event.key() == Qt.Key_Up:
                dy = -5
            elif event.key() == Qt.Key_Down:
                dy = 5
                
            pos = self.second_card.pos()
            self.second_card.setPos(pos.x() + dx, pos.y() + dy)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu de Cartes")
        
        self.scene = CardScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_card)
        self.animation_active = False
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            if self.animation_active:
                self.timer.stop()
            else:
                self.timer.start(100)  
            self.animation_active = not self.animation_active
        else:
            self.scene.keyPressEvent(event)
            
    def animate_card(self):
        if self.scene.card:
            pos = self.scene.card.pos()
            self.scene.card.setPos(pos.x() + 1, pos.y())  
            
            if pos.x() > self.scene.width():
                self.scene.card.setPos(0, pos.y())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)  
    window.show()
    sys.exit(app.exec_())
