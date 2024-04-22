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

CLOCK = {'Hour': 11 , 'Minute': 30}

PLAYERS = {1: {'money': 100, 2: 100, 3: 100, 4: 100, 'cards': []},
           2: {'money': 100, 1: 100, 3: 100, 4: 100, 'cards': []},
           3: {'money': 100, 1: 100, 2: 100, 4: 100, 'cards': []},
           4: {'money': 100, 1: 100, 2: 100, 3: 100, 'cards': []}}

CARDS = {1: {'name': 'Treaty', 'cost': 10, 'effect': 'Add 10 to a chosen player and remove 10 from their lowest player'},}
        #  2: {'name': 'Card2', 'cost': 20, 'effect': 'Add 20 to player 2'},
        #  3: {'name': 'Card3', 'cost': 30, 'effect': 'Add 30 to player 3'},
        #  4: {'name': 'Card4', 'cost': 40, 'effect': 'Add 40 to player 4'}}  # Add more cards here

# </COMMON_DATA>

# <COMMON_CODE>
class State:
    def __init__(self):
        self.players = PLAYERS
        self.cards = CARDS
        self.clock = CLOCK
        self.current_player = 1
        self.last_action = None
        

    def __eq__(self, s2):
        for p in self.players:
            if self.players[p]['money'] != s2.players[p]['money']:
                return False
            for other_player in self.players[p]:
                if other_player != 'money' and other_player != 'cards' and self.players[p][other_player] != s2.players[p][other_player]:
                    return False
            for card in self.players[p]['cards']:
                if card not in s2.players[p]['cards']:
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
        new_state.last_action = self.last_action
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

    def move(self, From, To):
        '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the topmost disk
       from the From peg to the To peg.'''
        news = self.copy()  # start with a deep copy.
        pf = self.d[From]  # peg disk goes from.
        pt = self.d[To]
        df = pf[-1]  # the disk to move.
        news.d[From] = pf[:-1]  # remove it from its old peg.
        news.d[To] = pt[:] + [df]  # Put disk onto destination peg.
        return news  # return new state


    def is_goal(self):
        '''If the first two pegs are empty, then s is a goal state.'''
        return self.d['peg1'] == [] and self.d['peg2'] == []


    def goal_message(self):
        return "The Tower Transport is Triumphant!"

# </COMMON_CODE>

# <OPERATORS>
from soluzion import Basic_Operator as Operator

OPERATORS = [Operator("Move disk from " + p + " to " + q,
                      lambda s, p1=p, q1=q: s.can_move(p1, q1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p1=p, q1=q: s.move(p1, q1))
             for (p, q) in peg_combinations]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>