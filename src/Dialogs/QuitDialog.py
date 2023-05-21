from pgu import gui

class QuitDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Quit")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Are you sure you want to quit?"),colspan=2)
        
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.QUIT)
        t.td(e)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)