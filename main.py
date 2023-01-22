import curses
import sys
import random as rand
import numpy as np

"""-------------------------IMPORTANT INFORMATION-------------------------
   |Idk why I'm making this so fancy, but all of the xxxx.main() classes |
   |in the objects are just for testing. They won't be used in the final |
   |code, because the wrapper class will simply use curses.wrapper() and |
   |pass the w parameter to the classes.                                 |
   -----------------------------------------------------------------------"""

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
            return False

        elif uin == 258:
            self.cursor_pos[0] += 1
            return False

        elif uin == 261:
            self.cursor_pos[1] += 1
            return False

        elif uin == 260:
            self.cursor_pos[1] -= 1
            return False

        elif uin == 10:
            return self.process_input(w)

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

    def process_input(self, w):
        act = self.menu_items[self.cursor_pos[0]][self.cursor_pos[1]]
        return ["rock", "paper", "scissors", "shop", "options", "exit", "start"].index(act)
        

class home_menu(menu_base):

    def __init__(self, last_move):
        """last_move is a two element list of the last moves done.
        -1 = reserved value, first move/ tutorial
        0 = rock
        1 = paper
        2 = scissors"""
        menu_items = (("rock", "paper", "scissors"), ("shop", "options", "exit"))
        menu_pos = (((11, 5), (11, 19), (11, 32)), ((13, 5), (13, 18), (13, 34)))
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
            f"{' '*41}" if b == -1 else\
            f"{' '*15}Player Won!{' '*15}" if b == 1 else\
            f"{' '*17}AI Won!{' '*17}" if b == 2 else\
            f"{' '*15}Nobody Won!{' '*15}"
        curses.curs_set(0)
        w.clear()
        w.addstr(0, 0,
                  "┌────────────────────┬────────────────────┐\n"+
                  "│                    │                    │\n"*7+
                  "├────────────────────┴────────────────────┤\n"+
                 f"│{a(self.game_logic(self.last_move, True))}│\n"+
                  "├────────────┬───────────────┬────────────┤\n"+
                  "│    rock    │     paper     │  scissors  │\n"+
                  "├────────────┼───────────────┼────────────┤\n"+
                  "│    shop    │    options    │    exit    │\n"+
                  "└────────────┴───────────────┴────────────┘\n")
        if self.last_move[0] in range(len(self.graphics_list)) or\
        self.last_move[1] in range(len(self.graphics_list)):
            player_graphic = self.graphics_list[self.last_move[0]].splitlines()
            ai_graphic = self.graphics_list[self.last_move[1]].splitlines()
            for i in range(6):
                player_graphic_line = player_graphic[i]
                ai_graphic_line = ai_graphic[i][::-1]
                w.addstr(i+1, 1, player_graphic_line)
                w.addstr(i+1, 24, self.reverse_parenthesis(ai_graphic_line))
        while True:
            try:
                # get input and change cursor_pos correspondingly
                rcode = super().Input(w)
                if rcode != False:
                    return rcode

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

class shop_menu(menu_base):
    def __init__(self, resources, items_avail):
        """resources is a dict of the resources available to the player as
        well as their amounts. items_avail is a list of the items available
        to the player in the shop (eventually will make into a list of items as 
        a tuple including their name, a tuple for resources needed, and the
        item's description. Item names cannot be more than 27 characters long, 
        however the recommended limit is 9 characters. Everything past that 
        starts getting kinda weird."""
        
        self.resources = resources
        self.items_avail = items_avail
        self.cursor_pos = 0
        self.submenu = False
        self.base_str = """┌────────────────────────────────────────┐
│                  quit                  │
└────────────────────────────────────────┘
┌──────────────────────────────┬─────────┐
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
└──────────────────────────────┴─────────┘"""
        self.items_str = "".join([f"│┌────────────────────────────┐│\n││{' '*(14-(len(item[0])//2))}{item[0]}{' '*(14-(len(item[0])//2)-(len(item[0])%2))}││\n│└────────────────────────────┘│\n" for item in items_avail])
        self.items_str += "│                              │\n"*10
        self.code = False
        
    def menu_str(self, w, pos):
        for p, i in enumerate(self.items_str.splitlines()[pos * 3:(pos * 3) + 9]):
            w.addstr(4+p, 0, i)

    def Input(self, w):
        char = w.getch()
        if char == 258 and self.cursor_pos <= len(self.items_avail) - 2:
            self.cursor_pos += 1
        if char == 259 and self.cursor_pos >= 0:
            self.cursor_pos -= 1
        if char == 10:
            if self.cursor_pos == -1:
                self.code = True
            else:
                self.submenu = not self.submenu
                self.last_pos = self.cursor_pos
                self.cursor_pos = 0
                w.addstr(0, 0, self.base_str)
    
    def main(self):
        curses.wrapper(self.shop_menu)

