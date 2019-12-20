import json
import sys
import random
from time import sleep
from customGUI import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GlobalVariables: 
    def __init__(self):
        self._dict_eng = dict(  # usage: self._global_variables.default_dict.get('
            yes = 'Yes',
            no = 'No',
            instance = 'Instance ',
            file = 'File',
            open = 'Open Project...',
            close_project = 'Close Project',
            export_instance_as_png = 'Export instance as PNG',
            instructions = 'Instructions',
            show_instructions = 'Show instructions',
            about = 'About',
            show_about = 'Show about',
            save_file = 'Save File',
            open_project = 'Open Project',
            options = 'Options',
            additional_options_of_the_instance = 'Additional options',
            update_the_output = 'Update the output',
            confirm_your_choice = 'Confirm Your choice',
            are_you_sure_you_want_to_delete = 'Are you sure you want to delete all instances?',
            add_a_new_instance_menu = 'Add a new instance menu',
            delete_all_instances = 'Delete all instances',
            hide_current_instance = 'Hide current instance',
            confirm_exit = 'Confirm exit',
            are_you_sure_you_want_to_exit = 'Are you sure you want to exit?',
            about_window_title = 'About',
            about_window_creators_name = 'Pavlov Alex',
            about_window_creators_github = 'https://github.com/alexLAP7'
        )
        self._dict_rus = dict(
            yes = 'Да',
            no = 'Нет',
            instance = 'Экземпляр объекта ',
            file = 'Файл',
            open = 'Открыть проект...',
            close_project = 'Закрыть проект',
            export_instance_as_png = 'Экспортировать как PNG',
            instructions = 'Инструкции',
            show_instructions = 'Показать инструкции',
            about = 'Об авторе',
            show_about = 'Показать информацию об авторе',
            save_file = 'Сохранить файл',
            open_project = 'Открыть проект',
            options = 'Настройки',
            additional_options_of_the_instance = 'Дополнительные настройки',
            update_the_output = 'Обновить отображение',
            confirm_your_choice = 'Подтвердите свой выбор',
            are_you_sure_you_want_to_delete = 'Вы уверены, что хотите удалить все объекты?',
            add_a_new_instance_menu = 'Добавить меню для нового экземпляра объекта',
            delete_all_instances = 'Удалить все экземпляры объектов',
            hide_current_instance = 'Скрыть данный экземпляр объекта',
            confirm_exit = 'Подтвердите выход',
            are_you_sure_you_want_to_exit = 'Вы уверены, что хотите выйти?',
            about_window_title = 'Об авторе',
            about_window_creators_name = 'Павлов Александр',
            about_window_creators_github = 'https://github.com/alexLAP7'
        )
        self.default_dict = self._dict_rus


class MenuInstance:
    def __init__(self):
        self._global_variables = GlobalVariables()
        self.id_of_instance = 0  # without id you couldn't get proper instance by call from another class
        self.name = self._global_variables.default_dict.get('instance')  # name of the instance
        self.V = 0 # deadline float
        self.N = 0 # number of items, just the length of the list int
        self.I = [] # list of important indexes
        self.U = 0 # time of start float
        self.T = [] # list of times
    

class GrowingTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.heightMin = 40
        self.heightMax = 40

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)
        if len(self.document().toPlainText()) > 200:  # 200 is number of chars
            self.textCursor().deletePreviousChar()


class CollapsibleBox(QtWidgets.QWidget):  # dynamically expandable box of gui elements
    def __init__(self, title="", parent=None):

        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

    @QtCore.pyqtSlot()
    def on_pressed(self):

        sleep(0.25)  # slows down so it won't lag because of users spam
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):

        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(300)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(300)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class Connector:
    def __init__(self):
        self._global_variables = GlobalVariables()
        self.list_of_widgets = []
        self.list_of_menu_instances = []
        self.number_of_menu_instances = 0
        self.current_widget_to_export = None


class InstructionWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(InstructionWindow, self).__init__(parent)
        self._global_variables = GlobalVariables()
        self.init_layout()

    def init_layout(self):
        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        w.setLayout(layout)
        
        self.title = self._global_variables.default_dict.get('instructions') 
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)  
        self.setGeometry(self.left, self.top, self.windowWidth, self.windowHeight) 

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        layout.addWidget(scroll)
        scrollContents = QtWidgets.QWidget()
        scroll.setWidget(scrollContents)
        text_layout = QtWidgets.QVBoxLayout(scrollContents)
        # font = QtGui.QFont()
        # font.setPointSize(11)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_text = QLabel()
        label_text.setText("Text")
        vbox.addWidget(label_text)

        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                QtWidgets.QSizePolicy.Expanding)
        vbox.addItem(verticalSpacer)
        text_layout.addWidget(frame)


class AboutWindow(QtWidgets.QMainWindow):  # have to change but it works for now
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self._global_variables = GlobalVariables()
        self.title = self._global_variables.default_dict.get('about_window_title') 
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)  
        self.setGeometry(self.left, self.top, self.windowWidth, self.windowHeight) 

        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        w.setLayout(layout)
        
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_creator_name = QLabel()
        creator_name = self._global_variables.default_dict.get('about_window_creators_name') 
        label_creator_name.setText(creator_name)
        vbox.addWidget(label_creator_name)
        
        label_creator_github = QLabel()
        creator_github = self._global_variables.default_dict.get('about_window_creators_github') 
        label_creator_github.setText(creator_github)
        vbox.addWidget(label_creator_github)
        
        vbox.setAlignment(Qt.AlignCenter)
        layout.addWidget(frame)


