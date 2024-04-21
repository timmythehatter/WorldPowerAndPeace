'''TestFormulationParamOpFloatStr.py
Unit-test formulation for clients that support
parameterized operators of types float (Python real number) and
str (Python string)..

For information about how the parameters are specified
and acquired during execution, see TestFormulationParmOpInteger.py.

'''

from soluzion import Basic_State, Basic_Operator, \
  Invalid_State_Exception

#<METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "Test Formulation for Real and String Parameters to Operators"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "21-JANUARY-2024"

PROBLEM_DESC=\
'''
This "problem" is trivial and exists only to support the
testing of the Real and String parameterized operators
mechanism.

The state contains to state variables: a real value which
should be between 0.0 and 1.0, and an arbitrary string.

There are three operators.
1. Get a new real value.
2. Get a new string value.
3. Get both in one operator application (via a sequence
 of prompts, rather than a combined form).
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>

class State(Basic_State):

  def __init__(self, realNum= 0.0, string='', validate=False):
    self.realNum = realNum
    self.string = string
    if validate:
      if (type(realNum) != type(0.0)):
        raise Invalid_State_Exception("realNum must be a float or double.")

  def is_goal(self):
    '''There is no goal to this "game".'''
    return False

  def goal_message(self):
    return "Congratulations on reaching the maximum state value!"

  def __eq__(self,s2):
    if s2==None: return False
    if self.realNum != s2.realNum: return False
    if self.string != s2.string: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    return "TPORS-Unit-tester State with realNum="+str(self.realNum)+\
      " and string: '"+self.string+"'"

  def __hash__(self):
    return (self.__str__()).__hash__()

class Operator(Basic_Operator):
  pass
#</COMMON_CODE>

#<OPERATORS>
# Operator to get the value of realNum:
phi0 = Operator("Get realNum",
                lambda s: True,
                lambda s,args: State(realNum=args[0], string=s.string),
                [{'name':'realNum', 'type':'float', 'min': 0.0, 'max': 1.0 }])

phi1 = Operator("Get string",
                lambda s: True,
                lambda s,args: State(string=args[0], realNum=s.realNum),
                [{'name':'string', 'type':'str' }])

phi2 = Operator("Get both",
                lambda s: True,
                lambda s,args: State(realNum=args[0], string=args[1]),
                [{'name':'realNum', 'type':'float', 'min': 0.0, 'max': 1.0 },\
                 {'name':'string', 'type':'str' }])


OPERATORS = [phi0, phi1, phi2]

#</OPERATORS>
