'''TestFormulationParamOpInt.py
This formulation will serve as a unit-test for
any client or autosolver that supports parameterized
operators of type int (integer). This formulation
provides a range restriction, prompting instructions,
and a suggested sampling policy for autosolvers.
Any given client can ignore those or use them.
Ideally a client will automatically
check for any restrictions of integers to a particular
range, and for any prompting instructions and use those
in an interactive session, if appropriate, and if it is
an autosolver, will use the suggested sampling policy.

Status: Working as of January 21, 2024.
 How a parameterized operator gets set up and executed is
as follows:
 1. This formulation file defines the Operator instance,
and the 4th argument to the Operator constructor is the
parameter list argument.  If an operator construction call
does NOT have a 4th argument, it defaults to [], which
counts as False when it is an argument to "if" within 
code that checks.  When the paramter list argument is an
actual non-empty list, the parameter fetching code in
soluzion.py and a client will go through that list and
obtain an argument for each parameter.  If that parameter
list is actually a function, then the function will be
applied to the current state to return a parameter list
that depends on the current state.  Then that list will
be used to fetch arguments as in the direct case.

Note that the execution chain starts in soluzion.py when
the operator's apply method is invoked there.  The
parameter fetching seems to start there, but the method
that really handles the getting of inputs from a user or
an agent is defined in a different file (such as
Int_Solv_Client4.py) but overwritten into the stub in
soluzion.py.  This gives access to the client's functionality
and the current state without having to have circular 
imports (which among other problems would make it difficult
to use DIFFERENT clients on the same problem formulation).

'''

from soluzion import Basic_State, Basic_Operator, \
  Invalid_State_Exception

#<METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "Test Formulation for Integer Parameters to Operators"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "20-JANUARY-2024"

PROBLEM_DESC=\
'''
"Get To Five" is a very easy game, in which we start out with
the number 0. In each turn, we can change the number by
applying an operator. The number must always be in the
range from -5 to 5.  If it gets to 5, you win the game.

The point of the game is not to pose any challenge; it's so
easy to win.  Rather, it is to illustrate several different
kinds of moves, and how the software handles them.
This problem formulation includes five operators, two of
which are "parameterized operators".
Each of them needs an integer parameter in order to proceed.
The state space is {-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5}.
There are five operators:
phi0: negate s.n. (always applicable and is a no-op when s.n=0)
phi1: subtract 1. (applicable when s.n >=  -4).
phi2: subtract k. (k is a parameter limited to {2, 3}, and only applicable when s.n >=  -2).
phi3: add k. (k is a parameter limited to {k0, ..., k1}, where these limits
are computed from s.n in such a way that -5 <= s.n+k <= 5.)
phi4: add k. (k is an integer with no restrictions; however,
 a client should catch an exception that this formulation will throw
 if the parameter would cause an illegal state.) 

A client should not crash when running this problem formulation,
regardless of what a user enters for a parameter value.
'''
#</METADATA>

#<COMMON_DATA>
MIN_STATE_N = -5
MAX_STATE_N = 5
#</COMMON_DATA>

#<COMMON_CODE>

class State(Basic_State):

  def __init__(self, n=0, validate=False):
    self.n = n
    if validate:
      if (type(n) != type(1)) or (n < MIN_STATE_N) or (n > MAX_STATE_N):
        raise Invalid_State_Exception("n is too small or too large.")

  def is_goal(self):
    '''If n is 5 we are at the goal.'''
    return (self.n == MAX_STATE_N)

  def goal_message(self):
    return "Congratulations on reaching the maximum state value!"

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
# Now we define 5 operators to illustrate the different ways
# to use or not use parameters, although in this formulation,
# we are only interested in parameters that are integers.

# First a simple operator, always applicable, assuming that
# MIN_STATE_INT = - MAX_STATE_INT,  with no parameters:
phi0 = Operator("Negate n",
                lambda s: True,
                lambda s: State(n= - s.n))

# The next operator does have a precondition that's not always true.
# The number used in subtraction here is "hard-coded" to the constant 1,
# and so we don't call this a parameterized operator, since there
# is no parameter to use for specifying this or any other value.
phi1 = Operator("Subtract 1",
                lambda s: s.n >= MIN_STATE_N + 1,
                lambda s: State(n= s.n - 1))

# Next is a parameterized operator that needs an integer in
# a narrow range of values, which are provided as constants.
# Although the operator's precondition depends on the current state's n
# value, the range for the parameter is hard-coded and does not depend
# on the state.
phi2 = Operator("Subtract k",
                lambda s: s.n >= MIN_STATE_N + 3,
                lambda s,args: State(n = s.n - args[0]),
                [{'name': 'k', 'type':'int', 'min':2, 'max':3, 'sampling':'all'}])

# The following operator is parameterized and the range of legal
# values is NOT constant, but depends upon the state s.  The client
# makes the assumption that this is always the CURRENT_STATE at the
# time arguments are being fetched for this operator.
phi3 = Operator("Add k; k is limited to a given range, depending on the current state.",
                lambda s: True,
                lambda s,args: State(n = s.n + args[0]),
# k is a parameter limited to {k0, ..., k1}, where these limits
#  are computed from s.n in such a way that -5 <= s.n+k <= 5.
# Here we define a LAMBDA FUNCTION that will return the parameter
# list where some details DEPEND ON THE CURRENT STATE:
                lambda s:
                [{'name': 'k', 'type':'int', 'min':MIN_STATE_N - s.n,\
                  'max':MAX_STATE_N - s.n, 'sampling':'all'}])

# Our last operator illustrates a different way of handling a parameter:
# the parameter list doesn't set value restrictions such as a minimum
# or maximum.  However, the state-transformation function (the 2nd lambda
# expression, has the option validate=True, which tells the State
# constructor to check the value of n and throw an exception if it
# is too low or too high.  The State class has to support this, as
# it does in this file.  The exception will be caught in the client code.
phi4 = Operator("Add k; k is unrestricted, though not always legal.",
                lambda s: True,
                lambda s,args: State(n = s.n + args[0], validate=True),
                [{'name': 'k', 'type':'int'}])

OPERATORS = [phi0, phi1, phi2, phi3, phi4]

#</OPERATORS>
