import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

/* on liste tous les événements dans un énuméré*/
enum Event {b1, b2}

/* on liste tous les états dans un énuméré*/
enum State {State_1, State_2, State_3, State_4, Final_1}

/*C'est la classe FSM java qui va être exécuté par le programme  en fonction de ses nécessités.*/
class FSM {
	/* l'état courant dans lequel se trouve la FSM */
    private State currentState;
	/* HashMap qui récupère toutes les méthodes qui seront déclenchée selon l'état et l'événement dans lequel on se trouve. */
    private Map<String, Method> functions;
    /* l'objet en contexte est la classe qui contient les fonctions de l'utilisateur, 
	Il est nécessaire d'avoir cet objet  pour déclencher les fonctions de l'utilisateur par le biais de la méthode Invoke*/
    private Object context;

	/*initialisation de la  machine a états finie, en fonction de la classe qui comprend les fonctions de l'utilisateur*/
    public FSM(Object context) {
        this.currentState = State.State_1;
        this.functions = new HashMap<>();
        this.context = context;
    }

	/*permet à un utilisateur de connecter sa fonction avec l'identifiant d'un état*/
	/*Il faut donner le nom de la fonction préalablement définie dans son object contexte et l'identifiant de l'état*/
    public void setFunctionsForAction(String action, String methodName) {
        try {
            functions.put(action, context.getClass().getMethod(methodName));
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        }
    }

	/*permet à la machine à état finie d'appeler la fonction en connaissant le nom de l'état courant*/
    private void callFunctionForAction(String action) {
        try {
            functions.get(action).invoke(context);
        } catch (NullPointerException | IllegalAccessException | InvocationTargetException e) {
            System.out.println("Function Not Found");
        }
    }

	/*similaire à callFunctionForAction, permet juste d'afficher un log en plus*/
    private void callFunctionForActionWithLog(String action, String log) {
        System.out.print(log + "\n");
        callFunctionForAction(action);
    }

	/*début du switch/case représentant les différents états de la machine a états fini.*/
    public void activate(Event event) {
		switch (currentState) {
			case State_1:
				if (event == Event.b1) {
					callFunctionForActionWithLog("State_1_b1","log(hey i'm going to state2)");
					currentState = State.State_2;
				}
				if (event == Event.b2) {
					callFunctionForAction("State_1_b2");
					currentState = State.State_3;
				}
			break;
			case State_2:
				if (event == Event.b2) {
					callFunctionForActionWithLog("State_2_b2","log(hey i'm going to state3)");
					currentState = State.State_3;
				}
			break;
			case State_3:
				if (event == Event.b1) {
					callFunctionForActionWithLog("State_3_b1","log(hey i'm going to state4)");
					currentState = State.State_4;
				}
			break;
			case State_4:
				callFunctionForActionWithLog("State_4_onentry","log(i'm entered in State_4)");
				if (event == Event.b2) {
					callFunctionForActionWithLog("State_4_b2","log(hey i'm going to finiish!)");
					currentState = State.Final_1;
				}
				callFunctionForActionWithLog("State_4_onexit","log(i'm outta this state !)");
			break;
			case Final_1:
			break;
		}
	}
}
