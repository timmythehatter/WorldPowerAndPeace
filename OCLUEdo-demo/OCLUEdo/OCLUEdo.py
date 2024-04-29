'''OCLUEdo.py  (formerly HalfClue.py)
("The Cards Half of the game of 'Clue'")
A SOLUZION problem formulation, for ZZ003.py.

First created in the Spring of 2020, during
the Covid-19 pandemic, this program provided
a means to handle the secret information aspects
of playing a game of CLUE online.
This included initial dealing of cards, with a
random "murder set" of (room, person, weapon),
and a random deal of the remaining cards to 
all the players.  This program was intended to
be used at the same time that a Zoom session
would happen, with one person using a real Clue
board and a webcam to share the board in Zoom,
and that person also rolling the dice for all
the other online players, moving tokens as
they requested.

The new game of OCLUEdo is a full game, but
with a much simpler board, and without dice.
Players still get to move to different places,
but other than the starting squares and the
rooms, there are only 9 other locations.
Instead of being squares on the board, they
are "lobbies" with one just outside of each
Clue room.  To go into a Clue room, you have
to first move to its lobby (unless you come
via secret passages, as in standard Clue).

Incorporating "accusations" as of April 8.
a. Add an "accusation_phase" variable to states.
b. Add a "current_accusation" variable to states.
c. Add operators analogous to the suggestion operators,
 but for accusations.
d. Update the vis to show 
    i. accusation in progress (but not what it is).
    ii. results of the accusation, followed by
          acknowledge end of turn, if wrong;
          or END OF GAME, if correct.
    iii. if any passive players, a list of them.
'''
#<METADATA>
SOLUZION_VERSION = "3.0"
PROBLEM_NAME = "OCLUEdo, a Variation of The Game of Clue"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "08-APR-2024"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The game of <b>"OCLUEdo"</b> is a variation of the board game
known as Clue in the USA and Cluedo in the UK with cards and dice,
Clue dates back to World War II, first under the name of Cluedo.
OCLUEdo has the same rooms, characters, and weapons as Clue
(classic version rather than more recent Hasbro variations).
However, instead of players moving around the large Clue board
using dice, OCLUEdo uses a more restricted board and no dice.
<br>
  The cards portion of the game includes the following: setting up
a random selection of murderer, weapon and room before the game
begins, which the players will have to figure out; dealing the
remaining cards randomly to the players at the beginning of the
game, and then managing the business of "suggestions" about the
murder, and the showing of cards by one person secretly to another.

