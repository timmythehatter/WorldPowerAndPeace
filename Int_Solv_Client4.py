#!/usr/bin/python3
"""Int_Solv_Client4b.py
(VARIATION ON Int_Solv_Client4a.py that handles operators
with integer, real, and string parameters)
 Experimental, as of Jan. 21, 2024, it is working with
3 types of parameters: int, float, str.

 This file implements a simple interactive problem-solving
 client. The user can interactively explore a problem space
 for a suitably-formulated problem.  The user only has to
 input single-character commands to control the search.
 Output is purely textual, and thus the complexity of a
 graphical interface is avoided.

 This client runs standalone -- no server connection.
 It thus provides a bare-bones means of testing a problem
 formulation.

 This file corresponds to version 3 of the software.
 It is compatible with problems whose formulations use
 a class called State for representing problem states.
 Last updated November 1, 2023.
 Previously (version 3) updated August 21, 2019.

----

PURPOSE OF THIS MODULE:
        
    This module supports what we can call "interactive state
    space search".  Whereas traditional search algorithms in the
    context of artificial intelligence work completely automatically,
    this module lets the user make the moves.  It provides support
    to the user in terms of computing new states, displaying that
    portion of the state space that the user has embodied, and
    providing controls to permit the user to adapt the presentation
    to his or her needs.  This type of tool could ultimately be a
    powerful problem solving tool, useful in several different
    modes of use: interactive processing of individual objects,
    programming by demonstration (the path from the root to any
    other node in the state space represents a way of processing
    any object similar in structure to that of the root object.)

    """

TITLE="Interactive Solving Client (Version 4)"
print(TITLE)

def mainloop():
  print("Problem name and version: ", end="")
  print(PROBLEM.PROBLEM_NAME+"; "+PROBLEM.PROBLEM_VERSION)
  global STEP, DEPTH, OPERATORS, CURRENT_STATE, STATE_STACK
  CURRENT_STATE = PROBLEM.State() # Create the initial state

  STATE_STACK = [CURRENT_STATE]
  STEP = 0
  DEPTH = 0
  while(True):
    print("\nStep "+str(STEP)+", Depth "+str(DEPTH))
    print("CURRENT_STATE = "+str(CURRENT_STATE))
    if CURRENT_STATE.is_goal():
      print('''CONGRATULATIONS!
You have solved the problem by reaching a goal state.
''')
      print(CURRENT_STATE.goal_message())
      print('''
Do you wish to continue exploring?
''')
      answer = input("Y or N? >> ")
      if answer=="Y" or answer=="y": print("OK, continue")
      else: return

    applicability_vector = get_applicability_vector(CURRENT_STATE)
    #print("applicability_vector = "+str(applicability_vector))
    for i in range(len(OPERATORS)):
      if applicability_vector[i]:
        print(str(i)+": "+OPERATORS[i].name)
    command = input("Enter command: 0, 1, 2, etc. for operator; B-back; H-help; Q-quit. >> ")
    if command=="B" or command=="b": 
      if len(STATE_STACK)>1:
        STATE_STACK.pop()
        DEPTH -= 1
        STEP += 1
      else:
        print("You're already back at the initial state.")
      CURRENT_STATE = STATE_STACK[-1]
      continue

    if command=="H" or command=="h": show_instructions(); continue
    if command=="Q" or command=="q": break
    if command=="": continue
    try:
      i = int(command)
    except:
      print("Unknown command or bad operator number.")
      continue
    print("Operator "+str(i)+" selected.")
    if i<0 or i>= len(OPERATORS):
      print("There is no operator with number "+str(i))
      continue
    if applicability_vector[i]:
      try:
       CURRENT_STATE = OPERATORS[i].apply(CURRENT_STATE)
       STATE_STACK.append(CURRENT_STATE)
       DEPTH += 1
       STEP += 1
      except Exception as e:
       print("------------- NOTE: ----------------")
       print("Aborting use of operator: "+OPERATORS[i].name+". "+str(e))
      continue
    else:
       print("Operator "+str(i)+" is not applicable to the current state.")
       continue
    #print("Operator "+command+" not yet supported.")

def get_applicability_vector(s):
    #print("OPERATORS: "+str(OPERATORS))
    return [op.is_applicable(s) for op in OPERATORS]  

def exit_client():
  print("Terminating Text_SOLUZION_Client session.")
  log("Exiting")
  exit()
  

def show_instructions():
  print('''\nINSTRUCTIONS:\n
The current state of your problem session represents where you
are in the problem-solving process.  You can try to progress
forward by applying an operator to change the state.
To do this, type the number of an applicable operator.
The program shows you a list of what operators are 
applicable in the current state.

You can also go backwards (undoing a previous step)
by typing 'B'.  

If you reach a goal state, you have solved the problem,
and the computer will usually tell you that, but it depends
on what kind of problem you are solving.''')
      
