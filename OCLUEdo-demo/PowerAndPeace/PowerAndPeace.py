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

PLAYERS = {1: {'money': 100, 2: 100, 3: 100, 4: 100, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           2: {'money': 100, 1: 100, 3: 100, 4: 100, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           3: {'money': 100, 1: 100, 2: 100, 4: 100, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []},
           4: {'money': 100, 1: 100, 2: 100, 3: 100, 'cards': [], 'stability': 100, 'goalScore': 0, 'activeCards': []}}

CARDS = {0: {'name': 'Treaty', 'cost': 10, 'effect': 'Adds 10 rep to a chosen player and removes 10 rep from their lowest rep player. Costs $10'},
         1: {'name': 'Factory', 'cost': 30, 'effect': 'Generates $10 per turn and adds 1 to goal score. Costs $30'},
         2: {'name': 'Embassy', 'cost': 50, 'effect': 'Generates 10 rep lowest favored country per turn. Costs $50'},
         3: {'name': 'Trade', 'cost': 0, 'effect': 'Increases money by 10 times the number of active cards.'},
         4: {'name': 'Embargo', 'cost': 15, 'effect': 'Drastically reduces rep with a country and reduces their money. Costs $15'},
         5: {'name': 'Election', 'cost': 25, 'effect': 'Increases factional goal score. Costs $25'}}

for player in PLAYERS.values():
    player['cards'] = random.sample(list(CARDS.keys()), k=3)


def card_effect_treaty(state):
    chosen_player = int(input("Choose a player to make a treaty with: "))

    # Find the least favored player from the perspective of the chosen player
    least_favored_player = min(
        (player for player in state.players[chosen_player] if player not in [state.current_player, 'money', 'cards', 'stability', 'goalScore', 'activeCards']),
        key=lambda x: state.players[chosen_player][x])
    # Increase the reputation with the chosen player
    state.players[state.current_player][chosen_player] += 10
    state.players[chosen_player][state.current_player] += 10

    # Decrease the reputation with the least favored player
    state.players[state.current_player][least_favored_player] -= 10
    state.players[least_favored_player][state.current_player] -= 10

def card_effect_factory(state):
    state.players[state.current_player]['activeCards'].append(1)
    state.players[state.current_player]['money'] += 10
    state.players[state.current_player]['goalScore'] += 1
    state.players[state.current_player]['stability'] += 10    

def card_effect_embassy(state):
    # Generates 10 rep with lowest favored player per turn
    state.players[state.current_player]['activeCards'].append(2)
    state.players[state.current_player]['money'] -= 50
    least_favored_player = min(
        (player for player in state.players[state.current_player] if player not in [state.current_player, 'money', 'cards', 'stability', 'goalScore', 'activeCards']),
        key=lambda x: state.players[state.current_player][x])
    state.players[state.current_player][least_favored_player] += 10

def card_effect_trade(state):
    # Increases money by 10 times the number of active cards. Requires positive rep with a country.
    state.players[state.current_player]['money'] += 10 * len(state.players[state.current_player]['activeCards'])

def card_effect_embargo(state):
    # Drastically reduces rep with a country and reduces their money
    chosen_player = int(input("Choose a player to impose embargo: "))
    state.players[chosen_player]['money'] -= 20
    state.players[state.current_player][chosen_player] -= 20
    state.players[state.current_player]['stability'] -= 1

def card_effect_election(state):
    # Increases factional goal score
    state.players[state.current_player]['goalScore'] += 2
    state.players[state.current_player]['stability'] -= 1
    state.players[state.current_player]['money'] -= 25

CARD_EFFECTS = {
    0: card_effect_treaty,
    1: card_effect_factory,
    2: card_effect_embassy,
    3: card_effect_trade,
    4: card_effect_embargo,
    5: card_effect_election
}



# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self):
        self.game_turn = 1
        self.players = PLAYERS
        self.cards = CARDS
        self.clock = CLOCK
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
        txt = "Current Player: " + str(self.current_player) + "\n"
        for p in self.players:
            txt += "Player " + str(p) + ":\n"
            txt += "Money: " + str(self.players[p]['money']) + "\n"
            for other_player in self.players[p]:
                if other_player != 'money':
                    txt += "Player " + str(other_player) + ": " + str(self.players[p][other_player]) + "\n"
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
        '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the topmost disk
       from the From peg to the To peg.'''
        news = self.copy()  # start with a deep copy.
        news.players[self.current_player]['cards'].remove(card)
        CARD_EFFECTS[card](news)
        news.current_player = (news.current_player % 4) + 1
        news.players[news.current_player]['cards'].append(1)
        if news.current_player == 1:
            news.new_turn()
        return news  # return new state

    def is_goal(self):
        '''WIP: Checks if the current state is a goal state.'''
        return self.game_turn == 12 or self.players[self.current_player]['money'] >= 200


    def goal_message(self):
        return "You have taken over the world!"
    
    def new_turn(self):
        self.game_turn += 1
        for player in self.players:
            for card in self.players[player]['activeCards']:
                CARD_EFFECTS[card](self)

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
    {'name': 'Player 1', 'min': 1, 'max': 1},
    {'name': 'Player 2', 'min': 1, 'max': 1},
    {'name': 'Player 3', 'min': 1, 'max': 1},
    {'name': 'Player 4', 'min': 1, 'max': 1},
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