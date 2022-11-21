## code that isn't useful anymore but wanted to keep anyways
```python
if self.last_move[0] == -1:
      player_graphic = ""
    if self.last_move[1] == -1:
      ai_graphic = ""
    else:
      player_graphic = self.graphics_list[self.last_move[0]]
      ai_graphic = self.graphics_list[self.last_move[1]]
      graphic = "".join([f"│{player_graphic.splitlines()[i]}"
      f"{' '*(18-len(player_graphic.splitlines()[i]))}│"
      f"{' '*(18-len(self.reverse_parentheses(ai_graphic.splitlines()[i][::-1])))}"
      f"{self.reverse_parentheses(ai_graphic.splitlines()[i][::-1])}│\n"
      for i in range(6)])\
      if len(player_graphic)>1else f"│{' '*18}│{' '*18}│\n"*6
```
## How to use the `menu_base` class
when creating a menu class, import the 
