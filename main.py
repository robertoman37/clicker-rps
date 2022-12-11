import curses
import sys
import random as rand
import numpy as np

class menu_base:
    """A base menu class for methods to make making menus in this game easier.
    Contains basic methods which should be inside the main event loop for all
    menus in the game. Note for future me: remember to make a main function
    that takes the return parameters for all classes and directs them to the
    next class, stores global variables, and calls curses.wrapper() inside it.
    """

    def __init__(self, menu_items, menu_pos):
        self.menu_items = menu_items
        self.menu_pos = menu_pos
        self.cursor_pos = [0, 0]

    def Input(self, w):
        uin = w.getch()
        if uin == 259:
            self.cursor_pos[0] -= 1

        elif uin == 258:
            self.cursor_pos[0] += 1

        elif uin == 261:
            self.cursor_pos[1] += 1

        elif uin == 260:
            self.cursor_pos[1] -= 1

        elif uin == 10:
            return None
        #   ^^^ Will eventually assign values to each menu. Uinimplemented for
        #       now

    def write_buffer(self, w):
        for p1, i in enumerate(self.menu_items):
            for p2, v in enumerate(i):
                if self.menu_items[self.cursor_pos[0] % len(self.menu_items)]\
                        [self.cursor_pos[1] % len(i)] == v:
                    w.addstr(self.menu_pos[p1][p2][0],
                             self.menu_pos[p1][p2][1],
                             v,
                             curses.A_REVERSE)
                else:
                    w.addstr(self.menu_pos[p1][p1][0],
                             self.menu_pos[p1][p2][1],
                             v)
        w.refresh()
        

class home_menu(menu_base):

    def __init__(self, last_move):
        """last_move is a two element list of the last moves done.
        -1 = reserved value, first move/ tutorial
        0 = rock
        1 = paper
        2 = scissors"""
        menu_items = (("rock", "paper", "scissors"), ("shop", "options", "exit"))
        menu_pos = (((11, 5), (11, 17), (11, 28)), ((13, 5), (13, 16), (13, 30)))
        super().__init__(menu_items, menu_pos)
        self.last_move = last_move
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
        a = lambda b:\
            f"{' '*37}" if b == -1 else\
            f"{' '*13}Player Won!{' '*13}" if b == 1 else\
            f"{' '*15}AI Won!{' '*15}" if b == 2 else\
            f"{' '*13}Nobody Won!{' '*13}"
        curses.curs_set(0)
        w.clear()
        w.addstr(0, 0,
                  "┌──────────────────┬──────────────────┐\n"+
                  "│                  │                  │\n"*7+
                  "├──────────────────┴──────────────────┤\n"+
                 f"│{a(self.game_logic(self.last_move, True))}│\n"+
                  "├────────────┬───────────┬────────────┤\n"+
                  "│    rock    │   paper   │  scissors  │\n"+
                  "├────────────┼───────────┼────────────┤\n"+
                  "│    shop    │  options  │    exit    │\n"+
                  "└────────────┴───────────┴────────────┘\n")
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
                super().Input(w)

                # write buffer: includes graphical renditions.
                super().write_buffer(w)
            except IndexError:
                while True:
                    w.clear()
                    w.addstr(0, 0, "a;sldjfa;skd fh;aksjdh f;alksdj ;flaks d;flaks d;flka sd;lf jas;dfkjasl fdkja slkdjflak sjd;f lkajs; kfas;dl fkajs d;flasjd;f lkasd;f lajsd; fljasd kfa;sdl fj;asldohi sda ;isda ;hl sda; a hk a lhu saf8 r c   4  zszn ez 43v   ;asldkfh;oa idudr[0aw 8uetklajshe tlkasdjxhl kasjd ;kj")

    def game_logic(self, input, ig_ran):
        """If ig_ran = true, ingores random and takes a two integer list entry
        If not, generates a random number for ai_input"""
        if ig_ran and len(input) == 2:
            ai_input = input[1]
            input = input[0]
        else:
            ai_input = rand.randint(0,2)
        
        if ai_input == 0 and input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 3 and input == 0:
            return 1
        elif input == 0 and ai_input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 2 and input == 0:
            return 2
        elif input == -1:
            return -1
        else:
            return 3

menu = home_menu([1, 2])
menu.main()

class shop_menu(menu_base):
    def __init__(self, resources, items_avail):
        """resources is a dict of the resources available to the player as
        well as their amounts. items_avail is a list of the items available
        to the player in the shop"""
        self.resources = resources
        self.items_avail = items_avail
        self.menu_items = ["quit"] + items_avail
        self.menu_pos = [i for i in range(len(items_avail) + 2)]
        menu_base.__init__(self.menu_items, self.menu_pos)