#    def render_selection(self, w):
#        w.chgat(1, 0, 42, curses.A_NORMAL)
#        w.chgat(5, 0, 42, curses.A_NORMAL)
#        if self.cursor_pos >= 0:
            #self.xpos = len(f"││{' '*(16-(len(self.items_avail[self.cursor_pos])//2))}")
#            w.chgat(5, 3, 32, curses.A_REVERSE)
#        elif self.cursor_pos == -1:
#            w.chgat(1, 1, 40, curses.A_REVERSE)


    def render_selection(self, w):
        # Highlight the quit button
        if self.cursor_pos == -1:
            w.chgat(1, 1, 40, curses.A_REVERSE)
        else:
            w.chgat(1, 0, 42, curses.A_NORMAL)
            
        # Highlight the selected menu item
        # Menu items don't highlight (I think replit's fault). Will fix later
        if self.cursor_pos >= 0:
            x_pos = 3 + 13 - (len(self.items_avail[self.cursor_pos][0]) // 2)
            w.chgat(5, x_pos, len(self.items_avail[self.cursor_pos][0]), curses.A_REVERSE)
        else:
            w.chgat(5, 0, 42, curses.A_NORMAL)

    def submenu_input(self, w):
        char = w.getch()
        if char == 258 and self.cursor_pos <= 1:
            self.cursor_pos += 1
        if char == 259 and self.cursor_pos >= 1:
            self.cursor_pos -= 1
        if char == 10:
            if self.cursor_pos == 0:
                pass #make buying code later
            if self.cursor_pos == 1:
                self.details(w)
            if self.cursor_pos == 2:
                self.submenu = False
                self.cursor_pos = self.last_pos
                w.addstr(0, 0, self.base_str)
    
    def render_submenu(self, w):
        for p, i in enumerate(self.prep_submenu_text(w)[:-1]):
            w.addstr(4+p, 31, i)
        if self.cursor_pos == 0:
            w.chgat(10, 35, 3, curses.A_REVERSE)
        elif self.cursor_pos == 1:
            w.chgat(11, 33, 7, curses.A_REVERSE)
        elif self.cursor_pos == 2:
            w.chgat(12, 34, 5, curses.A_REVERSE)
            
    
    def prep_submenu_text(self, w):
        # Returns a list of strings to print for each row bc that's how curses 
        # works
        name = self.items_avail[self.last_pos][0]
        if len(name) == 0:
            raise Exception("You can't do that")
        if len(name) in range(10):
            return [f"│{' '*(4-len(name)//2)}{name}{' '*(5-len(name)//2-(len(name)%2))}│",
                    "│         │",
                    "│         │",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   0]
        elif len(name) in range(10, 19):
            return [f"│{name[0:9]}│",
                    f"│{' '*(4-len(name[9:19])//2)}{name[9:19]}{' '*(5-len(name[9:19])//2-(len(name[9:19])%2))}│",
                    "│         │",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   1]
        elif len(name) in range(19, 28):
            return [f"│{name[0:9]}│",
                    f"│{name[9:19]}│"
                    f"│{' '*(4-len(name[19:28])//2)}{name[19:28]}{' '*(5-len(name[19:28])//2-(len(name[19:28])%2))}│",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   0]
        else:
            raise Exception("You can't do that")
            
  
    def shop_menu(self, w):
        w.clear()
        curses.curs_set(0)
        w.addstr(0,0, self.base_str)
        while True:
            if not self.submenu:
                self.menu_str(w, self.cursor_pos)
                self.Input(w)
                if self.code:
                    return 6
                self.render_selection(w)
                w.addstr(20,0," "*50)
                w.addstr(20,0,f"{self.cursor_pos}           {self.items_avail[self.cursor_pos]}")
            if self.submenu:
                self.menu_str(w, self.last_pos)
                self.render_submenu(w)
                self.submenu_input(w)
                w.addstr(20,0," "*50)
                w.addstr(20,0,f"{self.cursor_pos}           {self.last_pos}")
            w.refresh()

    def details_str(self, w, item):
        name = item[0]
        resources = item[1]
        description = item[2]
        description += " "*(241-len(description))
        w.addstr(0, 0, "┌────────────────────────────────────────┐\n"
               f"│{name.center(40)}│\n"
                "├─────────┬──────────────────────────────┤\n"
               f"│rock:    │                              │\n"
               f"│{resources[0]}{' '*(9-len(str(resources[0])))}│                              │\n"
               f"│paper:   │                              │\n"
               f"│{resources[1]}{' '*(9-len(str(resources[1])))}│                              │\n"
               f"│scissors:│                              │\n"
               f"│{resources[2]}{' '*(9-len(str(resources[2])))}│                              │\n"
               f"│         │                              │\n"
               f"│         │                              │\n"
                "├─────────┴──────────────────────────────┤\n"
                "│         Press any key to exit.         │\n"
                "└────────────────────────────────────────┘\n")
        w.addstr(3, 11, description[0:30])
        w.addstr(4, 11, description[30:60])
        w.addstr(5, 11, description[60:90])
        w.addstr(6, 11, description[90:120])
        w.addstr(7, 11, description[120:150])
        w.addstr(8, 11, description[150:180])
        w.addstr(9, 11, description[180:210])
        w.addstr(10, 11, description[210:240])
    def details(self, w):
        self.details_str(w, self.items_avail[self.last_pos])
        while True:
            if w.getch() != -1:
                self.shop_menu(w)
                break

class start_menu:
    def __init__(self):
        self.cursor_pos = 0
        self.string = [r"┌─────────────────────────────────────────────────────────────────────────────────────┐",
r"│ ___   ________   ___        _______           ________   ________   ________        │",
r"│ |\  \ |\   ___ \ |\  \      |\  ___ \         |\   __  \ |\   __  \ |\   ____\      │",
r"│ \ \  \\ \  \_|\ \\ \  \     \ \   __/|        \ \  \|\  \\ \  \|\  \\ \  \___|_     │",
r"│  \ \  \\ \  \ \\ \\ \  \     \ \  \_|/__       \ \   _  _\\ \   ____\\ \_____  \    │",
r"│   \ \  \\ \  \_\\ \\ \  \____ \ \  \_|\ \       \ \  \\  \|\ \  \___| \|____|\  \   │",
r"│    \ \__\\ \_______\\ \_______\\ \_______\       \ \__\\ _\ \ \__\      ____\_\  \  │",
r"│     \|__| \|_______| \|_______| \|_______|        \|__|\|__| \|__|     |\_________\ │",
r"│                                                                        \|_________| │",
r"├─────────────────────────────────────────────────────────────────────────────────────┤",
r"│                                        start                                        │",
r"│                                        close                                        │",
r"│                                       options                                       │",
r"└─────────────────────────────────────────────────────────────────────────────────────┘"]
    def main(self):
        curses.wrapper(self.curses_main)
    def print_str(self, w):
        for p, v in enumerate(self.string):
            w.addstr(p, 0, v)
    def curses_main(self, w):
        curses.curs_set(0)
        self.print_str(w)
        w.chgat(10, 41, 5, curses.A_REVERSE)
        while True:
            char = w.getch()

            if char == 258 and self.cursor_pos <= 1:
                self.cursor_pos += 1
            if char == 259 and self.cursor_pos >= 1:
                self.cursor_pos -= 1
            if char == 10:
                if self.cursor_pos == 0:
                    return 6
                if self.cursor_pos == 1:
                    return 5
                if self.cursor_pos == 2:
                    return 4

            # since cursor_pos only has 3 possibilities, this works fine?
            if self.cursor_pos == 0:
                w.chgat(10, 41, 5, curses.A_REVERSE)
                w.chgat(11, 41, 5, curses.A_NORMAL)
                w.chgat(12, 40, 7, curses.A_NORMAL)
            if self.cursor_pos == 1:
                w.chgat(10, 41, 5, curses.A_NORMAL)
                w.chgat(11, 41, 5, curses.A_REVERSE)
                w.chgat(12, 40, 7, curses.A_NORMAL)
            if self.cursor_pos == 2:
                w.chgat(10, 41, 5, curses.A_NORMAL)
                w.chgat(11, 41, 5, curses.A_NORMAL)
                w.chgat(12, 40, 7, curses.A_REVERSE)
            w.refresh()
#menu = shop_menu((1), [("placeholder", (0, 5, 0), "b"),
#                       ("man", (5, 3, 1), "g"),
#                       ("a", (30, 50, 30), "a"),
#                       ("catapult", (10, 5, 3), "20"),
#                       ("minors", (50, 30, 10), "ggggggg"),
#                       ("odd", (30, 10, 5), "bgalhk")])

class game:
    def __init__(self):
        self.items = [("placeholder", (0, 5, 0), "b"),
                       ("man", (5, 3, 1), "g"),
                       ("a", (30, 50, 30), "a"),
                       ("catapult", (10, 5, 3), "20"),
                       ("miners", (50, 30, 10), "ggggggg"),
                       ("odd", (30, 10, 5), "bgalhk")]
        self.last_turn = [-1, -1]
    def main(self):
        curses.wrapper(self.main_curses)
    def main_curses(self, w):
        menu = start_menu()
        code = menu.curses_main(w)
        while True:
            if code == 0:
                pass
            if code == 1:
                pass
            if code == 2:
                pass
            if code == 3:
                menu = shop_menu((1), [("placeholder", (0, 5, 0), "b"),
                       ("man", (5, 3, 1), "g"),
                       ("a", (30, 50, 30), "a"),
                       ("catapult", (10, 5, 3), "20"),
                       ("minors", (50, 30, 10), "ggggggg"),
                       ("odd", (30, 10, 5), "bgalhk")])
                code = menu.shop_menu(w)
            if code == 4:
                pass
            if code == 5:
                sys.exit()
            if code == 6:
                menu = home_menu(self.last_turn)
                code = menu.home(w)
            
                
#menu = start_menu()
menu = game()
menu.main()