'''
#</METADATA>

#<COMMON_DATA>
MURDERER = None
CRIME_ROOM = None
CRIME_WEAPON = None
MISS_SCARLET = 0
MR_GREEN = 1
COLONEL_MUSTARD = 2
PROFESSOR_PLUM = 3
MRS_PEACOCK = 4
MRS_WHITE = 5
ROLE_BEING_PLAYED = 6*[False]
PLAYER_HAND = 6*[[]]
NAMES = ['Miss Scarlet','Mr. Green','Colonel Mustard','Prof. Plum','Mrs. Peacock','Mrs. White']
WEAPONS = ['Candlestick','Knife','Lead Pipe','Revolver','Rope','Wrench']
ROOMS = ['Lounge','Dining Room','Kitchen','Ballroom','Conservatory','Billiard Room','Library','Study','Hall']
LOBBIES = [r + "'s Lobby" for r in ROOMS]
PLAYER_STARTS = [p + "'s Start" for p in NAMES]
POSSIBLE_PLAYER_SPOTS = PLAYER_STARTS + LOBBIES + ROOMS
#</COMMON_DATA>

#<COMMON_CODE>
DEBUG=False

#if DEBUG: 
#  ROLE_BEING_PLAYED[0]=True
#  ROLE_BEING_PLAYED[2]=True
#  ROLE_BEING_PLAYED[4]=True

def int_to_name(i):
    return NAMES[i]

def int_to_player_spot(i):
    return POSSIBLE_PLAYER_SPOTS[i]

def spot_is_lobby(i):
    if i > 5 and i < 15: return True
    else: return False

def spot_is_room(i):
    if i > 14: return True
    else: return False
    
class State():
  def __init__(self, old=None):
    if old == None:
      self.whose_turn = next_player(-1)
      self.whose_subturn = -1
      self.suggestion = None
      # A suggestion looks like [7,2,2] (room no. suspect no., weapon no.)
      self.suggestion_phase = 0 # No suggestion started. Then 4 phases: 1 is starting suggestion,
      # 2 is room has been suggested, 3 suspect identified, 4 weapon suggested, 
      # and responses in progress.  
      # Responses can end in two ways:
      #  On a subturn, a player makes a "refutation", showing a card that disproves the suggestion.
      #    In this case, that card is recorded in the refutation portion of the state,
      #      and the suggestion phase changes from 4 to 5.
      #      Phase 5 affords the suggester a moment to "see" the refutation card,
      #        before ending his/her turn.
      #  Going all around, no player can refute the suggestion.  In this case, the
      #    suggestion phase also goes to 5, but no refutation card is seen.
      #    Instead, the display shows "Nobody could refute the suggestion."
      # When the player whose turn it is clicks to acknowledge the information, responses are done.
      # When responses end, phase goes back to 0.
      self.refutation_card = None
      self.accusation = None # any accusation in progress.
      self.accusation_phase = 0
      self.accusations = [] # List of accusations so far, and who made them 
      # Someone who made a false accusation is now inactive, 
      # but still playing to respond to suggestions.
      # An accusation looks like [7,2,2,3], a suggestion with a 4th int: the role of the accuser.
      self.player_places = [0, 1, 2, 3, 4, 5]
      self.winner = None
    else:
      self.whose_turn = old.whose_turn
      self.whose_subturn = old.whose_subturn
      self.suggestion = old.suggestion
      self.accusations = old.accusations[:]
      self.suggestion_phase = old.suggestion_phase
      self.refutation_card = old.refutation_card
      self.player_places = old.player_places[:]
      self.accusation = old.accusation
      self.accusation_phase = old.accusation_phase
      self.winner = old.winner

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    # A state maps usernames to play integers.
    news = State(None)
    news.whose_turn = self.whose_turn
    news.whose_subturn = self.whose_subturn
    news.suggestion = self.suggestion
    news.suggestion_phase = self.suggestion_phase
    news.refutation_card = self.refutation_card
    news.accusations = self.accusations
    news.accusation = self.accusation
    news.accusation_phase = self.accusation_phase
    news.winner = self.winner
    return news

  def __str__(self):
    ''' Produces a textual description of a state.
        Might not be needed in normal operation with GUIs.'''
    txt = ''
    txt += NAMES[self.whose_turn]+"'s turn.\n"
    if self.suggestion != '':
       txt += "Suggestion is "+format_suggestion(self.suggestion)+".\n"
    if self.whose_subturn >= 0 and self.suggestion_phase==4:
       txt += "Waiting for "+int_to_name(self.whose_subturn)+" to disprove this or pass.\n"
    elif self.suggestion_phase in [2,3]: txt += "Suggestion in progress.\n"
    elif self.suggestion_phase==5:
      if self.refutation_card != None:
        txt += "refutation card shown by "+NAMES[self.whose_subturn]+\
               " is "+str(self.refutation_card)+".\n"
    txt += format_accusations(self.accusations)
    return txt

  def __eq__(self, s):
    return self.__hash__() == s.__hash__()

  def __hash__(self):
    return (self.__str__()).__hash__()

  def is_goal(self):
    return not self.winner == None

def format_suggestion(sug):
    if sug==[] or sug==None: return "(no suggestion)"
    #print("suggestion to be formatted is: "+str(sug))
    (room_no, suspect_no, weapon_no) = sug
    room = ROOMS[room_no]
    if suspect_no==-1: suspect="unnamed"
    else: suspect=NAMES[suspect_no]
    if weapon_no==-1: weapon="unsuggested"
    else: weapon = WEAPONS[weapon_no]
    s = "%s in the %s with the %s" % (suspect, room, weapon)
    return s

def format_accusations(acc):
    if acc==[]:
       return "No accusations have yet been made.\n"
    else:
       txt = ''
       for a in acc:
         txt += format_suggestion(a[:-1])+(" accused by %s\n" % NAMES[a[-1]])
    return txt

SESSION = None
INACTIVE_PLAYERS = [] # A player becomes inactive after making a false accusation.

def next_player(k, inactive_ok=False):
  if SESSION==None: return 0 # Roles not ready
  search_count = 0
  while True:
    k = (k + 1) % 6
    #if ROLE_BEING_PLAYED[k]:
    if len((SESSION['ROLES_MEMBERSHIP'])[k])>0:
      if k in INACTIVE_PLAYERS:
        if inactive_ok: return k
      else: return k
    search_count += 1
    if search_count > 6:
      print("Nobody is playing today.\n")
      raise Exception("No players available in function: next_player.")


def is_players_turn(state, role):
  '''Return True if it's this player's turn, and
  the player has never made a false accusation.'''
  if not role==state.whose_turn: return False
  for acc in state.accusations:
     if role==acc[-1]: return False
  return True

def is_players_subturn(state, role): 
  '''Is response rotation at this role (player)?
  Check elsewhere for suggestion_phase equal to 4.'''
  if not role==state.whose_subturn: return False
  return True # Here it's OK if player earlier made a false accusation.

def can_start_suggestion(state, role):
  return False # THIS OPERATOR IS DEPROCATED.
  '''Return True if player is allowed to initiate or continue a suggestion.
  It must be the player's turn.  The player must be active (not a player
  who made a false accusation and remains in the game to respond to suggestions).
  The current suggestion phase must be 0.
  '''
  if not is_players_turn(state, role): return False
  if state.suggestion_phase > 0: return False
  return True

def start_suggestion(state, role):
  news = State(state)
  news.suggestion_phase = 1
  return news

def can_suggest_room(state, role, room):
  '''Return True if player is allowed to initiate or continue a suggestion.
  It must be the player's turn.  The player must be active (not a player
  who made a false accusation and remains in the game to respond to suggestions).
  
  '''
  if not is_players_turn(state, role): return False
  if state.suggestion_phase != 1: return False
  return True

def suggest_room(state, role, room):
  news = State(state)
  news.suggestion = [room, -1, -1]
  news.suggestion_phase = 2
  return news

def can_suggest_suspect(state, role, suspect):
  '''Is it still this role's turn? Was a room just suggested?'''
  if not is_players_turn(state, role): return False
  if state.suggestion_phase != 2: return False
  return True

