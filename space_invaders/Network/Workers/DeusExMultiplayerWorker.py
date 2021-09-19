import copy
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Entities.Box import Box
from Entities.Bullet import Bullet
from Entities.Spaceship import Spaceship
from Factories.BulletFactory import BulletFactory
from Handlers.CollisionHandler import CollisionHandler
import multiprocessing as mp
from queue import  Queue



class DeusExMultiplayerWorkerThread(QThread):
    show_random_force = pyqtSignal(Box)

    def __init__(self, screen: QWidget, queue: Queue):
        super().__init__()
        self.screen = screen
        self.queue = queue


        self.box = Box(self.screen, "box_id", 350, 350, "../Sources/Images/Other/box.png", 35, 35, "player_id")
        self.box.isHidden = True
        self.box.hide()



    def run(self):

        #self.pipe.send('go')
        while True:

            luckyFactor, x, y = self.queue.get()

            #print("wrk lst rcv {0}".format(x))
            if str(x).lstrip('-').isdigit() and str(y).lstrip('-').isdigit() and str(luckyFactor).lstrip('-').isdigit():
                # notify all
                # in this case: update all listeners
                self.box.x = x
                self.box.y = y
                self.box.luckyFactor = luckyFactor

                print(self.box.luckyFactor)

                self.box.move(0, 0)
                self.box.show()
                self.show_random_force.emit(self.box)
                time.sleep(5)
                self.box.hide()
                self.box.isHidden = True
            if x == 'end':
                # notify all
                # in this case: kill the thread
                #self.finished.emit()
                break
