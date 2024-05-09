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
    "rgb(37, 31, 33)",  # BSS
    "rgb(133, 44, 43)",  # SE
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
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="10", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[0]], ("-3%", "23%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "28%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_1):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="10", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[1]], ("-3%", "39%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "44%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_2):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="10", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))

    add_image_to_svg(dwg, PLAYER_ICONS[other_players[2]], ("-3%", "55%"), ("15%", "15%"))

    start_x, start_y = "8.5%", "60%"
    line_height = "1.1em"

    for i, line in enumerate(player_state_3):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(line, insert=(start_x, start_y), text_anchor="start", font_size="10", dy=[dy_value], stroke=ROLE_TEXT[role], fill=ROLE_TEXT[role]))
        
    if s.phase == 1:
        add_image_to_svg(dwg, PHASE1_VISUALS[role], ("32%", "2%"), ("70%", "70%"))
    elif s.phase == 2:
        add_image_to_svg(dwg, PHASE2_VISUALS[role], ("32%", "2%"), ("70%", "70%"))
    elif s.phase == 3:
        add_image_to_svg(dwg, PHASE3_VISUALS[role], ("32%", "2%"), ("70%", "70%"))
    else:
        add_image_to_svg(dwg, PHASE4_VISUALS[role], ("32%", "2%"), ("70%", "70%"))

    dwg.add(dwg.rect(insert=("38%", "75%"),
                     size=("58%", "22%"),
                     stroke_width="2",
                     stroke="black",
                     fill="white"))
    

    for i in range(0, len(s.players[role]['cards'])):
        offset = 33 + 10 * i
        if (role-1) in roles:
            if role == 1:
                add_image_to_svg(dwg, BSS_CARDS[8], (str(offset) + "%", "76%"), ("20%", "20%"))
            elif role == 2:
                add_image_to_svg(dwg, SE_CARDS[8], (str(offset) + "%", "76%"), ("20%", "20%"))
            elif role == 3:
                add_image_to_svg(dwg, SL_CARDS[8], (str(offset) + "%", "76%"), ("20%", "20%"))
            else:
                add_image_to_svg(dwg, VC_CARDS[8], (str(offset) + "%", "76%"), ("20%", "20%"))
        else:
            add_image_to_svg(dwg, FACTION_CARDS[role], (str(offset) + "%", "76%"), ("20%", "20%"))
            

    clock_text = f"MINUTES TO MIDNIGHT: {60 - s.clock['Minute']:02}"
    clock_position_x = f"{W - 100}px"  # Adjust this value to position it right with a margin
    clock_position_y = f"{20}px"  # Similarly adjust this to position from the bottom
    dwg.add(dwg.text(clock_text, insert=(clock_position_x, clock_position_y),
                     text_anchor="end", font_size="16px", fill=ROLE_TEXT[role]))
    
    # Display up to 5 most recent events
    num_events = len(s.events)
    events_to_display = s.events[max(0, num_events - 5):num_events]  # Last 5 or fewer
    
    # Calculate start position for events text
    events_start_x = "1%"
    events_start_y = f"{H - 100}px"  # Adjust this value as needed to fit within your SVG dimensions
    line_height = "1.1em"
    
    # Add events text to the SVG
    for i, event in enumerate(reversed(events_to_display)):
        dy_value = f"{float(line_height[:-2]) * i}em"
        dwg.add(dwg.text(event, insert=(events_start_x, events_start_y), text_anchor="start",
                         font_size="8", dy=[dy_value], fill=ROLE_TEXT[role]))

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

PHASE2_VISUALS = {
    1: "bss_phase2.png",
    2: "se_phase2.png",
    3: "sl_phase2.png",
    4: "vc_phase2.png",
}

PHASE3_VISUALS = {
    1: "bss_phase3.png",
    2: "se_phase3.png",
    3: "sl_phase3.png",
    4: "vc_phase3.png",
}

PHASE4_VISUALS = {
    1: "bss_phase4.png",
    2: "se_phase4.png",
    3: "sl_phase4.png",
    4: "vc_phase4.png",
}

FACTION_CARDS = {
    1: "bss_back.png",
    2: "se_back.png",
    3: "sl_back.png",
    4: "vc_back.png"
}

BSS_CARDS = {
    8: "bss_sabotage.png"
}

SE_CARDS = {
    8: "se_sabotage.png"
}

SL_CARDS = {
    8: "sl_sabotage.png"
}

VC_CARDS = {
    8: "vc_sabotage.png"
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
