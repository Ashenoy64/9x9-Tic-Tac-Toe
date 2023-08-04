from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import  Color
from kivy.graphics import Rectangle


#3x3 grid
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
        return self.parent.take_turn()

    def background_highlight(self, col):
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

    def is_full(self):
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


class Grid(GridLayout):
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
        self.player1_Box = []
        self.player2_Box = []

        self.winner = 0
        self.box = 4
        self.nextMove = 4
        self.cur_player = 1
        self.player2 = 2

        self.disable()

    def create_grid(self):
        for i in range(9):
            self.grid.append(Box())
            self.add_widget(self.grid[i])

    def disable(self):
        for i in range(9):
            self.grid[i].disable_buttons()

    def end_game(self):
        for i in range(9):
            self.grid[i].disable_buttons()
        if self.winner==1:
            winner="X"
        else:
            winner="O"

        self.parent.result(winner)

    

    def play(self):
        self.nextMove = self.box
        if self.nextMove == 4 and self.is_center_full():
            self.set_winner(self.player2)
            self.end_game()
        if self.is_over():
            self.end_game()
        self.background_highlight(self.nextMove)
        self.cur_player, self.player2 = self.player2, self.cur_player

    def take_turn(self):
        winner = self.move(self.nextMove)
        if winner != 0:
            if winner==1:
                self.grid[self.nextMove].background_highlight(self.player1_color)
            else:
                self.grid[self.nextMove].background_highlight(self.player2_color)
        return self.play()


    def is_center_full(self):
        return self.grid[4].is_full()

    def move(self, box):
        if self.grid[box].check_winner() == 1 and box not in self.player1_Box:
            self.player1_Box.append(box)
            self.parent.update_score(1)
        if self.grid[box].check_winner() == 2 and box not in self.player2_Box:
            self.player2_Box.append(box)
            self.parent.update_score(2)

        return self.grid[box].check_winner()


    def is_over(self):
        return len(self.player1_Box) == 5 or len(self.player2_Box) == 5

    def set_winner(self, player):
        self.winner = player



    def background_highlight(self, block_no):
        for i in range(9):
            if i not in self.player1_Box and i not in self.player2_Box:
                if i == block_no:
                    self.grid[i].background_highlight(self.highlight)
                else:
                    self.grid[i].background_highlight(self.dim)
            if i == block_no:
                self.grid[i].enable_buttons()
            else:
                self.grid[i].disable_buttons()

    


class Top(BoxLayout):
    grid = Grid()

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
        self.add_widget(self.grid)


    def start(self,btn):
        self.grid.background_highlight(self.grid.nextMove)
        self.control.remove_widget(self.create_game)
        self.control.add_widget(self.player1)
        self.control.add_widget(self.player2)

    def update_score(self,player):
        if player==1:
            self.player1.text="Player 1: X  {}".format(len(self.grid.player1_Box))
        else:
            self.player2.text="Player 2: O   {}".format(len(self.grid.player2_Box))

    def result(self,winner):
        context=GridLayout(cols=1,padding=10)
        popup_label=Label(text=f'Player {winner} won ')
        popup_close_button=Button(text="Close")
        
        context.add_widget(popup_label)
        context.add_widget(popup_close_button)
        
        popup=Popup(title="Status",content=context,size_hint=(None, None), size=(400, 200))
        popup.open()
        popup_close_button.bind(on_press=popup.dismiss)
    
      


class App(App):
    def build(self):
        return Top()


App().run()
