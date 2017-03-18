import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

enum Event {b1}

enum State {State_1_1, State_6, State_2}


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
					callFunctionForActionWithLog("State_1_1_b1","win");
					currentState = State.State_6;
				}
			break;
			case State_6:
				if (event == Event.b1) {
					callFunctionForActionWithLog("State_1_b1","fail");
					currentState = State.State_2;
				}
			break;
			case State_2:
			break;
		}
	}
}
