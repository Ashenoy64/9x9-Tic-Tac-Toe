from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse, Color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle


class Box(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(240/255, 240/255, 240/255)
            self.rect = Rectangle()
        self.bind(pos=self.update)
        self.bind(size=self.update)
        self.cols = 3
        self.l = []
        self.create_box()
        self.spacing = "1dp"
        self.squareList = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.winner = 0
        self.first = 1

    def update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def create_box(self):
        for i in range(9):
            self.l.append(Button(text=" ", background_disabled_normal="", on_press=self.place, background_color=(
                0, 0, 0, 0.5), disabled_color=(1, 1, 1, 1), pos=self.pos, size=self.size))
            self.l[i].border = (10, 10, 10, 10)
            self.add_widget(self.l[i])

    def place(self, button):
        if self.parent.cur_player == 1:
            button.color = (1, 0, 0)
            button.disabled_color = (1, 0, 0, 1)
            button.text = "X"
        else:
            button.color = (0, 0, 1)
            button.disabled_color = (0, 0, 1, 1)
            button.text = "O"
        self.parent.box = self.l.index(button)
        self.squareList[self.parent.box] = self.parent.cur_player
        #print(self.squareList)
        return self.parent.taketurn()

    def highlight_dim(self, col):
        r, g, b = col
        self.canvas.before.remove(self.rect)
        with self.canvas.before:
            Color(r, g, b)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def disable_buttons(self):
        for i in self.l:
            i.disabled = True

    def enable_buttons(self):
        for i in self.l:
            if i.text != "X" or i.text != "O":
                i.disabled = False

    def isFull(self):
        for i in range(9):
            if self.squareList[i] == 0:
                return False
        return True

    def check_winner(self):
        if self.winner == 0:
            win_cond = [(0, 1, 2), (0, 3, 6), (0, 4, 8), (3, 4, 5),
                        (1, 4, 7), (2, 4, 6), (6, 7, 8), (2, 5, 8)]
            for win in win_cond:
                x, y, z = win
                if self.squareList[x] == self.squareList[y] and self.squareList[z] == self.squareList[y] and self.squareList[x] != 0:
                    self.winner = self.squareList[x]
        return self.winner

    def move(self, square, player):
        self.squareList[square] = player


class Window(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rect = []
        self.grid = []
        self.def_col = (240/255, 240/255, 240/255)
        self.pos_hint = {"x": .25, "y": 0.25}
        self.size_hint = (0.5, 0.5)
        self.create_grid()
        self.player1_color = (1, 0, 0,)
        self.player2_color = (0, 0, 1)
        self.highlight = (240/255, 240/255, 240/255)
        self.dim = (0.41, 0.41, 0.41)
        self.spacing = "1dp"
        self.box_list = []
        self.winner = 0
        self.player1_Box = []
        self.player2_Box = []
        self.box = 4
        self.nextMove = 4
        self.cur_player = 1
        self.player2 = 2
        self.begin()
    def End_Game(self):
        for i in range(9):
            self.grid[i].disable_buttons()
        if self.winner==1:
            winner="X"
        else:
            winner="O"

        self.parent.show(winner)

    def begin(self):
        for i in range(9):
            self.grid[i].disable_buttons()

    def play(self):
        self.nextMove = self.box
        if self.nextMove == 4 and self.isCenterFull():
            self.setWinner(self.player2)
            self.End_Game()
        if self.isOver():
            self.End_Game()
        self.highlight_dim(self.nextMove)
        self.cur_player, self.player2 = self.player2, self.cur_player

    def taketurn(self):
        # self.nextMove=self.box_list
        winner = self.move(self.nextMove, self.cur_player)
        if winner != 0:
            if winner==1:
                self.grid[self.nextMove].highlight_dim(self.player1_color)
            else:
                self.grid[self.nextMove].highlight_dim(self.player2_color)
        return self.play()

    def getNextMove(self):
        return self.nextMove

    def isCenterFull(self):
        return self.grid[4].isFull()

    def move(self, box, player):
        if self.grid[box].check_winner() == 1 and box not in self.player1_Box:
            self.player1_Box.append(box)
            self.parent.update_score(1)
        if self.grid[box].check_winner() == 2 and box not in self.player2_Box:
            self.player2_Box.append(box)
            self.parent.update_score(2)

        return self.grid[box].check_winner()


    def isBoxwon(self, box):
        return self.box_list[box].check_winner()

    def isValid(self, box, square):
        return self.grid[box].squareList[square] == 0

    def isOver(self):
        return len(self.player1_Box) == 5 or len(self.player2_Box) == 5

    def setWinner(self, player):
        self.winner = player

    def getWinner(self):
        if self.isOver() and len(self.player2_Box) == 5:
            self.winner = 2
        if self.isOver() and len(self.player1_Box) == 5:
            self.winner = 1

        return self.winner

    def highlight_dim(self, block_no):
        for i in range(9):
            if i not in self.player1_Box and i not in self.player2_Box:
                if i == block_no:
                    self.grid[i].highlight_dim(self.highlight)
                else:
                    self.grid[i].highlight_dim(self.dim)
            if i == block_no:
                self.grid[i].enable_buttons()
            else:
                self.grid[i].disable_buttons()

    def create_grid(self):
        for i in range(9):
            self.grid.append(Box())
            '''with self.grid[i].canvas.before:
                Color(240/255,240/255,240/255)
                self.rect.append(Rectangle(size=self.grid[i].size,pos=self.grid[i].pos))'''

            self.add_widget(self.grid[i])


class Top(BoxLayout):
    obj = Window()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.control=BoxLayout()
        self.control.size_hint=(1,0.1)
        self.orientation="vertical"
        self.create_game=Button(text="Start Game",on_press=self.start)
        self.player1=Label(text="Player 1:'X'  0")
        self.player2=Label(text="Player 2:'O'  0")
        self.add_widget(self.control)
        self.control.add_widget(self.create_game)
        self.final=Label()
        self.add_widget(self.obj)




    def start(self,btn):
        self.obj.highlight_dim(self.obj.nextMove)
        self.control.remove_widget(self.create_game)
        self.control.add_widget(self.player1)
        self.control.add_widget(self.player2)

    def update_score(self,player):
        if player==1:
            self.player1.text="Player 1:'X'  {}".format(len(self.obj.player1_Box))
        else:
            self.player2.text="Player 2:'O'  {}".format(len(self.obj.player2_Box))

    def show(self,winner):
        self.control.remove_widget(self.player1)
        self.control.remove_widget(self.player2)
        self.add_widget(self.final)
        self.final.text="Player {} won ".format(winner)
    '''def play(self):
    while true:
        get next move box
        highlilight and dim box
        player 1 moves
        decide next move box
        
        if box==4 and self.gameborad is full:
            self.gameboard.setwinner(2)
            break
        if self.gameboard.isover():
            break
        unhiglight and higlighht

        player 2 moves
        decide next move box
        if box==4 and self.gameborad is full:
            self.gameboard.setwinner(1)
            break
        if self.gameboard.isover():
            break
        highligh and unlight

        afer break
        winner=self.gameboard.getwinner



    '''


class ExampleApp(App):
    obj = Top()

    def build(self):
        return self.obj


app = ExampleApp()
app.run()
