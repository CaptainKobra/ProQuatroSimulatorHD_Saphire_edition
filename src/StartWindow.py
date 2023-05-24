from customtkinter import (CTk, CTkLabel, CTkButton, StringVar, CTkOptionMenu)

class StartWindow:
    class Listener:
        def selectPlayers(self, player1:str, player2:str):
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
        self.textLabel.set("Select players")
        self.startButton.pack_forget()
        self.exitButton.pack_forget()

        self.player1 = StringVar(self.root, "MCTS")
        self.player1Menu = CTkOptionMenu(self.root, values=["human", "MCTS", "MinMax"], variable=self.player1)
        self.player2 = StringVar(self.root, "MinMax")
        self.player2Menu = CTkOptionMenu(self.root, values=["human", "MCTS", "MinMax"], variable=self.player2)
        self.player1Menu.pack()
        self.player2Menu.pack()

        self.confirmButton = CTkButton(self.root, text="Confirm", command=self.onButtonConfirmClick)
        self.confirmButton.pack()


    def onButtonConfirmClick(self):
        self.root.destroy()
        self.listener.selectPlayers(self.player1.get(), self.player2.get())

    def onButton2Click(self):
        exit(0)
            

"""
w = StartWindow()
w.run()
print("end")
"""