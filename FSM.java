import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

enum Event {b1, b2}

enum State {State_1_1, State_6, State_7, State_8, State_9State_10, State_9State_12, State_11State_10, State_11State_12}


class FSM {
    private State currentState;
    private Map<String, Method> functions;
    private Object context;


    public FSM(Object context) {
        this.currentState = State.State_1_1;
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
			case State_1_1:
				if (event == Event.b1) {
					callFunctionForAction("State_1_1_b1");
					currentState = State.State_6;
				}
			break;
			case State_6:
				if (event == Event.b1) {
					callFunctionForAction("State_1_b1");
					currentState = State.Parallel_1;
				}
			break;
			case State_9State_10:
				if (event == Event.b1) {
					callFunctionForAction("State_9_b1State_12_b1");
					currentState = State.State_11State_12;
				}
				if (event == Event.b2) {
					callFunctionForAction("State_10_b2");
					currentState = State.State_11State_12;
				}
			break;
			case State_9State_12:
				if (event == Event.b1) {
					callFunctionForAction("State_9_b1State_12_b1");
					currentState = State.State_11State_12State_10;
				}
			break;
			case State_11State_10:
				if (event == Event.b2) {
					callFunctionForAction("State_11_b2State_10_b2");
					currentState = State.State_9State_11State_12;
				}
			break;
			case State_11State_12:
				if (event == Event.b2) {
					callFunctionForAction("State_11_b2State_10_b2");
					currentState = State.State_9State_10;
				}
				if (event == Event.b1) {
					callFunctionForAction("State_12_b1");
					currentState = State.State_9State_10;
				}
			break;
		}
	}
}
