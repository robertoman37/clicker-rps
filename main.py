import curses
import sys
import random as rand
import numpy as np
from menu_base import *


class home_menu:

    def __init__(self):
        self.first_turn = True
        self.last_move = [1, 1]
        self.player_won = None
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

    # variables for home menu
    self.home_menu_items = (("rock", "paper", "scissors"),
                            ("shop", "options", "exit"))
    self.home_menu_pos = (((11, 5), (11, 17), (11, 28)),
                                ((13, 5), (13, 16), (13, 30)))
# ^ entires correspond to self.home_menu_items  in order

    self.cursor_pos = [0, 0]

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
                uin = w.getch()
                if uin == 259:
                    self.cursor_pos[0] -= 1

                elif uin == 258:
                    self.cursor_pos[0] += 1

                elif uin == 261:
                    self.cursor_pos[1] += 1

                elif uin == 260:
                    self.cursor_pos[1] -= 1

                # enter submenu or enter game phase
                elif uin == 10:
                    self.process_input(self.cursor_pos,
                                       self.home_menu_items,
                                       w)

                # write buffer: includes graphical renditions.
                for p1, i in enumerate(self.home_menu_items):
                    for p2, v in enumerate(i):
                        if self.home_menu_items[self.cursor_pos[0] % 2]\ # PEP8 FORMATTING PLEASE STOP COMPLAINING I KNOW YOUR IP
                                [self.cursor_pos[1] % 3] == v:
                            w.addstr(self.home_menu_pos[p1][p2][0],
                                self.home_menu_pos[p1][p2][1],
                                v,
                                curses.A_REVERSE)
                         else:
                            w.addstr(self.home_menu_pos[p1][p2][0],
                            self.home_menu_pos[p1][p2][1],
                            v)
        w.refresh()
        except IndexError:
            if self.cursor_pos[1] >= 2:
                self.cursor_pos[1] -= 1
            elif self.cursor_pos[0] >= 3:
                self.cursor_pos -= 1
    
    def process_input(self, input, menu_list, w):
        if menu_list == (("rock", "paper", "scissors"),
                         ("shop", "options", "exit")):
        if input[0] == 0:
            self.game_logic(input[1], w)
        else:
            if input[1] == 0:
                self.shop(w)
            elif input[1] == 1:
                self.options(w)
            elif input[1] == 2:
                sys.exit()

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

game = home_menu()
game.main()
