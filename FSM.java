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
	public T action_State_1_transitionb1(Callable<T> func) {
		System.out.print("hey i'm going to state2");
		func.call();
	}

	public T action_State_1_transitionb2(Callable<T> func) {
		func.call();
	}

	public T action_State_2_transitionb2(Callable<T> func) {
		System.out.print("hey i'm going to state3");
		func.call();
	}

	public T action_State_3_transitionb1(Callable<T> func) {
		System.out.print("hey i'm going to state4");
		func.call();
	}

	public T action_State_4_transitionb2(Callable<T> func) {
		System.out.print("hey i'm going to finiish!");
		func.call();
	}

	public T action_State_4_onentry(Callable<T> func) {
		System.out.print("i'm entered in State_4");
		func.call();
	}

	public T action_State_4_onexit(Callable<T> func) {
		System.out.print("i'm outta this state !");
		func.call();
	}

	void activate(Event event) {
		switch (currentState) {
			case State_1:
				if (event == Event.b1) {
					action_transitionb1();
					currentState = State.State_2;
				}
				if (event == Event.b2) {
					action_transitionb2();
					currentState = State.State_3;
				}
				
			break;
			case State_2:
				if (event == Event.b2) {
					action_transitionb2();
					currentState = State.State_3;
				}
				
			break;
			case State_3:
				if (event == Event.b1) {
					action_transitionb1();
					currentState = State.State_4;
				}
				
			break;
			case State_4:
				action_State_4onentry();
				if (event == Event.b2) {
					action_transitionb2();
					currentState = State.Final_1;
				}
				action_State_4onexit();
			break;
			case Final_1:
				
			break;
		}
	}
}
