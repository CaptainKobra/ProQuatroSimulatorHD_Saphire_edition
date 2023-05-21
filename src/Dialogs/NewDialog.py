from pgu import gui

class NewDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Who Starts?")
        
        t = gui.Table()
        
        t.tr()
        t.td(gui.Label("Who starts the game ?"),align=0,colspan=2)
        
        t.tr()
        b1 = gui.Button("You")
        b1.connect(gui.CLICK,self.send,151)
        t.td(b1)
        
        b2 = gui.Button("AI")
        b2.connect(gui.CLICK,self.send,152)
        t.td(b2)
        
        gui.Dialog.__init__(self,title,t)