# -*- coding: utf-8 -*-
import os
from maya import cmds
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

# designer.exeで作ったUIファイルを取得する
CURRENT_FILE = os.path.normpath(__file__)
path, ext = os.path.splitext(CURRENT_FILE)
UI_FILE = path + ".ui"
OPTVAR_NAME = "SimpleRenamerUI"

class SimpleRenamerWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(SimpleRenamerWindow, self).__init__(*args, **kwargs)

        # 作ったUIファイルをロードして変数に入れる
        self.UI = QUiLoader().load(UI_FILE)
        self.setWindowTitle(self.UI.windowTitle())

        # QMainWindowの中央のウィジェットに入れる
        self.setCentralWidget(self.UI)

        # ボタンとのコネクションを作る
        self.UI.pb_exexute.clicked.connect(self.__do_rename)
        
        # 一の復元
        if cmds.optionVar( exists=OPTVAR_NAME):
            self.setGeometry(
                    *cmds.optionVar( query=OPTVAR_NAME)
                )
        return

    def __do_rename(self): # リネームする
        nodes = cmds.ls(sl=True)
        txt = self.UI.le_text.text()
        if nodes and txt :
            cmds.rename(nodes[0], txt)
        return
    
    def __save_optionVar(self):
        x, y, w, h = self.geometry().getRect()
        cmds.optionVar( intValue4=[OPTVAR_NAME, x, y, w, h])
        return

    def closeEvent(self, event):
        self.__save_optionVar()
        return