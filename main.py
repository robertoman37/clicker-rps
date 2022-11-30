import curses as curse
import sys
import random as rand
import numpy as np
from menu_base import menu_base


class home_menu:

    def __init__(self, last_move):
        menu = menu_base()
        menu.init((("rock", "paper", "scissors"),
                        ("shop", "options", "exit")),
                       (((11, 5), (11, 17), (11, 28)),
                        ((13, 5), (13, 16), (13, 30))))
        self.last_move = [1, 1]
        self.money = 0
        self.graphics_list = ["""\
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",
                          """\
     _______      
---'    ____)____ 
           ______)
          _______)
         _______) 
---.__________)   
""",
                          """\
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""]

    def main(self):
        curses.wrapper(self.home)

    def reverse_parenthesis(self, var):
        return "".join(["(" if i == ")" else
                        ")" if i == "(" else
                        i for i in var])

    def home(self, w):
        a = lambda:\
            f"{' '*37}" if self.first_turn else\
            f"{' '*13}Player Won!{' '*13}" if self.player_won == True else\
            f"{' '*15}AI Won!{' '*15}" if self.player_won == False else\
            f"{' '*13}Nobody Won!{' '*13}"
        curses.curs_set(0)
        w.clear()
        w.addstr(0, 0,
                  "┌──────────────────┬──────────────────┐\n"+
                  "│                  │                  │\n"*7+
                  "├──────────────────┴──────────────────┤\n"+
                 f"│{a()}│\n"+
                  "├────────────┬───────────┬────────────┤\n"+
                  "│    rock    │   paper   │  scissors  │\n"+
                  "├────────────┼───────────┼────────────┤\n"+
                  "│    shop    │  options  │    exit    │\n"+
                  "└────────────┴───────────┴────────────┘\n"+
                  f"{self.player_won}")
        if self.last_move[0] in range(len(self.graphics_list)) or\
        self.last_move[1] in range(len(self.graphics_list)):
            player_graphic = self.graphics_list[self.last_move[0]].splitlines()
            ai_graphic = self.graphics_list[self.last_move[1]].splitlines()
        for i in range(6):
            player_graphic_line = player_graphic[i]
            ai_graphic_line = ai_graphic[i][::-1]
            w.addstr(i+1, 1, player_graphic_line)
            w.addstr(i+1, 20, self.reverse_parenthesis(ai_graphic_line))
        while True:
            try:
                # get input and change cursor_pos correspondingly
                menu.Input()

                # write buffer: includes graphical renditions.
                menu_base.write_buffer(curses)
            except IndexError:
                while True:
                    w.clear()
                    w.addstr(0, 0, "a;sldjfa;skd fh;aksjdh f;alksdj ;flaks d;flaks d;flka sd;lf jas;dfkjasl fdkja slkdjflak sjd;f lkajs; kfas;dl fkajs d;flasjd;f lkasd;f lajsd; fljasd kfa;sdl fj;asldohi sda ;isda ;hl sda; a hk a lhu saf8 r c   4  zszn ez 43v   ;asldkfh;oa idudr[0aw 8uetklajshe tlkasdjxhl kasjd ;kj")

    def game_logic(self, input, w):
        ai_input = rand.randint(0,2)
        if ai_input == 0 and input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 3 and input == 0:
            self.player_won = True
        elif input == 0 and ai_input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 2 and input == 0:
            self.player_won = False
        else:
            self.player_won = None

game = home_menu([1,1])
game.main()
