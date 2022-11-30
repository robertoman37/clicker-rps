class menu_base:
    """A base menu class for methods to make making menus in this game easier.
    Contains basic methods which should be inside the main event loop for all
    menus in the game. Note for future me: remember to make a main function
    that takes the return parameters for all classes and directs them to the
    next class, stores global variables, and calls curses.wrapper() inside it.
    """

    def init(self, menu_items, menu_pos):
        """define in here whatever other things you need to do for your menu to
        work."""
        import curses
        self.menu_items = menu_items
        self.menu_pos = menu_pos
        self.cursor_pos = [0, 0]

    def Input(self, w):
        uin = w.getch
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

    def write_buffer(self, w, curses):
        for p1, i in enumerate(self.menu_items):
            for p2, v in enumerate(i):
                if self.menu_items[self.cursor_pos[0] % len(self.menu_items)]\
                        [self.cursor_pos[p1] % len(i)] == v:
                    w.addstr(self.menu_pos[p1][p2][0],
                             self.menu_pos[p1][p2][1],
                             v,
                             curses.A_REVERSE)
                # note to self: fix that ^^^
                else:
                    w.addstr(self.menu_pos[p1][p1][0],
                             self.menu_pos[p1][p2][1],
                             v)
        w.refresh()
