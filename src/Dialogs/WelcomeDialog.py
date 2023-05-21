from pgu import gui

class WelcomeDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Welcome")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Welcome to the Quarto Game Simulator!"),colspan=2)
        
        t.tr()
        e = gui.Button("Start")
        e.connect(gui.CLICK,self.send,150)
        t.td(e)
        
        e = gui.Button("Exit")
        e.connect(gui.CLICK,self.send,gui.QUIT)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)