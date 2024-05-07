# Author: S. Tanimoto
# Purpose: SVG visualization for a generic game
# Created: 2020
# Python version 3.x

import svgwrite
import base64
from PowerAndPeace import *  # State,

DEBUG = False
W = 1250  # Width of Vis. region
SQW = W / 8
HALF_SQW = SQW / 2
H = 700
THREE_QUARTER_SQW = 3 * (HALF_SQW / 2)

ROLE_COLORS = [
    "rgb(0, 0, 0)", #black
    "rgb(220, 220, 220)",  # (off) white
    "rgb(255, 0, 0)",  # scarlet
    "rgb(0, 100, 230)",  # peacock
    "rgb(0, 255, 0)",  # green
    "rgb(150, 150, 150)"]  # no-role or observer: darker gray.

session = None

def load_image_as_base64(filepath):
    """Load an image file and return its data URL"""
    with open(filepath, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
        img_type = filepath.split('.')[-1]
        return f"data:image/{img_type};base64,{img_data}"
    
def add_image_to_svg(dwg, image_path, position, size):
    """Add an image to an SVG drawing at the specified position and size"""
    image_data_url = load_image_as_base64(image_path)
    dwg.add(dwg.image(image_data_url, insert=position, size=size))


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
        
        role = s.whose_turn
        
        dwg.add(dwg.rect(insert=(0, 0),
                         size=(str(W) + "px", str(H) + "px"),
                         stroke_width="1",
                         stroke="black",
                         fill=ROLE_COLORS[role]))

        label = "This is for the role of " + FACTIONS[role]
        x = 300;
        y = 100
        dwg.add(dwg.text(label, insert=(x + HALF_SQW, y - THREE_QUARTER_SQW),
                         text_anchor="middle",
                         font_size="25",
                         stroke="black",
                         fill="red"))
        add_image_to_svg(dwg, PHASE1_VISUALS[role], (0,0), (str(W) + "px", str(H) + "px"))

    svg_string = dwg.tostring()
    return svg_string

PLAYER_ICONS = {
    1: "bss_icon.png",
    2: "se_icon.png",
    3: "sl_icon.png",
    4: "vc_icon.png"
}

PHASE1_VISUALS = {
    1: "bss_phase1.png",
    2: "se_phase1.png",
    3: "sl_phase1.png",
    4: "vc_phase1.png",
}

if __name__ == '__main__':
    DEBUG = True
    PLAYER_HAND = [[('p', 0), ('r', 3), ('r', 6), ('p', 4)]]
    session = {'HOST': 'localhost', 'PORT': 5000}
    INITIAL_STATE = State()
    print(INITIAL_STATE)
    svg_string = render_state(INITIAL_STATE, roles=[0])
    print("svg_string is: ")
    print(svg_string)
