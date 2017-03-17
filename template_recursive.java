import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

enum Event {b1, b2}

enum State {State_1, State_2, State_3, State_4, Final_1}


class FSM {
    private State currentState;
    private Map<String, Method> functions;
    private Object context;


    public FSM(Object context) {
        this.currentState = State.State_1;
        this.functions = new HashMap<>();
        this.context = context;
    }

    public void setFunctionsForAction(String action, String methodName) {
        try {
            functions.put(action, context.getClass().getMethod(methodName));
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        }
    }

    public void callFunctionForAction(String action) {
        try {
            functions.get(action).invoke(context);
        } catch (NullPointerException | IllegalAccessException | InvocationTargetException e) {
            System.out.println("Function Not Found");
        }
    }

    public void callFunctionForActionWithLog(String action, String log) {
        System.out.print(log + "\n");
        callFunctionForAction(action);
    }

	void activate(Event event) {
		switch (currentState) {
			switch (currentState) {
			case State_1:
				if (event == Event.b1) {
					callFunctionForActionWithLog("State_1_b1","hey i'm going to state2");
					currentState = State.State_2;
				}
				if (event == Event.b2) {
					callFunctionForAction("State_1_b2");
					currentState = State.State_3;
				}
			break;
			case State_2:
		            switch (currentState) {
		            case State_1_1:
		                if (event == Event.b2) {
                            callFunctionForAction("State_1_b2");
                            currentState = State.State_3;
                        }
		            break;
		            case State_1_2:
		                if (event == Event.b1) {
                            callFunctionForActionWithLog("State_1_b1","hey i'm going to state2");
                            currentState = State.State_2;
                        }
		            break;
		            }
				if (event == Event.b2) {
					callFunctionForActionWithLog("State_2_b2","hey i'm going to state3");
					currentState = State.State_3;
				}
			break;
			case State_3:
				if (event == Event.b1) {
					callFunctionForActionWithLog("State_3_b1","hey i'm going to state4");
					currentState = State.State_4;
				}
			break;
			case State_4:
				callFunctionForActionWithLog("State_4_onexit","i'm outta this state !");
				if (event == Event.b2) {
					callFunctionForActionWithLog("State_4_b2","hey i'm going to finiish!");
					currentState = State.Final_1;
				}
				callFunctionForActionWithLog("State_4_onexit","i'm outta this state !");
			break;
			case Final_1:
			break;
		}
	}
}