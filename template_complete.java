import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

enum Event {b1, b2, e}

enum State {State_1_1, State_6, State_9, State_11, State_10, State_12}


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
			case State_9_State_10:
                if (event == Event.b1) {
                    callFunctionForAction("State_9_b1");
                    currentState = State.State_11_State_10;
                }
                if (event == Event.b2) {
                    callFunctionForAction("State_10_b2");
                    currentState = State.State_9_State_12;
                }
            break;
            case State_9_State_12:
            break;
            case State_11_State_10:
            break;
            case State_11_State_12:
            break;
		}
	}
}
