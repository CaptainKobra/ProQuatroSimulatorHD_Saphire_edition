from customtkinter import (CTk, CTkLabel, CTkButton, StringVar)

class StartWindow:
    class Listener:
        def selectStarter(self, starter:str):
            pass

    def __init__(self) -> None:
        self.root = CTk()
        self.root.title("QUARTO")
        self.root.geometry("400x200")

        self.textLabel = StringVar(self.root, value="Welcome in Quarto game simulator!")
        self.texButton1 = StringVar(self.root, value="Start")
        self.texButton2 = StringVar(self.root, value="Exit")

        self.welcomeLabel = CTkLabel(self.root, textvariable=self.textLabel)
        self.startButton = CTkButton(self.root, textvariable=self.texButton1, command=self.onButton1Click)
        self.exitButton = CTkButton(self.root, textvariable=self.texButton2, command=self.onButton2Click)

        self.welcomeLabel.pack(pady=30)
        self.startButton.pack()
        self.exitButton.pack()

        self.listener = None


    def setListener(self, l:Listener):
        self.listener = l


    def run(self):
        self.root.mainloop()


    def onButton1Click(self):
        if self.texButton1.get() == "Start":
            self.textLabel.set("Who Starts ?")
            self.texButton1.set("Me")
            self.texButton2.set("AI")
        else:
            self.root.destroy()
            self.listener.selectStarter("player")


    def onButton2Click(self):
        if self.texButton2.get() == "Exit":
            exit(0)
        else:
            self.root.destroy()
            self.listener.selectStarter("AI")
            

"""
w = StartWindow()
w.run()
print("end")
"""