'''TestTransitions.py
This formulation will serve as a unit-test for
any client or autosolver that supports "transitions"
in problem/game formulations.

A transition is a user-interface action, initiated
and performed by the client software, when a state transition 
occurs during a game or problem-solving session.

A textual client might simply render a transition by
displaying some text that depends on what the two
relevant states (current state, next state) are.
The operator that was applied to cause the state
change can also affect the transition.

Status: Started on April 25, 2024. 
 Ready to test with a client that supports transitions.


'''

from soluzion import Basic_State, Basic_Operator

#<METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "Test Formulation for Clients that handle 'Transitions' "
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "20-JANUARY-2024"

PROBLEM_DESC=\
'''
The "Count" game is a trivial game with two operators:
Add-1 and Add-2.  
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>

class State(Basic_State):

  def __init__(self, n=0):
    self.n = n

  def is_goal(self):
    '''If n is 5 we are at the goal.'''
    return (self.n > 9)

  def goal_message(self):
    return "Congratulations on exceeding 9!"

  def __eq__(self,s2):
    if s2==None: return False
    if self.n != s2.n: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    return str(self.n)

  def __hash__(self):
    return (self.__str__()).__hash__()

class Operator(Basic_Operator):
  pass
#</COMMON_CODE>

#<OPERATORS>
# Operator to add 1
phi0 = Operator("Add 1",
                lambda s: True,
                lambda s: State(n = s.n + 1))

# Operator to add 2
phi1 = Operator("Add 2",
                lambda s: True,
                lambda s: State(n = s.n + 2))

OPERATORS = [phi0, phi1]

#</OPERATORS>

#<TRANSITIONS>
def getting_even(s1, s2, op=None):
  " Return True if s1 is odd and s2 is even. "
  return s1.n % 2 == 1 and s2.n % 2 == 0

def getting_odd(s1, s2, op=None):
  " Return True if s1 is odd and s2 is even. "
  return s1.n % 2 == 0 and s2.n % 2 == 1

def say_prime(s1, s2, op):
  return "At "+str(s2.n)+", your moving into a prime state!"

# The client will import the following list or rules.
# Each time a transition (s1, s2, op)  occurs during a session,
# the client will start with the first rule on the list and see if
# its condition matches the transition.  As soon as it
# finds a matching condition it will apply the action of
# that rule, and respect any of the rule's options that it is
# able to, that are not overridden by any session-time user
# preference settings, such as timing or font color and size..
# Each rule's condition is specified as a function, for example,
# getting_even, which takes up to three arguments: the
# current state, next state, and optionally, the operator used
# in the transition.
# Action portion of each rule is either a text string to
# be rendered, OR a function to be applied to render the
# transition.  If the function returns a string, then the
# client will render that string in the same way it would
# render a string not produced by a function.
# Note that the transitions and their conditions and/or
# action functions can be implemented in one or more separate
# files, if desired, and imported here.  The action functions
# could cause animations, transitory audio effects, or even
# the starting of background music or audio that continues
# until stopped later in the game by a transition that stops
# or changes the background audio.  Transitions may involve
# modal dialogs, so that users can take as much time as they
# need to read transition text or inspect transition images
# or charts that appear.  If the same transition can occur
# multiple times during a session, it is up to the options,
# and a client that can interpret them, to decide whether
# abbreviated versions of transition text should be shown
# after the first occurrence of the transition.
TRANSITIONS = [
  (getting_even, "Your number n is getting even.", {}),
  (getting_odd, "Your number n is getting odd.", {}),
  (lambda s1, s2, op: s2.n>9 and op==phi1, "You made it by adding 2!", {}),
  (lambda s1, s2, op: s2.n>9, "Made it!", {}),
  (lambda s1, s2, op: s2.n in [2, 3, 5, 7], say_prime, {}),
  (lambda s1, s2, op: True, "Parity is not changing here.")
  ]
#</TRANSITIONS>