class Application(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._global_variables = GlobalVariables()
        self.title = 'Application'
        self.setWindowTitle(self.title)
        self.connector = None
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        self.instruction_window = InstructionWindow()
        self.about_window = AboutWindow()

        self.showMaximized()
        self.mainMenu = QMenuBar(self)
        self.setMenuBar(self.mainMenu)
        
        self.set_a_project()
        
        menu_file = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('file'))
        
        file_action_export_as_png = menu_file.addAction(
            self._global_variables.default_dict.get('export_instance_as_png'))
        file_action_export_as_png.triggered.connect(self.export_instance_as_png)
        
        file_action_close = menu_file.addAction(
            self._global_variables.default_dict.get('close_project'))
        file_action_close.triggered.connect(self.close_application)

        menu_instructions = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('instructions'))
        instructions_action_show = menu_instructions.addAction(
            self._global_variables.default_dict.get('show_instructions'))
        instructions_action_show.triggered.connect(self.show_instructions)

        menu_about = self.mainMenu.addMenu(
            self._global_variables.default_dict.get('about'))
        about_action_show = menu_about.addAction(
            self._global_variables.default_dict.get('show_about'))
        about_action_show.triggered.connect(self.show_about)

    def export_instance_as_png(self):
        try:
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                        self._global_variables.default_dict.get(
                                                            'save_file'),
                                                         '.png', "Image (*.png *.jpg *.tif)")
            if name:
                img = self.connector.current_widget_to_export.grab()
                img.save(name)
        except:
            print('Oops! An Error: There is a problem with a file, which you have tried to save.')

    def show_instructions(self):
        self.instruction_window.show()

    def show_about(self):
        self.about_window.show()

    def open_file_dialog(self):
        try:
            self.set_a_project()
            
            # filename, _ = QFileDialog.getOpenFileName(self,
            #                                            self._global_variables.default_dict.get(
            #                                                'open_project'),
            #                                            'c:\\',
            #                                             "Excel Files (*.xls *.xml *.xlsx *.xlsm)",
            #                                           options=QFileDialog.DontUseNativeDialog)
            # if (filename):
            #     # self.close_a_project()  # close all active subwindows and dockable windows
            #     self.set_a_project(filename)
        except:
            print('Oops! An Error: There is a problem with a file, which you have tried to open.\n'
                  ' Make sure, it has the right extension')

    def close_a_project(self):
        try:
            self.close_application()
        except:
            pass

    def set_options_dock(self):  
        self.dockWidget = QDockWidget(self._global_variables.default_dict.get('options'), self)
        self.connector.list_of_widgets.append(self.dockWidget)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                    QtWidgets.QDockWidget.DockWidgetMovable)
        widget = QWidget(self.dockWidget)
        qvbox_layout = QVBoxLayout(widget)
        qvbox_layout.setSpacing(1)
        qvbox_layout.setContentsMargins(2, 2, 2, 2)
        widget.setLayout(qvbox_layout)

        button = QPushButton()
        button_update_the_output = QPushButton()
        button_update_the_output.setText(self._global_variables.default_dict.get('update_the_output'))
        button_update_the_output.setStyleSheet('QPushButton {background-color:rgb(170, 255, 0); color: black;}')
        qvbox_layout.addWidget(button_update_the_output)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        qvbox_layout.addWidget(scroll)
        scrollContents = QtWidgets.QWidget()
        scroll.setWidget(scrollContents)

        self.QVBox_layout_of_dock_options = QtWidgets.QVBoxLayout(scrollContents)
        font = QtGui.QFont()
        font.setPointSize(11)

        def button_update_the_output_clicked(arg):
            self.clear_textedit()            

        button_update_the_output.clicked.connect(button_update_the_output_clicked)

        def button_add_a_new_instance_menu_new_clicked(arg):
            self.set_option_fields()

        def button_delete_all_clicked(arg):
            msg = QMessageBox()
            msg.setWindowTitle(self._global_variables.default_dict.get('confirm_your_choice'))
            msg.setText(self._global_variables.default_dict.get('are_you_sure_you_want_to_delete'))
            okButton = msg.addButton(self._global_variables.default_dict.get('yes'),
                                      QMessageBox.AcceptRole)
            msg.addButton(self._global_variables.default_dict.get('no'), QMessageBox.RejectRole)
            msg.exec()
            if msg.clickedButton() == okButton:
                self.connector.list_of_menu_instances.clear()
                self.connector.number_of_menu_instances = 0
                self.connector.current_widget_to_export = None
                self.statusBar().showMessage("")
                self.dockWidget.close()
                self.set_options_dock()
            else:
                pass

        button_add_a_new_instance_menu = QPushButton()
        button_add_a_new_instance_menu.setText(self._global_variables.default_dict.get('add_a_new_instance_menu'))
        button_add_a_new_instance_menu.clicked.connect(button_add_a_new_instance_menu_new_clicked)
        qvbox_layout.addWidget(button_add_a_new_instance_menu)

        button_delete_all = QPushButton()
        button_delete_all.setText(self._global_variables.default_dict.get('delete_all_instances'))
        button_delete_all.clicked.connect(button_delete_all_clicked)
        qvbox_layout.addWidget(button_delete_all)

        self.dockWidget.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

    def set_option_fields(self):

        instance_menu = MenuInstance()
        instance_menu.id_of_instance = self.connector.number_of_menu_instances
        self.connector.number_of_menu_instances = \
            self.connector.number_of_menu_instances + 1
        self.connector.list_of_menu_instances.append(instance_menu)

        MinimumWidth = 100
        MaximumWidth = 150   

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)

        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)
        name = GrowingTextEdit()
        name.setText(instance_menu.name + str(self.connector.number_of_menu_instances))
        self.connector.list_of_menu_instances[instance_menu.id_of_instance].name = name.toPlainText()
        name.setMinimumHeight(27)
        name.setMaximumHeight(27)

        def name_changed():  
            try:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].name = name.toPlainText()
            except:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].name = 'Incorrect symbols in name'

        name.textChanged.connect(name_changed)

        # def create_schedule():
        #     N = 5 # N is int number of items, just the length of the list
        #     V = 4 # V is float deadline, items with important indexes must be processed by this value of time
        #     K, L = 2, 4 # K and L are two important indexes
        #     I = [K, L] # list of important indexes
        #     U = 0 # the time of the float start
            
        #     T = [  # list_of_lists_with_times
        #         [2, 2, 1, 1, 1],
        #         [1, 1, .5, .5, .5], # this one is the best out of all given samples
        #         [2, 2, 4, 4, 4],
        #         [1, 1, 1, .5, .5],
        #         [1, 2, 2, 2, 2]    
        #     ]
            
        #     data_to_dump = {
        #         'N': N,
        #         'V': V,
        #         'I': tuple([K, L]),
        #         'U': U,
        #         'T': tuple(T)
        #     }
        #     schedule = OptimizedSchedule()
        #     schedule.init(data_to_dump)

        def get_values_to_make_schedule():
            data_to_return = {
                'N': self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].N,
                'V': self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].V,
                'I': tuple(
                    self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].I
                    ),
                'U': self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].U,
                'T': tuple(
                    self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].T
                )
            }
            return data_to_return 

        def print_all_values():
            schedule = OptimizedSchedule()
            schedule.init(get_values_to_make_schedule())
            self.text_edit.append(str(schedule))

        def print_list(_list: list):
            try:
                self.text_edit.append(str(_list))
            except:
                pass
            

        # def print_list(list_of_frequency: list, number_of_elements: int):
        #     self.text_edit.clear()
        #     if list_of_frequency:
        #         for i, v in enumerate(list_of_frequency):
        #             if i < number_of_elements:
        #                 try:
        #                     self.text_edit.append(
        #                         self._global_variables.default_dict.get('value') + str(v[0]) + ', ' +
        #                         self._global_variables.default_dict.get('frequency') + str(v[1]))
        #                     # self.text_edit.append(
        #                     #     self._global_variables.default_dict.get('value') + str(v[0]) + ', ' +
        #                     #     self._global_variables.default_dict.get('frequency') + str(v[1]))
        #                 except:
        #                     pass

        button_pretty_print_to_text_edit = QPushButton()
        button_pretty_print_to_text_edit.setText("")
            # self._global_variables.default_dict.get('pretty_print_tree_to_text_edit'))
        def button_pretty_print_to_text_edit_clicked(arg):
            print_all_values()
        button_pretty_print_to_text_edit.clicked.connect(button_pretty_print_to_text_edit_clicked)

        empty_label_N = QLabel('N:')
        vbox.addWidget(empty_label_N)

        def set_number_of_elements_N():
            spinBox_N.setMaximum(100)
            if spinBox_N.value() <= spinBox_N.value():
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].N = int(
                        str(spinBox_N.value()))

        spinBox_N = QSpinBox()
        spinBox_N.valueChanged.connect(set_number_of_elements_N)
        vbox.addWidget(spinBox_N)
        
        empty_label_0 = QLabel('')
        vbox.addWidget(empty_label_0)
        
        empty_label_V = QLabel('V:')
        vbox.addWidget(empty_label_V)
        
        def set_number_of_elements_V():
            spinBox_V.setMaximum(100)
            if spinBox_V.value() <= spinBox_V.value():
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].V = float(
                        str(spinBox_V.value()))

        spinBox_V = QDoubleSpinBox()
        spinBox_V.valueChanged.connect(set_number_of_elements_V)
        vbox.addWidget(spinBox_V)

        empty_label_1 = QLabel('')
        vbox.addWidget(empty_label_1)

        empty_label_U = QLabel('U:')
        vbox.addWidget(empty_label_U)

        def set_number_of_elements_U():
            spinBox_U.setMaximum(100)
            if spinBox_U.value() <= spinBox_U.value():
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].U = float(
                        str(spinBox_U.value()))

        spinBox_U = QDoubleSpinBox()
        spinBox_U.valueChanged.connect(set_number_of_elements_U)
        vbox.addWidget(spinBox_U)

        empty_label_2 = QLabel('')
        vbox.addWidget(empty_label_2)

        empty_label_I = QLabel('I:')
        vbox.addWidget(empty_label_I)

        list_I = GrowingTextEdit()
        list_I.setText("")
        list_I.setMinimumHeight(100)
        list_I.setMaximumHeight(100)

        def list_I_changed():  # maybe there are no any possible mistakes but I'll use try/except anyways
            try:
                _list = [x.split(' ') for x in list_I.toPlainText().split('\n')]
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].I = [[float(j) for j in i] for i in _list]
                    # instance_menu.id_of_instance].I = [[float(y) for y in x.split(' ')] for x in list_I.toPlainText().split('\n')]
                    # instance_menu.id_of_instance].I = [x.split(' ') for x in list_I.toPlainText().split('\n')]
            except:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].I = []  # 'Incorrect symbols in list'

        list_I.textChanged.connect(list_I_changed)
        vbox.addWidget(list_I)

        empty_label_3 = QLabel('')
        vbox.addWidget(empty_label_3)

        empty_label_T = QLabel('T:')
        vbox.addWidget(empty_label_T)

        list_T = GrowingTextEdit()
        list_T.setText("")
        list_T.setMinimumHeight(100)
        list_T.setMaximumHeight(100)

        def list_T_changed():  # maybe there are no any possible mistakes but I'll use try/except anyways
            try:
                _list = [x.split(' ') for x in list_T.toPlainText().split('\n')]
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].T = [[float(j) for j in i] for i in _list]
                    # instance_menu.id_of_instance].T = [[float(y) for y in x.split(' ')] for x in list_T.toPlainText().split('\n')]
                    # instance_menu.id_of_instance].T = [x.split(' ') for x in list_T.toPlainText().split('\n')]
            except:
                self.connector.list_of_menu_instances[
                    instance_menu.id_of_instance].T = []  # 'Incorrect symbols in list'

        list_T.textChanged.connect(list_T_changed)
        vbox.addWidget(list_T)

        empty_label_4 = QLabel('')
        vbox.addWidget(empty_label_4)

        empty_label_5 = QLabel('')
        vbox.addWidget(empty_label_5)

        button_import_tree = QPushButton()
        button_import_tree.setText('import')
            # self._global_variables.default_dict.get('import_tree'))
        def button_import_tree_clicked(arg):
            try:
                filename, _ = QFileDialog.getOpenFileName(self,
                                                           self._global_variables.default_dict.get(
                                                               'open_project'),'',
                                                            "Json Files (*.json)",
                                                          options=QFileDialog.DontUseNativeDialog)
                if (filename):
                    sm = ScheduleManager()
                    schedule = sm.read_data_from_json(filename)
                    self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].T = schedule.list_of_lists_of_times
                    self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].V = schedule.deadline
                    self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].I = schedule.list_of_important_indexes
                    self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].U = schedule.time_of_the_start
                    self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].N = schedule.valid_length_of_list
                    update_gui_elements()
            except:
                print('Oops! An Error: There is a problem with a file, which you have tried to open.\n'
                    ' Make sure, it has the right extension')
            print_all_values()
        button_import_tree.clicked.connect(button_import_tree_clicked)
        vbox.addWidget(button_import_tree)

        button_export_tree_as_list = QPushButton()
        button_export_tree_as_list.setText('export_tree_as_list')
            # self._global_variables.default_dict.get('export_tree_as_list'))
        def button_export_tree_as_list_clicked(arg):
            try:
                name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                            self._global_variables.default_dict.get(
                                                                'save_file'),
                                                                '.json','Json Files (*.json)')
                if name:
                    sm = ScheduleManager()
                    schedule = OptimizedSchedule()
                    schedule.init(get_values_to_make_schedule())
                    sm.write_data_to_json(name, schedule)
                print_all_values()
            except:
                print('Oops! An Error: There is a problem with a file, which you have tried to save.')
            
        button_export_tree_as_list.clicked.connect(button_export_tree_as_list_clicked)
        vbox.addWidget(button_export_tree_as_list)

        content = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(content)
        box = CollapsibleBox(self._global_variables.default_dict.get('additional_options_of_the_instance'))
        
        vlay.addWidget(name)
        vlay.addWidget(button_pretty_print_to_text_edit)
        vlay.addWidget(box)
        
        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        vlay.addItem(verticalSpacer)    
        
        box.setContentLayout(vbox)
        vlay.addStretch()
        
        def update_gui_elements():
            list_T.setText(
                '\n'.join(' '.join(map(str,sl)) for sl in self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].T))
            list_I.setText(
                ' '.join(map(str, self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].I)))
            spinBox_U.setValue(float(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].U))
            spinBox_V.setValue(float(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].V))
            spinBox_N.setValue(int(self.connector.list_of_menu_instances[
                        instance_menu.id_of_instance].N))
        
        frame_ = QtWidgets.QFrame()
        frame_.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        
        frame_.setLayout(vlay)
        self.QVBox_layout_of_dock_options.addWidget(frame_)

    def set_a_project(self):        
        if self.connector is None:  # we init only one table with a plot for a one project
            self.connector = Connector()
            self.connector.current_widget_to_export = self.text_edit
            self.set_options_dock()
        
    def clear_textedit(self):
        self.text_edit.clear()
        # self.text_edit.setText('hey it works')
        # print('hey it works')

    def close_application(self):
        msg = QMessageBox()
        msg.setWindowTitle(self._global_variables.default_dict.get('confirm_exit'))
        msg.setText(self._global_variables.default_dict.get('are_you_sure_you_want_to_exit'))
        okButton = msg.addButton(self._global_variables.default_dict.get('yes'),
                                  QMessageBox.AcceptRole)
        msg.addButton(self._global_variables.default_dict.get('no'), QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() == okButton:
            sys.exit()            
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.close_application()


class FileHandler():
    def __init__(self):
        super().__init__() 
    
    def print_data(self, data: dict):
        for k, v in data.items():
                    print('{}: {}'.format(k, v))
    
    def write_json_file(self, path: str, data: dict, indent=4):
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=indent)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
            
    def write_json_file_wo_indent(self, path: str, data: dict):
        try:
            with open(path, 'w') as f:
                json.dump(data, f)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
    
    def write_list_to_file(self, path: str, best_list: list, list_of_valid_lists=[]):
        try:
            if best_list:
                with open(path, 'w', encoding="utf-8") as f:
                    f.write("{}\n".format('The best list:'))
                    for item in best_list:
                        f.write("{}\n".format(item))
                    
                    if list_of_valid_lists:
                        f.write("\n\n{}\n".format('All valid lists:'))
                        for item in list_of_valid_lists:
                            f.write("{}\n".format(item))
            else:
                with open(path, 'w', encoding="utf-8") as f:
                    f.write("{}".format('[]'))
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
    
    def read_json_file(self, path: str):
        try:
            with open(path) as f:
                data = json.load(f)
            return data
        except:
            print("Error: cannot read the data from the file with this path:")
            print("Path: " + str(path))
        return None
             