def suggest_suspect(state, role, suspect):
  news = State(state)
  news.suggestion[1]=suspect
  news.suggestion_phase = 3
  # The suspect get's summoned to the room.
  room = news.suggestion[0]
  news.player_places[suspect]=room + 15 # real rooms are the last 9 possible places.
  return news

def can_suggest_weapon(state, role, weapon):
  '''Is it still this role's turn? Was a suspect just suggested?'''
  if not is_players_turn(state, role): return False
  if state.suggestion_phase != 3: return False
  return True

def suggest_weapon(state, role, weapon):
  news = State(state)
  news.suggestion[2]=weapon
  news.suggestion_phase = 4
  # Suggestion is now ready for possible refutation.
  # Identify the first player allowed to respond.
  news.whose_subturn = next_player(news.whose_turn, inactive_ok=True)
  return news

def can_respond(state, role, card_no):
  '''Is it now this role's subturn"'''
  if state.suggestion_phase != 4: return False
  if not is_players_subturn(state, role): return False
  #print(" Considering whether "+NAMES[state.whose_subturn]+" can respond with his/her card number "+str(card_no))
  # Next, does this player have at least k cards?
  hand = PLAYER_HAND[role]
  if card_no >= len(hand): return False
  # Next, find this player's kth card. k = card_no.
  card = hand[card_no]
  # Card must be one of those in the suggestion.
  if card[0]=='r' and card[1]==state.suggestion[0]: return True
  if card[0]=='p' and card[1]==state.suggestion[1]: return True
  if card[0]=='w' and card[1]==state.suggestion[2]: return True
  return False

def respond_sorry(state, role):
  return respond(state, role, -1)

def respond(state, role, card_number_or_pass):
  '''This operator handles a player's response to a suggestion.'''
  news = State(state)
  if card_number_or_pass==-1:
    print(NAMES[news.whose_subturn]+" cannot disprove the suggestion.")
    next_responder = next_player(news.whose_subturn, inactive_ok=True)
    print("Next responder is "+NAMES[next_responder])
    if next_responder==state.whose_turn: # Has the chance to respond gone all around?
      print("No responders have been able to disprove the suggestion!")
      #news.whose_turn = next_player(news.whose_turn)
      news.suggestion_phase = 5
      news.suggestion = None
    else:
      print("Continuing the response round.")
      news.whose_subturn = next_responder
  else:
    print("The suggestion by "+NAMES[state.whose_turn]+" has been disproved by "+NAMES[state.whose_subturn])
    hand = PLAYER_HAND[state.whose_subturn]
    evidence_card = hand[card_number_or_pass]
    news.refutation_card = evidence_card
    news.suggestion_phase = 5
    #if DEBUG: 
    print("You're not supposed to know this, but we are debugging. The card was number "+str(card_number_or_pass)+" within the responders hand.")
  return news

