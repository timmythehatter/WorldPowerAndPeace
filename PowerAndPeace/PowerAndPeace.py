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

PLAYERS = {1: {'money': 100, 'reputation': {2: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1, 'activeCards': []},
           2: {'money': 100, 'reputation': {1: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1, 'activeCards': []},
           3: {'money': 100, 'reputation': {1: 100, 2: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 1, 'activeCards': []},
           4: {'money': 100, 'reputation': {1: 100, 2: 100, 3: 100}, 'cards': [], 'stability': 100, 'goalScore': 1, 'activeCards': []}}
           

FACTIONS = {1: 'Black Sun Syndicate',
            2: 'Scarlet Empire',
            3: 'Sapphire League',
            4: 'Viridian Concord'}

CARDS = {0: {'name': 'Treaty', 'cost': 10, 'effect': 'Adds 10 rep to a chosen player and removes 10 rep from their lowest rep player. Costs $10'},
         1: {'name': 'Factory', 'cost': 30, 'effect': 'Generates $10 per turn and adds 1 to goal score. Costs $30'},
         2: {'name': 'Embassy', 'cost': 50, 'effect': 'Generates 10 rep lowest favored country per turn. Costs $50'},
         3: {'name': 'Trade', 'cost': 0, 'effect': 'Increases money by 10 times the number of active cards.'},
         4: {'name': 'Embargo', 'cost': 15, 'effect': 'Drastically reduces rep with a country and reduces their money. Costs $15'},
         5: {'name': 'Election', 'cost': 25, 'effect': 'Increases factional goal score. Costs $25'},
         6: {'name': 'Humanitarian Aid', 'cost': 15, 'effect': 'Increase the stability of another faction by 20. Costs $15'},
         7: {'name': 'Cultural Exchange', 'cost': 25, 'effect': 'Increase reputation with all countries by 10. Costs $25'},
         8: {'name': 'Sabotage', 'cost': 15, 'effect': 'Discards a card from a random opponent. Costs $15'},
         9: {'name': 'Spy', 'cost': 20, 'effect': 'Steals a random card from a chosen opponent. Costs $30'},
         10: {'name': 'Economic Boom', 'cost': 0, 'effect': 'Increase $30 and stability by 20, decrease Reputation with all countries by 5.'},
         11: {'name': 'Inflation Tax', 'cost': 0, 'effect': 'Earn two times the turn number.'},
         12: {'name': 'Plunder', 'cost': 0, 'effect': 'Steal up to $10 from a chosen player. Lose 10 reputation with them.'},
         13: {'name': 'Double Agent', 'cost': 50, 'effect': 'Steal 1 goal achievement from a chosen player and lose 20 reputation with them. If chosen player has no achievements, nothing happens.'},
         14: {'name': 'Diplomat', 'cost': 0, 'effect': 'Earn $1 for every 20 reputation points you have.'}}


for player in PLAYERS.values():
    player['cards'] = random.sample(list(CARDS.keys()), k=3)
    player['cards'].append(0)


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
    state.players[state.whose_turn]['reputation'][chosen_player] += 10
    state.players[chosen_player]['reputation'][state.whose_turn] += 10

    # Decrease the reputation with the least favored player
    state.players[state.whose_turn]['reputation'][least_favored_player] -= 10
    state.players[least_favored_player]['reputation'][state.whose_turn] -= 10

    print('You have increased reputation with player ' + str(chosen_player) + ' and decreased reputation with player ' + str(least_favored_player))
    state.players[state.whose_turn]['money'] -= 10
    state.events.append(FACTIONS[state.whose_turn] + "has played card treaty increasing rep with " + FACTIONS[chosen_player] + 
                        "\n\t and decreasing rep with " + FACTIONS[least_favored_player])
    return True

def card_effect_factory(state, player):
    state.players[state.whose_turn]['activeCards'].append(1)
    state.players[state.whose_turn]['goalScore'] += 1
    state.players[state.whose_turn]['stability'] += 10    
    state.players[state.whose_turn]['money'] -= 30
    state.events.append(FACTIONS[state.whose_turn] + " has created a factory")
    return True

def active_effect_factory(state, owner):
    print("Your factory produces 10 money.")
    state.players[owner]['money'] += 10

def card_effect_embassy(state, player):
    # Generates 10 rep with lowest favored player per turn
    
    state.players[state.whose_turn]['activeCards'].append(2)
    state.players[state.whose_turn]['money'] -= 50
    state.events.append(FACTIONS[state.whose_turn] + " has built an embassy")
    return True
    
def active_effect_embassy(state, owner):
    rep_list = state.players[owner]['reputation']
    least_favored_player_list = [player for player, reputation in rep_list.items() if reputation == min(rep_list.values())]
    least_favored_player = random.choice(least_favored_player_list)

    state.players[owner]['reputation'][least_favored_player] += 10
    print('You have added reputation with player ' + str(least_favored_player))

def card_effect_trade(state, player):
    # Increases money by 10 times the number of active cards. Requires positive rep with a country.
    state.players[state.whose_turn]['money'] += 10 * len(state.players[state.whose_turn]['activeCards'])
    print(FACTIONS[state.whose_turn] + " just made $" + str(10 * len(state.players[state.whose_turn]['activeCards'])) + " through trade.")
    return True

def card_effect_embargo(state, player):
    # Drastically reduces rep with a country and reduces their money
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    state.players[chosen_player]['money'] -= 20
    state.players[state.whose_turn]['reputation'][chosen_player] -= 20
    state.players[state.whose_turn]['stability'] -= 1
    state.players[state.whose_turn]['money'] -= 15
    print(FACTIONS[state.whose_turn] + " has placed an embargo on " + FACTIONS[chosen_player])
    return True

def card_effect_election(state, player):
    # Increases factional goal score
    state.players[state.whose_turn]['goalScore'] += 1
    state.players[state.whose_turn]['stability'] -= 1
    state.players[state.whose_turn]['money'] -= 25
    print(FACTIONS[state.whose_turn] + " just had an election!")
    return True

def card_effect_humanitarian_aid(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    state.players[chosen_player]['stability'] += 20
    state.players[state.whose_turn]['money'] -= 15
    state.events.append(FACTIONS[state.whose_turn] + " just sent humanitarian aid to " + FACTIONS[chosen_player])
    return True

def card_effect_cultural_exchange(state, player):
    for player in state.players[state.whose_turn]['reputation']:
        state.players[state.whose_turn]['reputation'][player] += 10
        state.players[player]['reputation'][state.whose_turn] += 10
    
    state.players[state.whose_turn]['money'] -= 25
    state.events.append(FACTIONS[state.whose_turn] + " just engaged in a cultural exchange.")
    return True

def card_effect_sabotage(state, player):
    random_player = random.choice(list(state.players[state.whose_turn]['reputation'].keys()))
    random_card = random.choice(state.players[random_player]['cards'])
    state.players[random_player]['cards'].remove(random_card)

    print('You have discarded card ' + str(random_card) + ' from player ' + str(random_player) + '!')
    state.players[state.whose_turn]['money'] -= 15
    state.events.append(FACTIONS[state.whose_turn] + " just sabatoged " + FACTIONS[random_player])
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
    state.players[state.whose_turn]['money'] -= 30
    state.events.append(FACTIONS[state.whose_turn] + " has spied on " + FACTIONS[chosen_player])
    return True

def card_effect_economic_boom(state, player):
    state.players[state.whose_turn]['money'] += 20
    state.players[state.whose_turn]['stability'] += 10

    for player in state.players[state.whose_turn]['reputation']:
        state.players[state.whose_turn]['reputation'][player] -= 5
        state.players[player]['reputation'][state.whose_turn] -= 5
    state.events.append(FACTIONS[state.whose_turn] + " just had an economic boom!")
    return True
        
def card_effect_inflation_tax(state, player):
    state.players[state.whose_turn]['money'] += 3 * state.game_turn
    state.events.append(FACTIONS[state.whose_turn] + " just set an inflation tax on their population.")
    return True
    
def card_effect_plunder(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False
    
    # Decrease the reputation with the chosen player
    state.players[state.whose_turn]['reputation'][chosen_player] -= 30
    state.players[chosen_player]['reputation'][state.whose_turn] -= 30

    # take their money
    max = min(state.players[chosen_player]['money'], 30) / 2
    loot = random.randint(0, max)
    state.players[chosen_player]['money'] -= loot
    state.players[state.whose_turn]['money'] += loot
    state.events.append(FACTIONS[state.whose_turn] + " has plundered " + FACTIONS[chosen_player])
    return True
    
def card_effect_double_agent(state, player):
    chosen_player = player
    if chosen_player == -1:
        state.events.append(FACTIONS[state.whose_turn] + " must choose a player to play that card against")
        return False

    # take their goalScore
    goal = min(state.players[chosen_player]['goalScore'], 1)
    if goal == 1:
        # Decrease the reputation with the chosen player
        state.players[state.whose_turn]['reputation'][chosen_player] -= 20
        state.players[chosen_player]['reputation'][state.whose_turn] -= 20
        
        state.players[chosen_player]['goalScore'] -= goal
        state.players[state.whose_turn]['goalScore'] += goal
        state.players[state.whose_turn]['money'] -= 50
        state.events.append(FACTIONS[state.whose_turn] + " planted a double agent against " + FACTIONS[chosen_player])
        return True
    else:
        state.events.append(FACTIONS[state.whose_turn] + " must play that card against someone that has goal score.")
        return False
    
def card_effect_diplomat(state, player):
    favorability = 0
    for player in state.players[state.whose_turn]['reputation']:
        favorability += state.players[state.whose_turn]['reputation'][player]
        print(state.players[state.whose_turn]['reputation'][player])
        print(favorability)
    reward = favorability // 20
    print(reward)
    state.players[state.whose_turn]['money'] += reward
    state.events.append(FACTIONS[state.whose_turn] + "'s diplomatic endeavors were rewarded.")
    return True
    
# clock mechanic
def clock_progression(state):
    minutes = 0
    for player in state.players:
        if state.players[player]['stability'] < 50:
            minutes += 1
            
        if state.players[player]['stability'] > 80:
            minutes -= 1
            
        for other in state.players[player]['reputation']:
            if state.players[player]['reputation'][other] < 45:
                minutes += 0.5
                
            if state.players[player]['reputation'][other] > 75:
                minutes -= 0.5
    state.clock['Minute'] += minutes
    ## TODO: if clock hits midnight, do something

## TODO: Randomize player effects Q
def event_ecologic_disaster(state):
    print("A series of ecological crises erupt all over the globe, causing tensions to rise!")
    print("The doomsday clock advances 15 minutes.")
    state.clock['Minute'] += 15
    for player in state.players:
        if player == 1:
            state.events.append("The Black Sun Syndicate suffers from a serious famine, leading to political instability. Lose 10 stability.")
            state.players[player]['stability'] -= 10
        if player == 2:
            state.events.append("A series of earthquakes tear through the Scarlet Empire, you must rebuild. Lose 20 money.")
            state.players[player]['money'] -= 20
        if player == 3:
            state.events.append("A rogue cyber terrorist organization launches an attack and steals sensitive information from the Sapphire League. Lose 20 reputation with all factions.")
            state.players[player]['reputation'][1] -= 20
            state.players[player]['reputation'][2] -= 20
            state.players[player]['reputation'][4] -= 20
        if player == 4:
            state.events.append("Wildfires sweep large swathes of the Viridian Concord, destroying your infrastructure. Lose an active card.")
            state.players[state.whose_turn]['activeCards'].pop()

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
    state.events.append(message)

            


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
    14: card_effect_diplomat
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
        self.whose_turn = 1
        self.phase = 1
        self.events = []
        self.end_game = ""
        self.game_over = False

        

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
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
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
        new_state.phase = self.phase
        new_state.end_game = self.end_game
        new_state.game_over = self.game_over

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
            self.players[self.whose_turn]['cards'].remove(card)
            news = self.__copy__()  # start with a deep copy.
            news.whose_turn = (news.whose_turn % 4) + 1
            news.players[news.whose_turn]['cards'].append(1)
            if news.whose_turn == 1:
                news.new_turn()
            return news  # return new state

    def is_goal(self):
        '''WIP: Checks if the current state is a goal state.'''
        return self.clock['Minute'] >= 60 or self.game_over
            
        
    
    def new_turn(self):
        clock_progression(self)
        print("Phase: " + str(self.phase))
        self.game_turn += 1
        if self.game_turn == 2 and self.whose_turn == 1:
            self.game_over = True
            goal_message(self)
        if self.game_turn == 4:
            self.phase += 1
            event_ecologic_disaster(self)
        if self.game_turn == 7:
            self.phase += 1
            event_political_assassination(self)
        if self.game_turn == 10:
            self.phase += 1
            print("Doomsday has arrived!")
            doomsday = random.randint(1, 4)

        for player in self.players:
            for card in self.players[player]['activeCards']:
                ACTIVE_EFFECTS[card](self, player)

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
  
OPERATORS = op_play_card
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