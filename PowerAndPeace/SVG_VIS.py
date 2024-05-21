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

def split_text(text, max_length=50):  # 'indent' can be adjusted as needed
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) + 1 > max_length:
            if current_line:  # Avoid adding an empty string if the first word is too long
                lines.append(current_line)
            current_line =  word  # Start a new line with an indentation
        else:
            if current_line:
                current_line += " " + word  # Add a space before the word if it's not the first word
            else:
                current_line = word  # Start a new line without leading spaces

    lines.append(current_line)
    return lines




def render_state(s, roles=None):
    global session
    session = get_session()  # Need HOST and PORT info for accessing images.
    dwg = svgwrite.Drawing(filename="test-svgwrite.svg",
                            id="state_svg",  # Must match the id in the html template.
                            size=("98%", "100%"),
                            viewBox=f"0 0 {W} {H}",
                            debug=False)
    
    if s.whose_turn == -1:
        if s.game_turn == 1:
            # # Path to your background image
            # background_image_path = "path_to_your_background_image.jpg"

            # # Add the background image
            # add_image_to_svg(dwg, background_image_path, (0, 0), (W, H))

            intro_text = [
                "In a galaxy far, far away, a delicate balance of power shapes the destiny of countless lives. Amidst the stars, four distinct nations vie for dominance, each driven by their own unique ambitions and ideologies.",
                "The Black Sun Syndicate",
                "From the dense industrial complexes of their capital, the leaders of the Black Sun Syndicate master the art of economics. This money-hungry nation, built on the engines of massive corporations and fueled by ceaseless commerce, is dedicated to accumulating wealth. Their economy is their weapon, their shield, and their philosophy. Ruthless in business and unyielding in their pursuit of financial supremacy, they navigate the cosmic seas with a fleet powered by the almighty credit.",
                "The Scarlet Empire",
                "With their vast armies and formidable fleets, the Scarlet Empire epitomizes the might of military prowess. Theirs is a society built on the valor of conquest and the spoils of war. Benefiting greatly from the arms trade, the Empire's forges burn day and night, crafting weapons that ensure their borders expand ever outward. Warlords and generals hold power here, ruling over their domains with iron fists and sharp strategies.",
                "The Sapphire League",
                "Amidst the intellectual sanctuaries and advanced research facilities, the Sapphire League rises as a beacon of progress. This technologically advanced nation thrives on innovation and scientific discovery. Their society is sculpted by the brightest minds, where inventors and scientists are revered. In their quest for knowledge, they harness the power of new technologies to influence the galaxy around them, offering solutions that sway wars and alter economies.",
                "The Viridian Concord",
                "Deep within lush green worlds and thriving biodomes, the Viridian Concord champions the cause of the environment. This ecologically focused nation stands as the galaxy's guardian of nature, dedicated to preserving the delicate balance of their ecosystems. They wield influence not through force or wealth but through diplomacy and stewardship, striving to protect the galaxy from the ravages of industrial exploitation and warfare.",
                "As tensions rise and alliances form, the galaxy watches with bated breath, waiting to see which nation will ascend to dominate the cosmic landscape. The struggle for power, peace, and prosperity rages on, echoing through the stars..."
            ]

            text_start_x = "50%"
            text_start_y = "10%"  # Adjust starting y-coordinate as needed
            text_dy = "1.5em"
            dy_accumulated = 0
            
            for i, paragraph in enumerate(intro_text):
                font_size = "12px"
                if paragraph.startswith("The "):  # This is a title, add extra space before it
                    dy_accumulated += 1.5  # Increase for a line break
                lines = split_text(paragraph, 170)
                for line in lines:
                    dy_value = f"{dy_accumulated}em"
                    dy_accumulated += 1.5  # Increase the dy value after each line
                    dwg.add(dwg.text(line,
                                    insert=(text_start_x, text_start_y),
                                    text_anchor="middle",
                                    font_size=font_size,
                                    dy=[dy_value],
                                    fill="black"))
            
            return dwg.tostring()
        else:
            if s.phase_events:
                text_start_x = "50%"
                text_start_y = "10%"  # Adjust starting y-coordinate as needed
                text_dy = "1.5em"
                dy_accumulated = 0
                font_size = "12px"

                for event in s.phase_events:
                    lines = split_text(event, 170)
                    for line in lines:
                        dy_value = f"{dy_accumulated}em"
                        dy_accumulated += 1.5  # Increase the dy value after each line
                        dwg.add(dwg.text(line,
                                        insert=(text_start_x, text_start_y),
                                        text_anchor="middle",
                                        font_size=font_size,
                                        dy=[dy_value],
                                        fill="black"))

                return dwg.tostring()


    
    # Check if the game is over and display the end game message if it is.
    if s.game_over:
        text = dwg.text("", insert=("50%", "50%"), text_anchor="middle", font_size="24px", fill="red")
    
        # Split the end game message into lines
        lines = s.end_game.split('\n')
        for i, line in enumerate(lines):
            # Add each line as a tspan, adjusting 'dy' for line spacing
            text.add(dwg.tspan(line, x=["50%"], dy=["1.2em"] if i > 0 else ["0em"]))
    
        # Add the complete text element to the drawing
        dwg.add(text)
        return dwg.tostring()


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
                add_image_to_svg(dwg, BSS_CARDS[s.players[role]['cards'][i]], (str(offset) + "%", "76%"), ("20%", "20%"))
            elif role == 2:
                add_image_to_svg(dwg, SE_CARDS[s.players[role]['cards'][i]], (str(offset) + "%", "76%"), ("20%", "20%"))
            elif role == 3:
                add_image_to_svg(dwg, SL_CARDS[s.players[role]['cards'][i]], (str(offset) + "%", "76%"), ("20%", "20%"))
            else:
                add_image_to_svg(dwg, VC_CARDS[s.players[role]['cards'][i]], (str(offset) + "%", "76%"), ("20%", "20%"))
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
    events_start_y = f"{H - 150}px"  # Adjust this value as needed to fit within your SVG dimensions
    line_height = "1.1em"

    line_count = 0  # This will keep track of the total number of lines displayed so far

    for i, event in enumerate(reversed(events_to_display)):
        lines = split_text(event, 100)  # Use your defined max length here
        for j, line in enumerate(lines):
            if i == 0 and j == 0:
                # First line of the first event
                dy_value = "0em"
            else:
                # Calculate 'dy' based on the total lines displayed so far
                dy_value = f"{float(line_height[:-2]) * (line_count + (1 if j == 0 else 0))}em"
            
            dwg.add(dwg.text(line,
                            insert=(events_start_x, events_start_y),
                            text_anchor="start",
                            font_size="8",
                            dy=[dy_value],
                            fill=ROLE_TEXT[role]))
            if j == 0 and not i == 0:
                line_count += 2
            else:
                line_count += 1  # Update the total line count after each line is added

        # After each event, add an extra line's space to separate events
        if i < len(events_to_display) - 1:  # Check to ensure it's not the last event
            line_count += 1  # This adds space equivalent to one extra line



    
    # Add events text to the SVG
    # for i, event in enumerate(reversed(events_to_display)):
    #     dy_value = f"{float(line_height[:-2]) * i}em"
    #     dwg.add(dwg.text(event, insert=(events_start_x, events_start_y), text_anchor="start",
    #                      font_size="8", dy=[dy_value], fill=ROLE_TEXT[role]))

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
    0: "bss_cards/bss_treaty.png",
    1: "bss_cards/bss_factory.png",
    2: "bss_cards/bss_embassy.png",
    3: "bss_cards/bss_technology_research.png",
    4: "bss_cards/bss_blockade.png","
    5: "bss_cards/bss_election.png",
    6: "bss_cards/bss_military_aid.png",
    7: "bss_cards/bss_international_summit.png",
    8: "bss_cards/bss_sabotage.png",
    9: "bss_cards/bss_spy.png",
    10: "bss_cards/bss_posturing.png",
    11: "bss_cards/bss_nuclear_energy.png",
    12: "bss_cards/bss_spy_satellite.png",
    13: "bss_cards/bss_double_agent.png",
    14: "bss_cards/bss_diplomacy.png",
    15: "bss_cards/bss_citizen_uplift.png",
    16: "bss_cards/bss_friendly_neighborhood.png",
    17: "bss_cards/bss_thief.png",
    18: "bss_cards/bss_national_debt.png",
    19: "bss_cards/bss_threat.png"
}

