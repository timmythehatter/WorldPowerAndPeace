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

PLAYERS = {1: {'money': 100, 'reputation': {2: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           2: {'money': 100, 'reputation': {1: 100, 3: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           3: {'money': 100, 'reputation': {1: 100, 2: 100, 4: 100}, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           4: {'money': 100, 'reputation': {1: 100, 2: 100, 3: 100}, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []}}
           

FACTIONS = {1: 'Black Sun Syndicate (1)',
            2: 'Scarlet Empire (2)',
            3: 'Sapphire League (3)',
            4: 'Viridian Concord (4)'}

CARDS = {0: {'name': 'Treaty', 'cost': 10, 'effect': 'Adds 10 rep to a chosen player and removes 10 rep from their lowest rep player. Costs $10'},
         1: {'name': 'Factory', 'cost': 30, 'effect': 'Generates $10 per turn and adds 1 to goal score. Costs $30'},
         2: {'name': 'Embassy', 'cost': 50, 'effect': 'Generates 10 rep lowest favored country per turn. Costs $50'},
         3: {'name': 'Trade', 'cost': 0, 'effect': 'Increases money by 10 times the number of active cards.'},
         4: {'name': 'Embargo', 'cost': 15, 'effect': 'Drastically reduces rep with a country and reduces their money. Costs $15'},
         5: {'name': 'Election', 'cost': 25, 'effect': 'Increases factional goal score. Costs $25'},
         6: {'name': 'Humanitarian Aid', 'cost': 15, 'effect': 'Increase the stability of another faction by 20. Costs $15'},
         7: {'name': 'Cultural Exchange', 'cost': 25, 'effect': 'Increase reputation with all countries by 10. Costs $25'},
         8: {'name': 'Sabotage', 'cost': 15, 'effect': 'Discards a card from a random opponent. Costs $15'}}


for player in PLAYERS.values():
    player['cards'] = random.sample(list(CARDS.keys()), k=3)


def card_effect_treaty(state):
    chosen_player = int(input("Choose a player to make a treaty with: "))

    # Find the least favored player from the perspective of the chosen player
    # First we get the reputation list of current player to other players as rep_list.
    # Then, we extract the least_favored_player_list of player(s) 
    # with the lowest reputation from th current player.
    # Lastly, we will choose a random player from the list as the least_favored_player.
    rep_list = state.players[state.current_player]['reputation']
    least_favored_player_list = [player for player, reputation in rep_list.items() if reputation == min(rep_list.values())]
    least_favored_player = random.choice(least_favored_player_list)

    # Increase the reputation with the chosen player
    state.players[state.current_player]['reputation'][chosen_player] += 10
    state.players[chosen_player]['reputation'][state.current_player] += 10

    # Decrease the reputation with the least favored player
    state.players[state.current_player]['reputation'][least_favored_player] -= 10
    state.players[least_favored_player]['reputation'][state.current_player] -= 10

    print('You have increased reputation with player ' + str(chosen_player) + ' and decreased reputation with player ' + str(least_favored_player))
    state.players[state.current_player]['money'] -= 10

def card_effect_factory(state):
    state.players[state.current_player]['activeCards'].append(1)
    state.players[state.current_player]['goalScore'] += 1
    state.players[state.current_player]['stability'] += 10    

def active_effect_factory(state):
    print("Your factory produces 10 money.")
    state.players[state.current_player]['money'] += 10

def card_effect_embassy(state):
    # Generates 10 rep with lowest favored player per turn
    state.players[state.current_player]['activeCards'].append(2)
    state.players[state.current_player]['money'] -= 50
    
def active_effect_embassy(state):
    rep_list = state.players[state.current_player]['reputation']
    least_favored_player_list = [player for player, reputation in rep_list.items() if reputation == min(rep_list.values())]
    least_favored_player = random.choice(least_favored_player_list)

    state.players[state.current_player]['reputation'][least_favored_player] += 10
    print('You have added reputation with player ' + str(least_favored_player))

def card_effect_trade(state):
    # Increases money by 10 times the number of active cards. Requires positive rep with a country.
    state.players[state.current_player]['money'] += 10 * len(state.players[state.current_player]['activeCards'])

def card_effect_embargo(state):
    # Drastically reduces rep with a country and reduces their money
    chosen_player = int(input("Choose a player to impose embargo: "))
    state.players[chosen_player]['money'] -= 20
    state.players[state.current_player]['reputation'][chosen_player] -= 20
    state.players[state.current_player]['stability'] -= 1

def card_effect_election(state):
    # Increases factional goal score
    state.players[state.current_player]['goalScore'] += 2
    state.players[state.current_player]['stability'] -= 1
    state.players[state.current_player]['money'] -= 25

def card_effect_humanitarian_aid(state):
    chosen_player = int(input("Choose a player to send aid: "))
    state.players[chosen_player]['stability'] += 20

def card_effect_cultural_exchange(state):
    for player in state.players[state.current_player]['reputation']:
        state.players[state.current_player]['reputation'][player] += 10
        state.players[player]['reputation'][state.current_player] += 10
    
    state.players[state.current_player]['money'] -= 25
    

def card_effect_sabotage(state):
    random_player = random.choice(list(state.players[state.current_player]['reputation'].keys()))
    random_card = random.choice(state.players[random_player]['cards'])
    state.players[random_player]['cards'].remove(random_card)

    print('You have discarded card ' + str(random_card) + ' from player ' + str(random_player) + '!')
    state.players[state.current_player]['money'] -= 15



## TODO: Randomize player effects 
def event_ecologic_disaster(state):
    print("A series of ecological crises erupt all over the globe, causing tensions to rise!")
    print("The doomsday clock advances 15 minutes.")
    state.clock['Minute'] += 15
    for player in state.players:
        if player == 1:
            print("Your region suffers from a serious famine, leading to political instability. Lose 10 stability.")
            state.players[player]['stability'] -= 10
        if player == 2:
            print("A series of earthquakes tear through your region, you must rebuild. Lose 20 money.")
            state.players[player]['money'] -= 20
        if player == 3:
            print("Your advanced technology spares you from immediate disaster, but you are focused on advancing your own interests rather than helping others. Lose 20 reputation with all factions.")
            state.players[player][1] -= 20
            state.players[player][2] -= 20
            state.players[player][4] -= 20
        if player == 4:
            print("Wildfires sweep large swathes of your region, destroying your infrastructure. Lose an active card.")
            state.players[state.current_player]['activeCards'].pop()

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
            state.players[min_stability_player][i] -= 30
    
    message = "Political instability in the " + state.factions[min_stability_player] + " have reached a boiling point.\n"
    message += "Conspirators within the faction have conspired to demonstrate power by orchestarting an assassination of the leader of the " + state.factions[max_stability_player] + ".\n"
    message += "As a consequence, political power in the " + state.factions[min_stability_player] + " has consolidated around the rebel conspirators, resulting in a more stable"
    message += " balance of power, at the cost of the factions reputation around the world.\nMeanwhile, political turmoil and infighting racks the formerly stable " + state.factions[max_stability_player] + ".\n"
    message += "The situation grows more perilous, and the doomsday clock advances 15 minutes closer to midnight."    

            


CARD_EFFECTS = {
    0: card_effect_treaty,
    1: card_effect_factory,
    2: card_effect_embassy,
    3: card_effect_trade,
    4: card_effect_embargo,
    5: card_effect_election,
    6: card_effect_humanitarian_aid,
    7: card_effect_cultural_exchange,
    8: card_effect_sabotage
}

ACTIVE_EFFECTS = {
    1: active_effect_factory,
    2: active_effect_embassy
}

# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self):
        self.game_turn = 1
        self.players = PLAYERS
        self.cards = CARDS
        self.clock = CLOCK
        self.factions = FACTIONS
        self.current_player = 1

        

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
            if self.current_player != s2.current_player:
                return False
            if self.game_turn != s2.game_turn:
                return False
            if self.clock != s2.clock:
                return False
            if self.cards != s2.cards:
                return False 
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "Current Player: " + self.factions[self.current_player] + "\n"
        # for p in self.players:
        #     txt += "Player " + str(p) + ":\n"
        curr = self.players[self.current_player]
        txt += "Money: " + str(curr['money']) + "\n"
        for other_player in self.players[self.current_player]:
            if other_player != 'money' and other_player != 'cards' and other_player != 'activeCards' and other_player != 'goalScore' and other_player != 'stability':
                    txt += "Player " + str(other_player) + " rep: " + str(self.players[self.current_player][other_player]) + "\n"
        txt += "Goal Score: " + str(curr['goalScore']) + "\n"
        txt += "Stability: " + str(curr['stability']) + "\n"
        txt += "Game Turn: " + str(self.game_turn) + "\n"
        txt += "Clock: " + str(self.clock['Hour']) + ":" + str(self.clock['Minute']) + "\n"
        txt += "Cards: " + str(curr['cards']) + "\n"
        txt += "Active Cards: " + str(curr['activeCards']) + "\n"

        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        new_state = State()
        new_state.players = {p: self.players[p].copy() for p in self.players}
        new_state.current_player = self.current_player
        new_state.cards = self.cards
        new_state.clock = self.clock
        new_state.game_turn = self.game_turn
        new_state.factions = self.factions

        return new_state

    def can_move(self, card):
        '''Tests if the player has enough money to use the given card.'''
        try:
            if card in self.players[self.current_player]['cards']:
               return True
            else:
               return False
        except (Exception) as e:
            print(e)

    def move(self, card):
        # Procedure for moving from one game state to next
        CARD_EFFECTS[card](self)
        self.players[self.current_player]['cards'].remove(card)
        news = self.copy()  # start with a deep copy.
        news.current_player = (news.current_player % 4) + 1
        news.players[news.current_player]['cards'].append(1)
        if news.current_player == 1:
            news.new_turn()
        return news  # return new state

    def is_goal(self):
        '''WIP: Checks if the current state is a goal state.'''
        return self.game_turn == 12 or self.players[self.current_player]['money'] >= 2000


    def goal_message(self):
        return "You have taken over the world!"
    
    def new_turn(self):
        self.game_turn += 1
        if self.game_turn == 4:
            event_ecologic_disaster(self)
        if self.game_turn == 7:
            event_political_assassination(self)
        if self.game_turn == 10:
            print("Doomsday has arrived!")
            doomsday = random.randint(1, 4)

        for player in self.players:
            for card in self.players[player]['activeCards']:
                ACTIVE_EFFECTS[card](self)

# </COMMON_CODE>

# <OPERATORS>
from soluzion import Basic_Operator as Operator

OPERATORS = [Operator("Play card " + CARDS[card_id]['name'] + " with effect " + CARDS[card_id]['effect'],
                      lambda s, card_id=card_id: s.can_move(card_id),
                      lambda s, card_id=card_id: s.move(card_id))
             for card_id in CARDS]

# </OPERATORS>

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