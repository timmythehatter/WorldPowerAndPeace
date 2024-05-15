import random

# <METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "World Power and Peace"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['A Team']
PROBLEM_CREATION_DATE = "21-April-2024"
PROBLEM_DESC = \
    '''4 player game power and peace game
'''

# </METADATA>

# <COMMON_DATA>

CLOCK = {'Hour': 11 , 'Minute': 00}

PLAYERS = {1: {'money': 100, 'reputation': {2: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1.0, 'activeCards': []},
           2: {'money': 100, 'reputation': {1: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1.0, 'activeCards': []},
           3: {'money': 100, 'reputation': {1: 100, 2: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1.0, 'activeCards': []},
           4: {'money': 100, 'reputation': {1: 100, 2: 100, 3: 100}, 'cards': [], 'stability': 100, 'goalScore': 1.0, 'activeCards': []}}
           

FACTIONS = {-1: 'Game Start',
            1: 'Black Sun Syndicate',
            2: 'Scarlet Empire',
            3: 'Sapphire League',
            4: 'Viridian Concord'}

CARDS = {
         # neutral
         0: {'name': 'Treaty', 'cost': 10, 'effect': 'Adds 20 rep to a chosen player and removes 10 rep from their lowest rep player. Costs $10', 'alignment': 0},
         # neutral
         1: {'name': 'Factory', 'cost': 50, 'effect': 'Generates $10 per turn and adds 1 to goal score. Costs $50', 'alignment': 0},
         # positive
         2: {'name': 'Embassy', 'cost': 50, 'effect': 'Generates 5 rep lowest favored country per turn. Costs $50', 'alignment': 1},
         # positive
         3: {'name': 'Technology Research', 'cost': 30, 'effect': 'Increases money by 10 times the number of active cards. Costs $30', 'alignment': 1},
         # negative
         4: {'name': 'Blockade', 'cost': 15, 'effect': 'Drastically reduces rep with a country and reduces their money by $30. Costs $10', 'alignment': -1},
         # neutral
         5: {'name': 'Election', 'cost': 25, 'effect': 'Increases factional goal score. Costs $25', 'alignment': 0},
         # positive
         6: {'name': 'Military Aid', 'cost': 15, 'effect': 'Increase the stability of another chosen faction by 20. Costs $40', 'alignment': 1},
         # positive
         7: {'name': 'International Summit', 'cost': 25, 'effect': 'Increase reputation with all countries by 10. Costs $50', 'alignment': 1},
         # negative
         8: {'name': 'Sabotage', 'cost': 5, 'effect': 'Discards a card from a random opponent. Costs $5', 'alignment': -1},
         # negative
         9: {'name': 'Spy', 'cost': 10, 'effect': 'Steals a random card from a chosen opponent. Costs $10', 'alignment': -1},
         # neutral
         10: {'name': 'Posturing', 'cost': 0, 'effect': 'Gain $30 and increase stability by 20, decrease Reputation with all countries by 15.', 'alignment': -1},
         # neutral
         11: {'name': 'Nuclear Energy', 'cost': 0, 'effect': 'Earn $10 times the turn number but reduces stability by the same amount.', 'alignment': 0},
         # negative
         12: {'name': 'Spy Satellite', 'cost': 0, 'effect': 'Steal a random amount from $0 - $100 from a chosen player. Lose 20 reputation with them.', 'alignment': -1},
         # negative
         13: {'name': 'Double Agent', 'cost': 20, 'effect': 'Steal some goal achievement from a chosen player and lose 20 reputation with them. Costs $20', 'alignment': -1},
         # positive
         14: {'name': 'Diplomacy', 'cost': 0, 'effect': 'Earn $1 for every 30 reputation points you have.', 'alignment': 1},
         # positive
         15: {'name': 'Citizen Uplift', 'cost': 20, 'effect': 'Gain 0.1 goal score for 100 stability, and 0.1 for any additional 50 stability. Costs $20', 'alignment': 1},
         # positive
         16: {'name': 'Friendly Neighborhood', 'cost': 0, 'effect': 'Increase money by the sum of reputation with other factions.', 'alignment': 1},
         # negative
         17: {'name': 'Thief', 'cost': 0, 'effect': 'Steal $20 from a random player. Lose 20 reputation with them.', 'alignment': -1},
         # negative
         18: {'name': 'National Debt', 'cost': 0, 'effect': 'Increase your $50 by decreasing 30 stability.', 'alignment': -1},
         # negative
         19: {'name': 'Threat', 'cost': 20, 'effect': 'Gain 50 stability by decreasing another countrys stability and reputation by 30 and 20 respectively.', 'alignment': -1}}


for player in PLAYERS.values():
    player['cards'] = random.sample(list(CARDS.keys()), k=5)
    
def deal_cards(state):
    for player in state.players.values():
        player['cards'] = random.sample(list(CARDS.keys()), k=5)

def alot_money(state):
    for player in state.players.values():
        player['money'] += 100

def card_effect_treaty(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False

    # Find the least favored player from the perspective of the chosen player
    # First we get the reputation list of current player to other players as rep_list.
    # Then, we extract the least_favored_player_list of player(s) 
    # with the lowest reputation from th current player.
    # Lastly, we will choose a random player from the list as the least_favored_player.
    rep_list = dict(state.players[chosen_player]['reputation'])
    if state.whose_turn in rep_list:
        del rep_list[state.whose_turn]
    least_favored_player_list = [player for player, reputation in rep_list.items() if reputation == min(rep_list.values())]
    least_favored_player = random.choice(least_favored_player_list)

    # Increase the reputation with the chosen player
    state.players[state.whose_turn]['reputation'][chosen_player] += 20
    state.players[chosen_player]['reputation'][state.whose_turn] += 20

    # Decrease the reputation with the least favored player
    state.players[state.whose_turn]['reputation'][least_favored_player] -= 10
    state.players[least_favored_player]['reputation'][state.whose_turn] -= 10

    print('You have increased reputation with player ' + str(chosen_player) + ' and decreased reputation with player ' + str(least_favored_player))
    state.players[state.whose_turn]['money'] -= 10
    state.events.append(FACTIONS[state.whose_turn] + " has played card treaty increasing rep with " + FACTIONS[chosen_player] + 
                        "\n\t and decreasing rep with " + FACTIONS[least_favored_player])
    return True

def card_effect_factory(state, player):
    state.players[state.whose_turn]['activeCards'].append(1)
    state.players[state.whose_turn]['goalScore'] += 1
    state.players[state.whose_turn]['stability'] += 10    
    state.players[state.whose_turn]['money'] -= 50
    state.events.append(FACTIONS[state.whose_turn] + " has created a factory which produces $10 every turn")
    return True

def active_effect_factory(state, owner):
    print("Your factory produces 10 money.")
    state.players[owner]['money'] += 10

def card_effect_embassy(state, player):
    # Generates 10 rep with lowest favored player per turn
    
    state.players[state.whose_turn]['activeCards'].append(2)
    state.players[state.whose_turn]['money'] -= 50
    state.events.append(FACTIONS[state.whose_turn] + " has built an embassy generating 5 rep with their lowest rep faction every turn")
    return True
    
def active_effect_embassy(state, owner):
    rep_list = state.players[owner]['reputation']
    least_favored_player_list = [player for player, reputation in rep_list.items() if reputation == min(rep_list.values())]
    least_favored_player = random.choice(least_favored_player_list)

    state.players[owner]['reputation'][least_favored_player] += 5
    print('You have added reputation with player ' + str(least_favored_player))

def card_effect_trade(state, player):
    # Increases money by 10 times the number of active cards.
    state.players[state.whose_turn]['money'] += 10 * len(state.players[state.whose_turn]['activeCards']) - 30
    state.events.append(FACTIONS[state.whose_turn] + " just made $" + str(10 * len(state.players[state.whose_turn]['activeCards'])) + " through trade.")
    return True

def card_effect_embargo(state, player):
    # Drastically reduces rep with a country and reduces their money
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    state.players[chosen_player]['money'] -= 30
    state.players[state.whose_turn]['reputation'][chosen_player] -= 20
    state.players[chosen_player]['reputation'][state.whose_turn] -= 20
    state.players[state.whose_turn]['money'] -= 10
    state.events.append(FACTIONS[state.whose_turn] + " has placed an embargo on " + FACTIONS[chosen_player] + " reducing their $ by 30.")
    return True

def card_effect_election(state, player):
    # Increases factional goal score
    state.players[state.whose_turn]['goalScore'] += .1
    state.players[state.whose_turn]['money'] -= 25
    print(FACTIONS[state.whose_turn] + " just had an election slightly increasing their goal score!")
    return True

def card_effect_humanitarian_aid(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    state.players[chosen_player]['stability'] += 20
    state.players[state.whose_turn]['money'] -= 40
    state.events.append(FACTIONS[state.whose_turn] + " just sent military aid to " + FACTIONS[chosen_player] + " which helped restore stability.")
    return True

def card_effect_cultural_exchange(state, player):
    for player in state.players[state.whose_turn]['reputation']:
        state.players[state.whose_turn]['reputation'][player] += 10
        state.players[player]['reputation'][state.whose_turn] += 10
    
    state.players[state.whose_turn]['money'] -= 50
    state.events.append(FACTIONS[state.whose_turn] + " just engaged in a cultural exchange increasing rep with all factions.")
    return True

def card_effect_sabotage(state, player):
    random_player = random.choice(list(state.players[state.whose_turn]['reputation'].keys()))
    random_card = random.choice(state.players[random_player]['cards'])
    state.players[random_player]['cards'].remove(random_card)
    state.players[state.whose_turn]['money'] -= 5
    state.events.append(FACTIONS[state.whose_turn] + " just sabatoged " + FACTIONS[random_player] + " and destroyed one of their cards!")
    return True

def card_effect_spy(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False

    player_cards = state.players[chosen_player]['cards']
    card = random.choice(player_cards)

    state.players[chosen_player]['cards'].remove(card)
    state.players[state.whose_turn]['cards'].append(card)
    state.players[state.whose_turn]['money'] -= 10
    state.events.append(FACTIONS[state.whose_turn] + " has spied on " + FACTIONS[chosen_player] + " and stolen one of their cards.")
    return True

def card_effect_economic_boom(state, player):
    state.players[state.whose_turn]['money'] += 30
    state.players[state.whose_turn]['stability'] += 20

    for player in state.players[state.whose_turn]['reputation']:
        state.players[state.whose_turn]['reputation'][player] -= 15
        state.players[player]['reputation'][state.whose_turn] -= 15
    state.events.append(FACTIONS[state.whose_turn] + " just had an economic boom increasing their money and stability but decreasing their rep!")
    return True
        
def card_effect_inflation_tax(state, player):
    state.players[state.whose_turn]['stability'] -= 10 * state.game_turn
    state.players[state.whose_turn]['money'] += 10 * state.game_turn
    state.events.append(FACTIONS[state.whose_turn] + " just set an inflation tax on their population increasing their money, but decreasing their stability.")
    return True
    
def card_effect_plunder(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    
    # Decrease the reputation with the chosen player
    state.players[state.whose_turn]['reputation'][chosen_player] -= 20
    state.players[chosen_player]['reputation'][state.whose_turn] -= 20

    # take their money
    max = min(state.players[chosen_player]['money'], 100)
    loot = random.randint(0, max)
    state.players[chosen_player]['money'] -= loot
    state.players[state.whose_turn]['money'] += loot
    state.events.append(FACTIONS[state.whose_turn] + " has plundered " + FACTIONS[chosen_player] + " and stole $" + str(loot))
    return True
    
def card_effect_double_agent(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False

    # take their goalScore

    # Decrease the reputation with the chosen player
    state.players[state.whose_turn]['reputation'][chosen_player] -= 20
    state.players[chosen_player]['reputation'][state.whose_turn] -= 20
    
    state.players[chosen_player]['goalScore'] -= .1
    state.players[state.whose_turn]['goalScore'] += .1
    state.players[state.whose_turn]['money'] -= 20
    state.events.append(FACTIONS[state.whose_turn] + " planted a double agent against " + FACTIONS[chosen_player] + " and stole some of their goal score.")
    return True
    
def card_effect_diplomat(state, player):
    favorability = 0
    for player in state.players[state.whose_turn]['reputation']:
        favorability += state.players[state.whose_turn]['reputation'][player]
    reward = favorability // 30
    print(reward)
    state.players[state.whose_turn]['money'] += reward
    state.events.append(FACTIONS[state.whose_turn] + "'s diplomatic endeavors were rewarded and they earned some $.")
    return True

def card_effect_citizen_uplift(state, player):
    stability = state.players[state.whose_turn]['stability']
    state.players[state.whose_turn]['money'] -= 20

    if stability < 100:
        return True

    goalScore += 0.1
    goalScore += int((stability - 100) / 50) / 10

    print(goalScore)
    state.players[state.whose_turn]['goalScore'] += goalScore

    print(str(FACTIONS[state.whose_turn]) + " has added goal score to their national goal due to citizen stability.")
    state.events.append(FACTIONS[state.whose_turn] + " has added goal score to their national goal due to citizen stability.")
    return True

def card_effect_friendly_neighborhood(state, player):
    sum = 0

    for player in state.players[state.whose_turn]['reputation']:
        additional = state.players[state.whose_turn]['reputation'][player] - 100
        sum += additional
    
    state.players[state.whose_turn]['money'] += sum

    print(str(FACTIONS[state.whose_turn]) + " has been rewarded $ for their reputation.")
    state.events.append(FACTIONS[state.whose_turn] + " has been rewarded $ for their reputation.")
    return True

def card_effect_thief(state, player):
    random_player = random.choice(list(state.players[state.whose_turn]['reputation'].keys()))

    state.players[random_player]['money'] -= 20
    state.players[state.whose_turn]['money'] += 20

    state.players[random_player]['reputation'][state.whose_turn] -= 20
    state.players[state.whose_turn]['reputation'][random_player] -= 20
    
    print(str(FACTIONS[state.whose_turn]) + " has stolen $ from " + str(FACTIONS[random_player]) + '! Their relationship has worsen..')
    state.events.append(FACTIONS[state.whose_turn] + " has stolen $ from " + FACTIONS[random_player] + '! Their relationship has worsen..')
    return True

def card_effect_national_debt(state, player):
    state.players[state.whose_turn]['money'] += 50
    state.players[state.whose_turn]['stability'] -= 30

    print(str(FACTIONS[state.whose_turn]) + " has increased $ by decreasing country stability.")
    state.events.append(FACTIONS[state.whose_turn] + " has increased $ by decreasing country stability.")
    return True

def card_effect_threat(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False

    state.players[chosen_player]['reputation'][state.whose_turn] -= 20
    state.players[state.whose_turn]['reputation'][chosen_player] -= 20

    state.players[chosen_player]['stability'] -= 30
    state.players[state.whose_turn]['stability'] += 50

    state.players[state.whose_turn]['money'] -= 20
    print(str(FACTIONS[state.whose_turn]) + " has threaten " + str(FACTIONS[chosen_player]) + " and caused national unstability.")
    state.events.append(FACTIONS[state.whose_turn] + " has threaten " + FACTIONS[chosen_player] + " and caused national unstability.")
    return True
    
# clock mechanic
def clock_progression(state):
    minutes = 0
    threshold = -5 + 2 * state.phase

    nuclearMeasure = state.roundAlignment

    # Define narrative strings based on the phase of the game and actions taken
    phase_narratives = {
        1: {
            'positive': "Diplomatic dialogues open across continents, promising beginnings of peace and cooperation.",
            'negative': "Minor territorial disputes begin to emerge, stirring up regional tensions."
        },
        2: {
            'positive': "International trade agreements strengthen economies and build trust among nations.",
            'negative': "Cyber-attacks on critical infrastructure sow discord and suspicion among allies."
        },
        3: {
            'positive': "Global conferences set ambitious goals for climate action, uniting nations in a common cause.",
            'negative': "Resource shortages lead to skirmishes over water and minerals, escalating global tensions."
        },
        4: {
            'positive': "Humanitarian aid missions strengthen bonds and improve international relations.",
            'negative': "Proxy wars intensify, drawing in surrounding nations and destabilizing entire regions."
        },
        5: {
            'positive': "Breakthroughs in renewable energy reduce dependence on fossil fuels, easing geopolitical pressures.",
            'negative': "An arms race escalates as nations ramp up their nuclear arsenals."
        },
        6: {
            'positive': "Successful peace talks result in landmark treaties, significantly easing global tensions.",
            'negative': "Assassination of a high-profile leader throws the world into chaos, spiking tensions dramatically."
        },
        7: {
            'positive': "Major powers lead a global disarmament initiative, heralding a new era of peace.",
            'negative': "Nationalist movements gain momentum, leading to increased isolationism and fractured international relations."
        },
        8: {
            'positive': "Technological cooperation leads to a boom in global communication and understanding.",
            'negative': "Espionage and intelligence leaks lead to major diplomatic breakdowns."
        },
        9: {
            'positive': "Global health initiatives eradicate diseases and lift health standards, fostering international goodwill.",
            'negative': "Economic sanctions cripple several smaller nations, causing humanitarian crises and international condemnation."
        },
        10: {
            'positive': "Cultural exchanges and international arts programs foster a shared sense of global community.",
            'negative': "Religious and ideological conflicts flare up, leading to widespread civil unrest."
        },
        11: {
            'positive': "Global consensus on human rights advances leads to better treatment of minorities and refugees.",
            'negative': "Terrorist attacks on major cities rekindle old enmities and fear, pushing nations apart."
        },
        12: {
            'positive': "A historic summit results in a significant reduction in global military expenditures.",
            'negative': "A false alarm about a missile strike nearly triggers a nuclear war, dramatically advancing the doomsday clock."
        }
    }

    # Determine the narrative based on round alignment and phase
    if nuclearMeasure < threshold:
        minutes += abs(threshold) + abs(nuclearMeasure)
        narrative = phase_narratives[state.game_turn]['negative']
        state.phase_events.append(narrative + " The doomsday clock was advanced by " + str(minutes) + " minutes due to the actions of the nations in the past turn.")
    else:
        narrative = phase_narratives[state.game_turn]['positive']
        state.phase_events.append(narrative + " The doomsday clock remains steady, reflecting a cautious optimism due to the actions of the nations in the past turn.")

    # Check player stability and reputations
    for player in state.players:
        if state.players[player]['stability'] < 50:
            minutes += 1
            state.phase_events.append(FACTIONS[player] + " faces internal turmoil, contributing to instability.")
        bad_rep = False
        for other in state.players[player]['reputation']:
            if state.players[player]['reputation'][other] < 50:
                minutes += 0.5
                bad_rep = True
        if bad_rep:
            state.phase_events.append(FACTIONS[player] + " has deteriorating relations, adding to global tensions.")
        if state.players[player]['money'] < 0:
            state.phase_events.append(FACTIONS[player] + " is having significant economic problems thus reducing their stability proportionately.")
            state.players[player]['stability'] -= state.players[player]['money']

    # Update the clock based on the calculated minutes
    state.clock['Minute'] += minutes
    ## TODO: if clock hits midnight, do something

## TODO: Randomize player effects Q
def event_ecologic_disaster(state):
    print("A series of ecological crises erupt all over the globe, causing tensions to rise!")
    print("The doomsday clock advances 15 minutes.")
    state.clock['Minute'] += 15
    for player in state.players:
        if player == 1:
            state.phase_events.append("The Black Sun Syndicate suffers from a serious famine, leading to political instability. Lose 10 stability.")
            state.players[player]['stability'] -= 10
        if player == 2:
            state.phase_events.append("A series of earthquakes tear through the Scarlet Empire, you must rebuild. Lose 20 money.")
            state.players[player]['money'] -= 20
        if player == 3:
            state.phase_events.append("A rogue cyber terrorist organization launches an attack and steals sensitive information from the Sapphire League. Lose 20 reputation with all factions.")
            state.players[player]['reputation'][1] -= 20
            state.players[player]['reputation'][2] -= 20
            state.players[player]['reputation'][4] -= 20
        if player == 4:
            state.phase_events.append("Wildfires sweep large swathes of the Viridian Concord, destroying your infrastructure. Lose an active card.")
            if state.players[player]['activeCards']:
                state.players[player]['activeCards'].pop()

def event_political_assassination(state):
    state.clock['Minute'] += 15
    max_stability = -float('inf')
    min_stability = float('inf')
    max_stability_player = None
    min_stability_player = None

    for player in state.players:
        if state.players[player]['stability'] > max_stability:
            max_stability = state.players[player]['stability']
            max_stability_player = player
        elif state.players[player]['stability'] < min_stability:
            min_stability = state.players[player]['stability']
            min_stability_player = player
    
    state.players[max_stability_player]['stability'] = min_stability
    state.players[min_stability_player]['stability'] = max_stability
    for i in range(1, 5):
        if i != min_stability_player:
            state.players[min_stability_player]['reputation'][i] -= 30
    
    message = "Political instability in the " + state.factions[min_stability_player] + " have reached a boiling point.\n"
    message += "Conspirators within the faction have conspired to demonstrate power by orchestarting an assassination of the leader of the " + state.factions[max_stability_player] + ".\n"
    message += "As a consequence, political power in the " + state.factions[min_stability_player] + " has consolidated around the rebel conspirators, resulting in a more stable"
    message += " balance of power, at the cost of the factions reputation around the world.\nMeanwhile, political turmoil and infighting racks the formerly stable " + state.factions[max_stability_player] + ".\n"
    message += "The situation grows more perilous, and the doomsday clock advances 15 minutes closer to midnight."    
    state.phase_events.append(message)

            


CARD_EFFECTS = {
    0: card_effect_treaty,
    1: card_effect_factory,
    2: card_effect_embassy,
    3: card_effect_trade,
    4: card_effect_embargo,
    5: card_effect_election,
    6: card_effect_humanitarian_aid,
    7: card_effect_cultural_exchange,
    8: card_effect_sabotage,
    9: card_effect_spy,
    10: card_effect_economic_boom,
    11: card_effect_inflation_tax,
    12: card_effect_plunder,
    13: card_effect_double_agent,
    14: card_effect_diplomat,
    15: card_effect_citizen_uplift,
    16: card_effect_friendly_neighborhood,
    17: card_effect_thief,
    18: card_effect_national_debt,
    19: card_effect_threat
}

ACTIVE_EFFECTS = {
    1: active_effect_factory,
    2: active_effect_embassy
}

# </COMMON_DATA>

# <COMMON_CODE>
class State():
    def __init__(self):
        self.game_turn = 1
        self.players = PLAYERS
        self.cards = CARDS
        self.clock = CLOCK
        self.factions = FACTIONS
        self.whose_turn = -1
        self.phase = 1
        self.events = []
        self.phase_events = []
        self.end_game = ""
        self.game_over = False
        self.roundAlignment = 0

        

    def __eq__(self, s2):
        for p in self.players:
            if self.players[p]['money'] != s2.players[p]['money']:
                return False
            for card in self.players[p]['cards']:
                if card not in s2.players[p]['cards']:
                    return False
            if self.players[p]['stability'] != s2.players[p]['stability']:
                return False
            if self.players[p]['goalScore'] != s2.players[p]['goalScore']:
                return False
            for card in self.players[p]['activeCards']:
                if card not in s2.players[p]['activeCards']:
                    return False
            if self.whose_turn != s2.whose_turn:
                return False
            if self.game_turn != s2.game_turn:
                return False
            if self.clock != s2.clock:
                return False
            if self.cards != s2.cards:
                return False 
            if self.phase != s2.phase:
                return False
            if self.roundAlignment != s2.roundAlignment:
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        if self.whose_turn == -1:
            return 'It is the start of the game or a phase change'
        txt = "Current Player: " + self.factions[self.whose_turn] + "\n"
        # for p in self.players:
        #     txt += "Player " + str(p) + ":\n"
        curr = self.players[self.whose_turn]
        txt += "Money: " + str(curr['money']) + "\n"
        for other_player in self.players[self.whose_turn]:
            if other_player != 'money' and other_player != 'cards' and other_player != 'activeCards' and other_player != 'goalScore' and other_player != 'stability':
                    txt += "Player " + str(other_player) + " rep: " + str(self.players[self.whose_turn][other_player]) + "\n"
        txt += "Goal Score: " + str(curr['goalScore']) + "\n"
        txt += "Stability: " + str(curr['stability']) + "\n"
        txt += "Game Turn: " + str(self.game_turn) + "\n"
        txt += "Clock: " + str(self.clock['Hour']) + ":" + str(self.clock['Minute']) + "\n"
        txt += "Cards: " + str(curr['cards']) + "\n"
        txt += "Active Cards: " + str(curr['activeCards']) + "\n"

        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        new_state = State()
        new_state.players = {p: self.players[p].copy() for p in self.players}
        new_state.whose_turn = self.whose_turn
        new_state.cards = self.cards
        new_state.clock = self.clock
        new_state.game_turn = self.game_turn
        new_state.factions = self.factions
        new_state.events = self.events
        new_state.phase_events = self.phase_events
        new_state.phase = self.phase
        new_state.end_game = self.end_game
        new_state.game_over = self.game_over
        new_state.roundAlignment = self.roundAlignment

        return new_state

    def can_move(self, role, card):
        '''Tests if the player has enough money to use the given card.'''
        if not (self.whose_turn-1) == role:
            return False
        try:
            if card in self.players[self.whose_turn]['cards']:
               return True
            else:
               return False
        except (Exception) as e:
            print(e)

    def move(self, card, player):
        # Procedure for moving from one game state to next
        if card not in self.players[self.whose_turn]['cards']:
            self.events.append(FACTIONS[self.whose_turn] + " does not have that card. Play a card you have")
            return self
        elif player == self.whose_turn:
            self.events.append(FACTIONS[self.whose_turn] + " can't play a card against themself.")
            return self
        else:
            played = CARD_EFFECTS[card](self, player)
            if not played:
                return self
            self.roundAlignment += CARDS[card]['alignment']
            self.players[self.whose_turn]['cards'].remove(card)
            news = self.__copy__()  # start with a deep copy.
            news.whose_turn = (news.whose_turn % 4) + 1
            if news.whose_turn == 1:
                news.new_turn()
            return news  # return new state

    def is_goal(self):
        '''WIP: Checks if the current state is a goal state.'''
        return self.clock['Minute'] >= 60 or self.game_over
            
        
    
    def new_turn(self):
        self.phase_events = []
        self.whose_turn = -1
        clock_progression(self)
        self.roundAlignment = 0
        print("Phase: " + str(self.phase))
        self.game_turn += 1
        if self.game_turn == 13 and self.whose_turn == 1:
            self.game_over = True
            goal_message(self)
        if self.game_turn == 4:
            alot_money(self)
            deal_cards(self)
            self.phase += 1
            event_ecologic_disaster(self)
        if self.game_turn == 7:
            alot_money(self)
            deal_cards(self)
            self.phase += 1
            event_political_assassination(self)
        if self.game_turn == 10:
            alot_money(self)
            deal_cards(self)
            self.phase += 1
            print("Doomsday has arrived!")
            doomsday = random.randint(1, 4)

        for player in self.players:
            for card in self.players[player]['activeCards']:
                ACTIVE_EFFECTS[card](self, player)

    def can_proceed(self, role):
        return self.whose_turn == -1
    
    def proceed(self):
        news = self.__copy__()
        news.whose_turn = 1
        return news

def goal_message(self):
    if self.clock['Minute'] >= 60:
        end_game_messsage = "A nuclear war has broken out. There are no winners, only survivors."
        self.end_game = end_game_messsage
        return end_game_messsage
    else:
        # Calculate the scores for each player based on the provided formula
        scores = {}
        for player_id, info in self.players.items():
            rep_sum = sum(info['reputation'].values())  # sum of reputations with other players
            score = info['goalScore'] * (rep_sum + info['money'] + info['stability'])
            scores[player_id] = score
        
        # Sort scores in descending order to rank players
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        ranking_message = "Game over! Here are the player rankings:\n"
        for rank, (player_id, score) in enumerate(sorted_scores, start=1):
            faction_name = self.factions[player_id]
            ranking_message += f"{rank}. {faction_name} with a score of {score}\n"

        self.end_game = ranking_message
        return ranking_message

SESSION = None
def get_session():
    return SESSION

# </COMMON_CODE>

from soluzion import Basic_Operator


#<OPERATORS>  #---------------------
class Operator(Basic_Operator):
  def __init__(self, name, precond, state_transf):
    super().__init__(
        name = name,
        precond = precond,
        transf = state_transf,
        params=[
            {
                "name": "Chosen Player",
                "type": "int",
            }
        ],
    )

  def is_applicable(self, s, role_number=0):
    return self.precond(s, role=role_number)

  

  
op_play_card = [Operator(
    "Play card " + CARDS[card_id]['name'] + " with effect " + CARDS[card_id]['effect'],
    lambda s, role=0, card_id=card_id: s.can_move(role, card_id),
    lambda s, params, card_id=card_id: s.move(card_id, params)
    )
        for card_id in CARDS]

op_start_game = [Operator(
    "I have read the story and wish to proceed",
    lambda s, role=0: s.can_proceed(role),
    lambda s, params: s.proceed()
)]
  
OPERATORS = op_play_card + op_start_game
# </OPERATORS>

#<INITIAL_STATE>
INITIAL_STATE = None

INITIAL_STATE = State()
print(INITIAL_STATE)
#</INITIAL_STATE>


#<ROLES>
ROLES = [
    {'name': 'Black Sun Syndicate', 'min': 1, 'max': 1},
    {'name': 'Scarlet Empire', 'min': 1, 'max': 1},
    {'name': 'Sapphire League', 'min': 1, 'max': 1},
    {'name': 'Viridian Concord', 'min': 1, 'max': 1},
    {'name': 'Observer', 'min': 0, 'max': 25}
]

#</ROLES>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
BRIFL_SVG = True # The program FoxAndGeese_SVG_VIS_FOR_BRIFL.py is available
render_state = None
def use_BRIFL_SVG():
  global render_state
  from  SVG_VIS import render_state
#</STATE_VIS>