class OptimizedSchedule():
    def __init__(self):
        super().__init__() 
        self.list_of_lists_of_times = None # T
        self.deadline = None # V
        self.list_of_important_indexes = None # I
        self.time_of_the_start = None # U
        self.valid_length_of_list = None # N
 
    def init(self, data: dict):
        self.list_of_lists_of_times = data['T'] # list_of_lists_of_times
        self.deadline = data['V'] # deadline
        self.list_of_important_indexes = data['I'] # list_of_important_indexes
        self.time_of_the_start = data['U'] # time_of_the_start
        self.valid_length_of_list = data['N'] # valid_length_of_list
 
    def __repr__(self):
        return "\n" + \
            "%r\n%r\n%r\n%r\n%r\n" % (
                self.valid_length_of_list,
                self.deadline,
                self.list_of_important_indexes,
                self.time_of_the_start,
                self.list_of_lists_of_times)
 
    def find_the_best_list(self):
        list_of_valid_lists_of_times = self._validate_each_list_of_times()
        if list_of_valid_lists_of_times:
            list_of_sum = []
            for i, v in enumerate(list_of_valid_lists_of_times):
                list_of_sum.append(sum(range(len(v))))
            index_of_the_best_list = list_of_sum.index(min(list_of_sum))
            return list_of_valid_lists_of_times[index_of_the_best_list]
        return None
        
    def find_all_valid_lists(self):
        list_of_valid_lists_of_times = self._validate_each_list_of_times()
        return list_of_valid_lists_of_times
    
    def _validate_each_list_of_times(self):
        raw_list_of_valid_lists_of_times = []
        for i, list_of_times in enumerate(self.list_of_lists_of_times):
            raw_list_of_valid_lists_of_times.append(self._check_validation(list_of_times))
        list_of_valid_lists_of_times = [i for i in raw_list_of_valid_lists_of_times if i]
        return list_of_valid_lists_of_times
        
    def _check_validation(self, list_of_times: list):
        _sum = self.time_of_the_start
        try:
            if len(list_of_times) == self.valid_length_of_list:
                if self.list_of_important_indexes:  
                    for i in range(0, max(self.list_of_important_indexes)):
                        _sum += list_of_times[i]
                else:  # if list_of_important_indexes is empty then we compare sum of all elements with the deadline 
                    for i in range(0, len(list_of_times)):
                        _sum += list_of_times[i]
                if self.deadline > _sum:
                    return list_of_times
        except:
            print('Error: Input is not correct.')
        return None
        
            
