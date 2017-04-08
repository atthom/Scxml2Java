import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

/* on liste tous les événements dans un énuméré*/
enum Event {b1, b2}

/* on liste tous les états dans un énuméré*/
enum State {State_1_1, State_6, State_9State_10, State_9State_12, State_11State_10, State_11State_12}

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
        this.currentState = State.State_1_1;
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
    public void callFunctionForAction(String action) {
        try {
            functions.get(action).invoke(context);
        } catch (NullPointerException | IllegalAccessException | InvocationTargetException e) {
            System.out.println("Function Not Found");
        }
    }

	/*similaire à callFunctionForAction, permet juste d'afficher un log en plus*/
    public void callFunctionForActionWithLog(String action, String log) {
        System.out.print(log + "\n");
        callFunctionForAction(action);
    }

	/*début du switch/case représentant les différents états de la machine a états fini.*/
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
