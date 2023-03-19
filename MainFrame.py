import sys


from Game import Game, GameState
from GameCell import GameCell
from Level import Level
from Player import Player
from MainFrameUI import Ui_MainWindow as MainFrameUi

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QStandardItemModel, QColor, QBrush, QPen
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QModelIndex, QRectF, Qt

from State import State


class MainFrame(QMainWindow, MainFrameUi):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.level = Level("Levels/level01.txt")
        self.player = Player(0, 0)
        self.colors = [
            QColor(150, 10, 20),
            QColor(150, 100, 10),
            QColor(0, 128, 0),
            QColor(204, 0, 255),
            QColor(200, 255, 100),
            QColor(25, 50, 200),
            QColor(0, 200, 144),
            QColor(250, 20, 185),
            QColor(150, 100, 100),
        ]
        self._game = Game(len(self.colors))
        self.new_game()
        self.game_resize(self._game)
        self.msg = QMessageBox()

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.gameFieldTableView.setItemDelegate(MyDelegate(self))
        self.restartButton.clicked.connect(lambda: self.new_game())
        self.exitAction.triggered.connect(lambda: sys.exit())
        self.restartAction.triggered.connect(lambda: self.new_game())
        self.actionLevel_1.triggered.connect(lambda: self.change_level("Levels/level01.txt"))
        self.actionLevel_2.triggered.connect(lambda: self.change_level("Levels/level02.txt"))
        self.actionLevel_3.triggered.connect(lambda: self.change_level("Levels/level03.txt"))
        self.actionLevel_4.triggered.connect(lambda: self.change_level("Levels/level04.txt"))
        self.actionLevel_5.triggered.connect(lambda: self.change_level("Levels/level05.txt"))
        self.ruleAction.triggered.connect(lambda: self.print_mes("r"))
        self.infoAction.triggered.connect(lambda: self.print_mes("i"))
        self.gameFieldTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.gameFieldTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.gameFieldTableView.setFocusPolicy(Qt.NoFocus)
        self.gameFieldTableView.setSelectionMode(QAbstractItemView.NoSelection)

    def new_game(self):
        self._game.new_game(self.level, self.player)
        self.label.setText("Игра в процессе")
        self.game_resize(self._game)
        self.update_view()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        cell = self._game.get_cell(e.row(), e.column())
        if cell is None:
            cell = GameCell(State.VOID, -1)
        color = QColor(192, 192, 192)
        if cell.get_state() == State.VOID or cell.get_state() is None:
            color = QColor(255, 255, 255)
        if cell.get_state() == State.WALL:
            color = QColor(128, 128, 128)
        if cell.get_state() == State.CUBE:
            color = self.colors[cell.get_color()]
        if cell.get_state() == State.PLAYER:
            color = QColor(0, 0, 0)
            painter.setBrush(QBrush(color, Qt.SolidPattern))
            painter.drawEllipse(QRectF(option.rect))
            return
        painter.setPen(QPen(color, 5, Qt.SolidLine))
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        painter.drawRect(QRectF(option.rect))

    def update_view(self):
        self.gameFieldTableView.viewport().update()
        if self._game.get_state() == GameState.PLAYING:
            self.label.setText("Игра идет")
            self.label.setStyleSheet("background-color: blue; border: 1px solid black;")
        else:
            self.label.setText("")
            if self._game.get_state() == GameState.WIN:
                self.label.setText("Уровень пройден")
                self.label.setStyleSheet("background-color: green; border: 1px solid black;")

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.get_row_count(), game.get_col_count())
        self.gameFieldTableView.setModel(model)
        self.update_view()

    def keyPressEvent(self, e) -> None:
        player_pos_x = self.player.get_x_pos()
        player_pos_y = self.player.get_y_pos()

        if e.key() == Qt.Key_A:
            self._game.left_move(player_pos_x, player_pos_y, self.player)
        if e.key() == Qt.Key_W:
            self._game.up_move(player_pos_x, player_pos_y, self.player)
        if e.key() == Qt.Key_D:
            self._game.right_move(player_pos_x, player_pos_y, self.player)
        if e.key() == Qt.Key_S:
            self._game.down_move(player_pos_x, player_pos_y, self.player)
        self.update_view()

    def change_level(self, level_name: str):
        self.level.set_level_file_name(level_name)
        self.new_game()

    def print_mes(self, ch: str):
        self.msg.setInformativeText("")
        if ch == "i":
            self.msg.setWindowTitle("О программе")
            self.msg.setInformativeText("""Игра "Кубикон"\nАвтор: Шестопалов Д.А.""")
        if ch == "r":
            self.msg.setWindowTitle("Правила")
            self.msg.setInformativeText("В игре присутствуют группы разноцветных кубиков,"
                                                        " а от игрока требуеться собрать каждую группу в одну линию. ")
        self.msg.exec()

    '''def resizeEvent(self, event):
        width = self.size().width()
        height = self.size().height()

        koefW = width / self.w
        koefH = height / self.h

        self.verticalLayout.setGeometry(20, 20,100,100)
        self.horizontalLayout.setGeometry(20, 20,100,100)
        self.gameFieldTableView.setGeometry(20, 20,100,100)'''
