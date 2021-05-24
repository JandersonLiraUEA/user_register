import sys

from PyQt5.QtWidgets import QApplication

from screens.screen_main import ScreenMain
from data.methods_db import MethodsDb


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.db = MethodsDb()
        self.db.start_conn()
        self.db.create_tables()
        self.db.close_conn()

        self.view_main = ScreenMain()
        self.view_main.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())