class ScheduleManager():
    def __init__(self):
        super().__init__() 
        self.file_handler = FileHandler()
    
    def set_schedule_by_raw_data(self, data: dict):
        schedule = OptimizedSchedule()
        schedule.list_of_lists_of_times = data['T'] # list_of_lists_of_times
        schedule.deadline = data['V'] # deadline
        schedule.list_of_important_indexes = data['I'] # list_of_important_indexes
        schedule.time_of_the_start = data['U'] # time_of_the_start
        schedule.valid_length_of_list = data['N'] # valid_length_of_list
        return schedule
    
    def _dump(self, schedule: OptimizedSchedule):
        data = {
            'T': tuple(schedule.list_of_lists_of_times),
            'V': schedule.deadline,
            'I': tuple(schedule.list_of_important_indexes),
            'U': schedule.time_of_the_start,
            'N': schedule.valid_length_of_list
        }
        return data
    
    def write_the_best_list_to_file(self, path: str, schedule: OptimizedSchedule):
        try:
            data = self._dump(schedule)
            the_best_list = schedule.find_the_best_list()
            list_of_valid_lists = schedule.find_all_valid_lists()
            self.file_handler.write_list_to_file(path, the_best_list, list_of_valid_lists)
        except:
            print('Error: Could not find the best list.')
        return None
    
    def write_data_to_json(self, path: str, schedule: OptimizedSchedule):
        try:
            data = self._dump(schedule)
            self.file_handler.write_json_file(path, data)
        except:
            print('Error: Cannot write the data to the file.')
        return None
    
    def read_data_from_json(self, path: str):
        try:
            raw_data = self.file_handler.read_json_file(path)
            return self.set_schedule_by_raw_data(
                self._get_correct_dict_out_of_raw_data(raw_data))
        except:
            print('Error: Cannot read the data from the file.')
        return None
    
    def _get_correct_dict_out_of_raw_data(self, raw_data: dict):
        try:
            dict_to_return = {
                'T': raw_data['T'], # list_of_lists_of_times
                'V': raw_data['V'], # deadline
                'I': raw_data['I'], # list_of_important_indexes
                'U': raw_data['U'], # time_of_the_start
                'N': raw_data['N'], # valid_length_of_list
            }
            return dict_to_return
        except:
            print('Error: Input is not correct.')
        return None
    
    
