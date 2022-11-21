class button:
  """
  ------------------------------------NOTE------------------------------------
  buttons do not get cenetered on screen. If you wish for the buttons to be 
  centered, you must prepare the string beforehand
  ----------------------------------------------------------------------------
  """
  def __init__(self, text, pos=-1):
    self.pos    = pos
    self.text   = text

class multiline_text:
  def __init__(self, text, pos=-1):
    self.pos    = pos
    self.text   = text

class singleline_text:
  def __init__(self, text, pos=-1):
    self.pos    = pos
    self.text   = text

class border:
  def __init__(self, pos, border_type = "single_line"):
    """
    ----------------------------USAGE INSTRUCTIONS----------------------------
                               Border_Type attribute                           
    border_type is the type of the border
    default value = single_line
    AVAILABLE TYPES:
      │ = single_line
      ║ = double_line
      ╓ = double_horiz
      ╒ = double_vert
                               Border_type attribute                           
    border_pos is simply put, the position of the border.
    AVAILABLE POSITIONS (with singleline type)
      straight_vert      = │
      straight_horiz     = ─
      corner_topright    = ┐
      corner_topleft     = ┌
      corner_bottomright = ┘
      corner_bottomleft  = └
      horiz_vert_in      = ├
      horiz_vert_out     = ┤
      vert_horiz_up      = ┴
      vert_horiz_down    = ┬
      merge_bord         = ┼
                                     NOTE
    If you pass a value that is not one of the defined ones, that's your fault
    not mine.
    ------------------------------------------------------------------------
    """
    import numpy as np
    border_poss = np.array([["straight_vert","straight_horiz",
                             "corner_topright","corner_topleft",
                             "corner_bottomright","corner_bottomleft",
                             "horiz_vert_in","horiz_vert_out","vert_horiz_up",
                             "vert_horiz_down","merge_bord"],
                            ["single_line","│","─","┐","┌","┘","└","├","┤",
                             "┴","┬","┼"],
                            ["double_line","║","═","╗","╔","╝","╚","╠","╣",
                             "╩","╦","╬"],
                            ["double_horiz","║","─","╖","╓","╜","╙","╟","╢",
                             "╨","╥","╫"],
                            ["double_vert","│","═","╕","╒","╛","╘","╞","╡",
                             "╧","╤","╪"]])
    self.border = border_poss[np.where(border_poss==border_type)[0][0],
                              np.where(border_poss==pos)[1][0]]
class static_menu:
  """Base class for menus. All other menus will inherit from this class"""
  def __init__(self, enable_input):
    import curses
    import numpy as np
    self.enable_input   = enable_input
    self.button_items   = self.button_pos   = []
    self.text_items     = self.text_pos     = []
    self.graphics_items = self.graphics_pos = []
    self.border_items   = self.border_pos   = []
    self.cursor_pos     = [0, 0]
  def create_menu(self, obj_list):
    """Creates a string representation for a menu using a 2d array of 
    elements. Their y position is what list level they are on
    
    EXAMPLE USAGE
    menu_base.create_menu([[border(pos=corner_topleft),
                            border(pos=straight_horiz),
                            border(pos=vert_horiz_down),
                            border(pos=straight_horiz),
                            border(pos=corner_topright)],
                           [border(pos=straight_vert),
                            singleline_text(text)]])"""
    
    for p, v in enumerate(obj_list):
      for i, obj in v:
        if isinstance(obj, button):
          self.button_items.append(obj.text)
          self.button_pos.append((p, i))

        if isinstance(obj, multiline_text):
          self.graphics_items.append(obj.text)
          self.graphics_pos.append((range(p, len(obj.text.splitlines())), i))
          """Multiline text performs a bit differently. The position argument
          for y has to obtain a range of values."""
        if isinstance(obj, singleline_text):
          self.text_items.append(obj.text)
          self.text_pos.append((p, i))
        if isinstance(obj, border):
          self.border_items.append(obj.border)
          self.border_pos.append((p, i))
    