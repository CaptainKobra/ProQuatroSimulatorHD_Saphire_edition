from pgu import gui
from Dialogs.NewDialog import NewDialog
from Dialogs.QuitDialog import QuitDialog
from Dialogs.WelcomeDialog import WelcomeDialog

class MyApp(gui.App):
    def __init__(self, theme=None, **params):
        super().__init__(theme, **params)

        self.new_d = NewDialog()
        self.new_d.connect(151, self.action_new, "Player")
        self.new_d.connect(152, self.action_new, "IA")

        self.quit_d = QuitDialog()
        self.quit_d.connect(gui.const.QUIT,self.quit,None)
        self.app.connect(gui.QUIT,self.quit_d.open,None)

        self.welcome_d = WelcomeDialog()
        self.app.connect(gui.INIT,self.welcome_d.open,None)
        self.welcome_d.connect(gui.const.QUIT,self.quit,None)
        self.welcome_d.connect(150,self.start,None)


    def action_new(self,value=None):
        print(value)
        self.new_d.close()
        # TODO


    def start(self, value=None):
        self.welcome_d.close()
        self.new_d.open()

