import unittest
from codeGen import *
from Action import *
from Transition import *
from State import *

class TestTransition(unittest.TestCase):
    def test_to_string(self):
        T1 = Transition("B1", "State1")
        self.assertEqual(T1.to_string(0), "if (event == Event.B1) {\n\tcurrentState = State.State1;\n}\n")
    

    def test_to_string_with_action(self):
        T1 = Transition("B1", "State1")
        A1 = Action("State_1_B1", "Ceci est un test avec log")
        T1.add_action(A1)
        value = "if (event == Event.B1) {\n\tcallFunctionForActionWithLog(\"State_1_B1\",\"Ceci est un test avec log\");\n\tcurrentState = State.State1;\n}\n"
        self.assertEqual(T1.to_string(0), value)
    

class TestAction(unittest.TestCase):
    def test_to_string_with_log(self):
        A1 = Action("State_1_B1", "Ceci est un test avec log")
        self.assertEqual(A1.to_string(0), "callFunctionForActionWithLog(\"State_1_B1\",\"Ceci est un test avec log\");\n")
        
    def test_to_string(self):
        A1 = Action("State_1_B1", None)
        A2 = Action("State_1_B1")
        self.assertEqual(A1.to_string(0), "callFunctionForAction(\"State_1_B1\");\n")
        self.assertEqual(A2.to_string(0), "callFunctionForAction(\"State_1_B1\");\n")
    
    def test_merge(self):
        A1 = Action("State_1_B1", "Ceci est un test avec log")
        A2 = Action("State_1_B2", "Ceci est un test avec second log")
        
        A2.merge(A1)
        self.assertEqual(A2.to_string(0),"callFunctionForActionWithLog(\"State_1_B2State_1_B1\",\"Ceci est un test avec second log\nCeci est un test avec log\");\n")

if __name__ == '__main__':
    unittest.main()