def can_acknowledge(s, role):
  # True if responding is done and 'role' is ready to finish his/her turn.
  if not is_players_turn(s, role): return False
  if s.suggestion_phase < 5: return False
  else: return True

def acknowledge(s, role):
  # Player whose turn it is acknowledges having either seen the evidence
  # card, or witnessed the fact that nobody could refute the suggestion.
  news = State(s)
  news.whose_turn = next_player(news.whose_turn)
  news.suggestion = None
  news.refutation_card = None
  news.suggestion_phase = 0
  news.whose_subturn = -1
  return news

def cannot_disprove(s, role):
  # This is the precondition for a player to pass during a refutation round.
  # First, suggestion_phase must be 4.
  if s.suggestion_phase != 4: return False
  # Next, it must be this person's subturn.
  if not s.whose_subturn == role: return False
  # Finally, role must have NONE of the suggestion's cards.
  hand = PLAYER_HAND[s.whose_subturn]
  print("In cannot_disprove, with hand ", hand, "and suggestion ",s.suggestion)
  result = True
  room_card = ('r', s.suggestion[0])
  if room_card in hand: result = False
  suspect_card = ('p', s.suggestion[1])
  if suspect_card in hand: result = False
  weapon_card = ('w', s.suggestion[2])
  if weapon_card in hand: result = False
  print(" result = ", result)
  return result

def can_go(s, role, place):
  # It must be role's turn.
  if not s.whose_turn == role: return False
  # No suggestion round must be in progress
  if s.suggestion_phase > 0: return False
  # No accusation must be in progress
  if s.accusation_phase > 0: return False

  # If player is IN the lobby for the desired
  # room, then OK.
  current_place = s.player_places[role]
  # The place to go should NOT be the current place
  if current_place == place: return False
  
  # If the place to go is a lobby, it must not be occupied.
  if spot_is_lobby(place):
      # Any other players in there?
      if place in s.player_places: return False
      else: return True
  #print("Player "+str(role)+" is at "+ POSSIBLE_PLAYER_SPOTS[current_place])
  if spot_is_room(place) and\
    current_place == place - 9:
      return True
  # Consider secret passages.
  if current_place==22 and place==17: return True # Study to Kitchen
  if current_place==17 and place==22: return True # Kitchen to Study
  if current_place==15 and place==19: return True # Lounge to Conservatory
  if current_place==19 and place==15: return True # Conservatory to Lounge
  # Otherwise, going to this place is not allowed here.
  return False

def go(s, role, place_to_go):
  # The player in "role" goes to the location in "place_to_go".
  news = State(s)
  who = s.whose_turn
  news.player_places[who] = place_to_go
  # If the place is a normal room, then this player should make
  # a suggestion, and the suggestion should involve this place.
  if spot_is_room(place_to_go):
    news.suggestion_phase = 2; # Room is known.
    news.suggestion = [place_to_go-15, -1, -1]
  else:
    news.whose_turn = next_player(news.whose_turn)
  return news

def can_start_accusation(s, role):
  if not s.whose_turn == role: return False
  # No suggestion round must be in progress
  if s.suggestion_phase > 0: return False
  # No accusation must be in progress
  if s.accusation_phase > 0: return False
  return True # OK

def start_accusation(s, role):
  print(NAMES[s.whose_turn]+" is making an accusation!")
  news = State(s)
  news.accusation_phase = 1
  news.accusation = [-1, -1, -1, s.whose_turn]
  return news

def can_add_room_to_accusation(s, role, room):
  if not s.whose_turn == role: return False
  if s.accusation_phase == 1: return True
  return False
    
def add_room_to_accusation(s, role, room):
  news = State(s)
  news.accusation_phase = 2
  news.accusation[0]=room
  return news
  
def can_add_player_to_accusation(s, role, player):
  if not s.whose_turn == role: return False
  if s.accusation_phase == 2: return True
  return False

def add_player_to_accusation(s, role, player):
  news = State(s)
  news.accusation_phase = 3
  news.accusation[1]=player
  return news

def can_add_weapon_to_accusation(s, role, weapon):
  if not s.whose_turn == role: return False
  if s.accusation_phase == 3: return True
  return False

