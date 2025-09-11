rows, cols = 3, 3
x_o = []
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(" ")  # fill with 0 (or any value)
    x_o.append(row)


def get_current_shape():
    _TICTACTOE = f"""
      {x_o[0][0]}  | {x_o[0][1]}  | {x_o[0][2]}  
    -------------
      {x_o[1][0]}  | {x_o[1][1]}  | {x_o[1][2]}  
    -------------
      {x_o[2][0]}  | {x_o[2][1]}  | {x_o[2][2]}  
    """
    print(_TICTACTOE)


def is_x_winning():
    x_wins = False
    for curr_col in range(3):
        if x_o[curr_col] == ["x", "x", "x"]:
            x_wins = True

    for r in range(3):
        if x_o[0][r] == "x" and x_o[1][r] == "x" and x_o[2][r] == "x":
            x_wins = True

    if x_o[0][0] == "x" and x_o[1][1] == "x" and x_o[2][2] == "x":
        x_wins = True
    elif x_o[0][2] == "x" and x_o[1][1] == "x" and x_o[2][0] == "x":
        x_wins = True

    if x_wins:
        print("X WINS!")
        return True
    else:
        return False


def is_o_winning():
    o_wins = False
    for curr_col in range(3):
        if x_o[curr_col] == ["o", "o", "o"]:
            o_wins = True

    for r in range(3):
        if x_o[0][r] == "o" and x_o[1][r] == "o" and x_o[2][r] == "o":
            o_wins = True

    if x_o[0][0] == "o" and x_o[1][1] == "o" and x_o[2][2] == "o":
        o_wins = True
    elif x_o[0][2] == "o" and x_o[1][1] == "o" and x_o[2][0] == "o":
        o_wins = True

    if o_wins:
        print("O WINS!")
        return True
    else:
        return False


def is_draw():
    draw = 0
    for i in range(3):
        for j in range(3):
            if x_o[i][j] != " ":
                draw += 1
    if draw == 9:
        print("DRAW!")
        return True
    else:
        return False


def set_char(value, letter):
    if value == 1:
        x_o[0][0] = letter
    elif value == 2:
        x_o[0][1] = letter
    elif value == 3:
        x_o[0][2] = letter
    elif value == 4:
        x_o[1][0] = letter
    elif value == 5:
        x_o[1][1] = letter
    elif value == 6:
        x_o[1][2] = letter
    elif value == 7:
        x_o[2][0] = letter
    elif value == 8:
        x_o[2][1] = letter
    elif value == 9:
        x_o[2][2] = letter


while True:
    x_value = int(input("Enter X value from 1 to 9: "))
    set_char(x_value, "x")
    get_current_shape()
    if is_x_winning() or is_draw():
        break
    o_value = int(input("Enter O value from 1 to 9: "))
    set_char(o_value, "o")
    get_current_shape()
    if is_o_winning() or is_draw():
        break