def default_setup():
    N = 5 # N is number of items, just the length of the list
    V = 4 # V is deadline, items with important indexes must be processed by this value of time
    K, L = 2, 4 # K and L are two important indexes
    I = [K, L] # list of important indexes
    U = 0 # the time of the start
    
    T = [  # list_of_lists_with_times
        [2, 2, 1, 1, 1],
        [1, 1, .5, .5, .5], # this one is the best out of all given samples
        [2, 2, 4, 4, 4],
        [1, 1, 1, .5, .5],
        [1, 2, 2, 2, 2]    
    ]
    
    data_to_dump = {
        'N': N,
        'V': V,
        'I': tuple([K, L]),
        'U': U,
        'T': tuple(T)
    }
    schedule = OptimizedSchedule()
    schedule.init(data_to_dump)
    
    sm = ScheduleManager()
    sm.write_data_to_json('input_0.json', schedule)


def demo():
    sm = ScheduleManager()
    schedule = sm.read_data_from_json('input_0.json')
    sm.write_data_to_json('input_2.json', schedule)
    
    sm.write_the_best_list_to_file('the_best_option.txt', schedule)
    # print(schedule.find_the_best_list())

if __name__ == "__main__":
    
    # demo()
    
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    myapp = Application()
    myapp.show()
    sys.exit(app.exec_()) 
    