def add_weapon_to_accusation(s, role, weapon):
  news = State(s)
  news.accusation_phase = 4
  news.accusation[2]=weapon
  news.accusations.append(s.accusation)
  return news

def can_ask_win(s, role):
  if not s.whose_turn == role: return False
  if s.accusation_phase == 4: return True
  return False

def ask_win(s, role):
  # Accuser will learn whether they win or lose.
  news = State(s)
  win = True
  if DEBUG:
     print("CRIME_ROOM is "+str(CRIME_ROOM))
     print(" Accusation room is "+str(s.accusation[0]))
     print("MURDERER is "+str(MURDERER))
     print(" Accusation murderer is "+str(s.accusation[1]))
     print("CRIME_WEAPON is "+str(CRIME_WEAPON))
     print(" Accusation weapon is "+str(s.accusation[2]))
  if not s.accusation[0] == CRIME_ROOM: win = False
  if not s.accusation[1] == MURDERER: win = False
  if not s.accusation[2] == CRIME_WEAPON: win = False
  if win:
      print(NAMES[s.whose_turn]+" wins!")
      news.winner = s.whose_turn
      news.whose_turn = -1 # No more turns!
  else:
      print(NAMES[s.whose_turn]+" loses and is now and inactive player")
      INACTIVE_PLAYERS.append(s.whose_turn)
      news.accusation_phase = 0
      news.accusation = None
      news.whose_turn = next_player(news.whose_turn)
  return news

# New function, as of May 5, 2020, to facility role-specific visualizations...
def is_user_in_role(role_no):
  username = SESSION['USERNAME']
  rm = SESSION['ROLES_MEMBERSHIP']
  if rm==None: return False
  users_in_role = rm[role_no]
  return username in users_in_role

def get_session():
  return SESSION

def goal_message(s):
  return "Game Over."
#</COMMON_CODE>

#<OPERATORS>  #---------------------
class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s, role_number=0):
    return self.precond(s, role=role_number)

  def apply(self, s):
    return self.state_transf(s)

op_respond_sorry = Operator(\
  'Respond "Sorry but I cannot disprove your suggestion."',
  lambda s, role=0: cannot_disprove(s, role),
  lambda s, role=0: respond_sorry(s, role))

op_start_suggestion = Operator(\
  "Offer a suggestion.",
  lambda s, role=0: can_start_suggestion(s, role),
  lambda s, role=0: start_suggestion(s, role))

room_ops = [Operator(\
  "Suggest it happened in the "+ROOMS[room],\
  lambda s, role=0, room=room: can_suggest_room(s, role, room),\
  lambda s, role=0, room=room: suggest_room(s, role, room))\
  for room in range(len(ROOMS))]

suspect_ops = [Operator(\
  "Suggest suspect "+NAMES[suspect],\
  lambda s, role=0, suspect=suspect: can_suggest_suspect(s, role, suspect),\
  lambda s, role=0, suspect=suspect: suggest_suspect(s, role, suspect))\
  for suspect in range(len(NAMES))]

weapon_ops = [Operator(\
  "Suggest the weapon was the "+WEAPONS[weapon],\
  lambda s, role=0, weapon=weapon: can_suggest_weapon(s, role, weapon),\
  lambda s, role=0, weapon=weapon: suggest_weapon(s, role, weapon))\
  for weapon in range(len(WEAPONS))]

response_ops = [Operator(\
  "Show your card number "+str(i+1),\
  lambda s, role=0, card_no=i: can_respond(s, role, card_no),\
  lambda s, role=0, card_no=i: respond(s, role, card_no))
  for i in range(9)]

go_ops = [Operator(\
  "Go to "+POSSIBLE_PLAYER_SPOTS[i],
  lambda s, role=0, place_no=i: can_go(s, role, place_no),\
  lambda s, role=0, place_no=i: go(s, role, place_no))\
  for i in range(6, 24)]

op_acknowledge = Operator(\
  'Acknowledge end of turn.',
  lambda s, role=0: can_acknowledge(s, role),
  lambda s, role=0: acknowledge(s, role))

op_start_accusation = Operator(\
  "Make an accusation.",
  lambda s, role=0: can_start_accusation(s, role),
  lambda s, role=0: start_accusation(s, role))

op_add_room_to_accusation = [Operator(\
  "Add room "+ROOMS[room]+" to your accusation",
  lambda s, role=0, room=room: can_add_room_to_accusation(s, role, room),
  lambda s, role=0, room=room: add_room_to_accusation(s, role, room))\
  for room in range(len(ROOMS))]
                                      
