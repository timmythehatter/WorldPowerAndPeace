#!/usr/bin/python3
"""MinimalAutoPlayer.py
A minimal "client" program that will run some
game or problem-solving session by always trying
to choose the first applicable operator, and
if there are none, stopping.  This client 
waits 1 second after each move, so there will
be something to see when it runs."""

import time
TITLE="Minimal Auto-Player"
print(TITLE)

def run_session():
  print("Problem name and version: ", end="")
  print(PROBLEM.PROBLEM_NAME+"; "+PROBLEM.PROBLEM_VERSION)

  s = PROBLEM.State() # Create the initial state
  ops = applicable_ops(s)
  while(ops):
    print(s)
    try: 
      if s.is_goal():
        print('CONGRATULATIONS!')
        try:
          print(s.goal_message())
        except: pass
        return
    except: pass
    try:
       s = ops[0].apply(s)
    except Exception as e:
       print("Exception when applying operator "+ops[0].name)
       print(e)
       return
    time.sleep(1)
    ops = applicable_ops(s)  # Recompute the applicables.

def applicable_ops(s):
  """Returns the subset of OPERATORS whose preconditions are
       satisfied by the state s."""
  ao = [o for o in OPERATORS if o.is_applicable(s)]
  #print("Applicables: ", [o.name for o in ao])
  return ao

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

run_session()
