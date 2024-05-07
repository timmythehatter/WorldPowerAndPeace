# Author: S. Tanimoto
# Purpose: SVG visualization for a generic game
# Created: 2020
# Python version 3.x

import svgwrite
import base64
from PowerAndPeace import *  # State,

DEBUG = False
W = 1275  # Width of Vis. region
SQW = W / 8
HALF_SQW = SQW / 2
H = 600
THREE_QUARTER_SQW = 3 * (HALF_SQW / 2)

ROLE_COLORS = [
    "rgb(0, 0, 0)", #black
    "rgb(13, 10, 11)",  # BSS
    "rgb(113, 11, 9)",  # SE
    "rgb(124, 191, 203)",  # SL
    "rgb(119, 197, 131)",  # VC
    "rgb(150, 150, 150)"]  # no-role or observer: darker gray.

ROLE_TEXT = [
    "rgb(0, 0, 0)", #black
    "rgb(180, 179, 173)",  # BSS
    "rgb(235, 235, 234)",  # SE
    "rgb(0, 0, 0)",  # SL
    "rgb(0, 0, 0)",  # VC
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
                            size=("98%", "100%"),
                            viewBox=f"0 0 {W} {H}",
                            debug=False)


    role = s.whose_turn
    role_state = [
        f"CURRENT PLAYER: {FACTIONS[role]}",
        f"MONEY: {s.players[role]['money']}",
        f"STABILITY: {s.players[role]['stability']}",
        f"GOAL SCORE: {s.players[role]['goalScore']}"
    ]


    other_players = []

    for i in range(1, 5):
        if i != role:
            other_players.append(i)

    player_state_1 = [
        f"PLAYER {other_players[0]}: {FACTIONS[other_players[0]]}",
        f"MONEY: {s.players[other_players[0]]['money']}",
        f"STABILITY: {s.players[other_players[0]]['stability']}",
        f"GOAL SCORE: {s.players[other_players[0]]['goalScore']}"
    ]

    player_state_2 = [
        f"PLAYER {other_players[1]}: {FACTIONS[other_players[1]]}",
        f"MONEY: {s.players[other_players[1]]['money']}",
        f"STABILITY: {s.players[other_players[1]]['stability']}",
        f"GOAL SCORE: {s.players[other_players[1]]['goalScore']}"
    ]

    player_state_3 = [
        f"PLAYER {other_players[2]}: {FACTIONS[other_players[2]]}",
        f"MONEY: {s.players[other_players[2]]['money']}",
        f"STABILITY: {s.players[other_players[2]]['stability']}",
        f"GOAL SCORE: {s.players[other_players[2]]['goalScore']}"
    ]
        
    dwg.add(dwg.rect(insert=("0%", "0%"),
                     size=("100%", "100%"),
                     stroke_width="1",
                     stroke="black",
                     fill=ROLE_COLORS[role]))
        
    add_image_to_svg(dwg, PLAYER_ICONS[role], ("-4.5%", "2%"), ("20%", "20%"))
    # Add role state with separate text lines
    start_x, start_y = "10.5%", "8%"
    line_height = "1.2em"

    for i, line in enumerate(role_state):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="14", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[0]], ("-3%", "23%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "28%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_1):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="12", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[1]], ("-3%", "39%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "44%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_2):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="12", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[2]], ("-3%", "55%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "60%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_3):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="12", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))
        
    add_image_to_svg(dwg, PHASE1_VISUALS[role], ("32%", "2%"), ("70%", "70%"))

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
    DEBUG = False
    PLAYER_HAND = [[('p', 0), ('r', 3), ('r', 6), ('p', 4)]]
    session = {'HOST': 'localhost', 'PORT': 5000}
    INITIAL_STATE = State()
    print(INITIAL_STATE)
    svg_string = render_state(INITIAL_STATE, roles=[0])
    print("svg_string is: ")
    print(svg_string)