op_add_player_to_accusation = [Operator(\
  "Accuse "+NAMES[player]+" of being the murderer",
  lambda s, role=0, player=player: can_add_player_to_accusation(s, role, player),
  lambda s, role=0, player=player: add_player_to_accusation(s, role, player))\
  for player in range(len(NAMES))]
                                      
op_add_weapon_to_accusation = [Operator(\
  "Add weapon "+WEAPONS[weapon]+" to your accusation",
  lambda s, role=0, weapon=weapon: can_add_weapon_to_accusation(s, role, weapon),
  lambda s, role=0, weapon=weapon: add_weapon_to_accusation(s, role, weapon))\
  for weapon in range(len(WEAPONS))]

op_ask_win = Operator(\
  "Did I win?",
  lambda s, role=0: can_ask_win(s, role),
  lambda s, role=0: ask_win(s, role))
                      
OPERATORS = go_ops +\
 [op_start_suggestion]+\
 room_ops + suspect_ops + weapon_ops +\
 response_ops + [op_respond_sorry, op_acknowledge] +\
 [op_start_accusation] + op_add_room_to_accusation +\
 op_add_player_to_accusation + op_add_weapon_to_accusation +\
 [op_ask_win]

if DEBUG:
  print("All operators:")
  for o in OPERATORS:
    print(o.name)
#</OPERATORS>

#<INITIAL_STATE>
INITIAL_STATE = None
import random
def deal():
  global MURDERER, CRIME_WEAPON, CRIME_ROOM
  "In an hand or a deck, a card is a tuple. E.g., ('p',0) is Miss Scarlet - person 0."
  MURDERER = random.choice(range(6))
  non_murderers = [('p',i) for i in range(6)]
  non_murderers.pop(MURDERER)
  CRIME_WEAPON = random.choice(range(6))
  weapons_left = [('w',i) for i in range(6)]
  weapons_left.pop(CRIME_WEAPON)
  CRIME_ROOM = random.choice(range(9))
  rooms_left = [('r',i) for i in range(9)]
  rooms_left.pop(CRIME_ROOM)

  cards_left = non_murderers + weapons_left + rooms_left
  cards_shuffled = shuffle(cards_left)

  player = next_player(-1)
  while cards_shuffled != []:
    a_card = cards_shuffled.pop()
    new_hand = PLAYER_HAND[player][:]
    new_hand.append(a_card)
    PLAYER_HAND[player] = new_hand
    if DEBUG: print("Dealing card "+str(a_card)+" to "+NAMES[player])
    player = next_player(player)

  if DEBUG:
    print(" The MURDERER is "+NAMES[MURDERER]+".\n")
    print(" The CRIME_WEAPON is "+WEAPONS[CRIME_WEAPON]+".\n")
    print(" The CRIME_ROOM is "+ROOMS[CRIME_ROOM]+".\n")

    print(" Here are the hands dealt out:\n")
    for i in range(6):
      if PLAYER_HAND[i]==[]: continue
      print("For "+NAMES[i]+": ", str(PLAYER_HAND[i]))

def shuffle(L):
  "Return a copy of L with elements randomly reordered."
  LC = L[:]
  n = len(LC)
  shuffled = []
  for i in range(n-1,-1,-1):
    k = random.randint(0,i)
    shuffled.append(LC[k])
    LC.pop(k)
  return shuffled

def create_initial_state():
  global INITIAL_STATE
  deal()
  INITIAL_STATE = State()
  print(INITIAL_STATE)
#</INITIAL_STATE>

#<ROLES>
ROLES = [ {'name': 'Miss Scarlet', 'min': 1, 'max': 1},
          {'name': 'Mr. Green', 'min': 1, 'max': 1},
          {'name': 'Colonel Mustard', 'min': 1, 'max': 1},
          {'name': 'Prof. Plum', 'min': 1, 'max': 1},
          {'name': 'Mrs. Peacock', 'min': 1, 'max': 1},
          {'name': 'Mrs. White', 'min': 1, 'max': 1},
          {'name': 'Observer', 'min': 0, 'max': 25}]
#</ROLES>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
BRIFL_SVG = True # The program FoxAndGeese_SVG_VIS_FOR_BRIFL.py is available
render_state = None
def use_BRIFL_SVG():
  global render_state
  from  OCLUEdo_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>


