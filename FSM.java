import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

enum Event {B1, B2, B3}

enum State {State_2}


class FSM {
    private State currentState;
    private Map<String, Method> functions;
    private Object context;


    public FSM(Object context) {
        this.currentState = State.State_2;
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
			case State_2:
				callFunctionForActionWithLog("State_1_onentry","OnEntry du State1");
				callFunctionForActionWithLog("State_2_onentry","OnEntry du State2");
				if (event == Event.B1) {
					callFunctionForActionWithLog("State_2_B1","execute B1");
					currentState = State.State_2;
				}
				if (event == Event.B2) {
					callFunctionForActionWithLog("State_2_B2","execute B2");
					currentState = State.State_2;
				}
				if (event == Event.B3) {
					callFunctionForActionWithLog("State_1_B3","execute B3");
					currentState = State.State_1;
				}
				callFunctionForActionWithLog("State_2_onexit","OnExit du state2");
				callFunctionForActionWithLog("State_1_onexit","OnExit du State 1");
			break;
		}
	}
}
