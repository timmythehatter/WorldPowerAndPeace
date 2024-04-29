# Author: S. Tanimoto
# Purpose: SVG visualization for a generic game
# Created: 2020
# Python version 3.x

import svgwrite
from PowerAndPeace import *  # State,
import PowerAndPeace

DEBUG = False
W = 850  # Width of Vis. region
SQW = W / 8
HALF_SQW = SQW / 2
H = 400
THREE_QUARTER_SQW = 3 * (HALF_SQW / 2)

ROLE_COLORS = [
    "rgb(255, 0, 0)",  # scarlet
    "rgb(0, 255, 0)",  # green
    "rgb(200, 200, 0)",  # mustard
    "rgb(100, 0, 150)",  # plum
    "rgb(0, 100, 230)",  # peacock
    "rgb(220, 220, 220)",  # (off) white
    "rgb(150, 150, 150)"]  # no-role or observer: darker gray.

session = None
def render_state(s, roles=None):
    global session
    session = get_session()  # Need HOST and PORT info for accessing images.
    dwg = svgwrite.Drawing(filename="test-svgwrite.svg",
                            id="state_svg",  # Must match the id in the html template.
                            size=(str(W) + "px", str(H) + "px"),
                            debug=True)

    if roles == None or roles == []:
        label = "This player doesn't have any role in the game."
        x = 100;
        y = 100
        dwg.add(dwg.text(label, insert=(x + HALF_SQW, y + THREE_QUARTER_SQW),
                         text_anchor="middle",
                         font_size="25",
                         fill="red"))
    else:
        yc = 100
        # Instead of rendering all this player's roles, render just
        # the vis for the role that is current or most recent.
        # This info should be in the state.
        if s.whose_subturn > -1 and s.suggestion_phase < 5:
            active_role = s.whose_subturn
        else:
            active_role = s.whose_turn
        if active_role in roles:
            role = active_role
        else:
            role = roles[0]
        dwg.add(dwg.rect(insert=(0, 0),
                         size=(str(W) + "px", str(H) + "px"),
                         stroke_width="1",
                         stroke="black",
                         fill=ROLE_COLORS[role]))

        label = "This is for the role of " + NAMES[role]
        x = 300;
        y = 100
        dwg.add(dwg.text(label, insert=(x + HALF_SQW, y - THREE_QUARTER_SQW),
                         text_anchor="middle",
                         font_size="25",
                         stroke="black",
                         fill="red"))
    svg_string = dwg.tostring()
    return svg_string

if __name__ == '__main__':
    DEBUG = True
    PLAYER_HAND = [[('p', 0), ('r', 3), ('r', 6), ('p', 4)]]
    session = {'HOST': 'localhost', 'PORT': 5000}
    INITIAL_STATE = State()
    print(INITIAL_STATE)
    svg_string = render_state(INITIAL_STATE, roles=[0])
    print("svg_string is: ")
    print(svg_string)