def apply_one_op():
    """Populate a popup menu with the names of currently applicable
       operators, and let the user choose which one to apply."""
    currently_applicable_ops = applicable_ops(CURRENT_STATE)
    #print "Applicable operators: ",\
    #    map(lambda o: o.name, currently_applicable_ops)
    #print("Now need to apply the op")

def applicable_ops(s):
    """Returns the subset of OPERATORS whose preconditions are
       satisfied by the state s."""
    return [o for o in OPERATORS if o.is_applicable(s)]

import sys, importlib.util

# Get the PROBLEM name from the command-line arguments

if len(sys.argv)<2:
  print('''
       Usage: 
./Int_Solv_Client <PROBLEM NAME>
       For example:
./Int_Solv_Client Missionaries
  ''')
  exit(1)
  
problem_name = sys.argv[1]
print("Problem folder name is: "+problem_name)
print("Problem file name is: "+problem_name+".py")

try:
  spec = importlib.util.spec_from_file_location(problem_name, problem_name+".py")
  PROBLEM = spec.loader.load_module()
except Exception as e:
  print(e)
  exit(1)

OPERATORS=PROBLEM.OPERATORS
STATE_STACK = []

import soluzion as SZ

def get_args(op : SZ.Basic_Operator):
  '''Defines a method that will get, from the user,
  a list of arguments in order to apply a parameterized
  operator.  How the interaction happens is defined here
  in the client program, but the file soluzion.py needs
  to call this in order to handle operator application.
  So once it is defined here, it is written into the
  soluzion module, overwriting the stub there. '''
  if not op.params: return []  # No parameters
  p_list = op.params
  if type(p_list)==type(get_args): # Test to see if the param list
    # depends on the current state. If so, its a function; evaluate it.
    #print(" Evaluating the parameter-list function to get the parameter list.")
    p_list = p_list(CURRENT_STATE)
    #print("The argument list is: ")
    #print(p_list)
  arglist = [get_arg(param, op) for param in p_list]
  return arglist

NEG_INF = float('-inf')
POS_INF = float('inf')

def get_arg(param, op : SZ.Basic_Operator):
  # Get a value for the given param, to use in applying op.
  # param is given as a dictionary.
  # op is included here, in case the UI should mention the
  # name of the operator for which the parameter is requested.
  #print("In get_arg, param="); print(param)
  name = param['name']
  p_type = param['type']
  if p_type == 'int':
    arg = get_int(name, param, op)
    return arg
  if p_type == 'float':
    arg = get_float(name, param, op)
    return arg
  if p_type == 'str':
    arg = get_str(name, param, op)
    return arg
  else: return None

def get_int(name, param, op):
    #print("In get_int, param = "); print(param)
    try:
      min_int = param['min']
    except:
      #print("Did not find a min property of int. Using -inf.")
      min_int = NEG_INF
    try:
      max_int = param['max']
    except:
      #print("Did not find a max property of int. Using inf.")
      max_int = POS_INF
    op_name = op.name
    prompt = "Enter an integer in the range ["+str(min_int)+".."+\
     str(max_int)+"] for parameter "+name+" in operator \""+op_name+"\": "
    done = False
    while not done:
      try:
        response = input(prompt)
        arg = int(response)
        if arg < min_int:
          print("Integer is too low. Try again. ")
        elif arg > max_int:
          print("Integer is too high. Try again. ")
        else:          
          done = True
      except:
        print("Invalid integer. Try again. ")
    return arg

def get_float(name, param, op):
    try:
      min_float = param['min']
    except:
      min_float = NEG_INF
    try:
      max_float = param['max']
    except:
      max_float = POS_INF
    op_name = op.name
    prompt = "Enter a real number in the range ["+str(min_float)+".."+\
     str(max_float)+"] for parameter "+name+" in operator \""+op_name+"\": "
    done = False
    while not done:
      try:
        response = input(prompt)
        arg = float(response)
        if arg < min_float:
          print("Number is too low. Try again. ")
        elif arg > max_float:
          print("Number is too high. Try again. ")
        else:          
          done = True
      except:
        print("Invalid float. Try again. ")
    return arg

def get_str(name, param, op):
    op_name = op.name
    prompt = "Enter a string for parameter "+name+" in operator \""+op_name+"\": "
    response = input(prompt)
    return response  # Probably we should embed this is a try-except form.

SZ.GET_ARGS = get_args

  # The following is only executed if this module is being run as the main
# program, rather than imported from another one.
if __name__ == '__main__':
  mainloop()
  print("The session is finished.")



  