SE_CARDS = {
    0: "se_cards/se_treaty.png",
    1: "se_cards/se_factory.png",
    2: "se_cards/se_embassy.png",
    3: "se_cards/se_technology_research.png",
    4: "se_cards/se_blockade.png",
    5: "se_cards/se_election.png",
    6: "se_cards/se_military_aid.png",
    7: "se_cards/se_international_summit.png",
    8: "se_cards/se_sabotage.png",
    9: "se_cards/se_spy.png",
    10: "se_cards/se_posturing.png",
    11: "se_cards/se_nuclear_energy.png",
    12: "se_cards/se_spy_satellite.png",
    13: "se_cards/se_double_agent.png",
    14: "se_cards/se_diplomacy.png",
    15: "se_cards/se_citizen_uplift.png",
    16: "se_cards/se_friendly_neighborhood.png",
    17: "se_cards/se_thief.png",
    18: "se_cards/se_national_debt.png",
    19: "se_cards/se_threat.png"
}

SL_CARDS = {
    0: "sl_cards/sl_treaty.png",
    1: "sl_cards/sl_factory.png",
    2: "sl_cards/sl_embassy.png",
    3: "sl_cards/sl_technology_research.png",
    4: "sl_cards/sl_blockade.png",
    5: "sl_cards/sl_election.png",
    6: "sl_cards/sl_military_aid.png",
    7: "sl_cards/sl_international_summit.png",
    8: "sl_cards/sl_sabotage.png",
    9: "sl_cards/sl_spy.png",
    10: "sl_cards/sl_posturing.png",
    11: "sl_cards/sl_nuclear_energy.png",
    12: "sl_cards/sl_spy_satellite.png",
    13: "sl_cards/sl_double_agent.png",
    14: "sl_cards/sl_diplomacy.png",
    15: "sl_cards/sl_citizen_uplift.png",
    16: "sl_cards/sl_friendly_neighborhood.png",
    17: "sl_cards/sl_thief.png",
    18: "sl_cards/sl_national_debt.png",
    19: "sl_cards/sl_threat.png"
}

VC_CARDS = {
    0: "vc_cards/vc_treaty.png",
    1: "vc_cards/vc_factory.png",
    2: "vc_cards/vc_embassy.png",
    3: "vc_cards/vc_technology_research.png",
    4: "vc_cards/vc_blockade.png",
    5: "vc_cards/vc_election.png",
    6: "vc_cards/vc_military_aid.png",
    7: "vc_cards/vc_international_summit.png",
    8: "vc_cards/vc_sabotage.png",
    9: "vc_cards/vc_spy.png",
    10: "vc_cards/vc_posturing.png",
    11: "vc_cards/vc_nuclear_energy.png",
    12: "vc_cards/vc_spy_satellite.png",
    13: "vc_cards/vc_double_agent.png",
    14: "vc_cards/vc_diplomacy.png",
    15: "vc_cards/vc_citizen_uplift.png",
    16: "vc_cards/vc_friendly_neighborhood.png",
    17: "vc_cards/vc_thief.png",
    18: "vc_cards/vc_national_debt.png",
    19: "vc_cards/vc_threat.png"
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
