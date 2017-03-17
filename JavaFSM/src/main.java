/**
 * Created by Thom on 03/03/2017.
 */
public class main {
    public static void main (String[] args){
        System.out.println("Main func");

        FSM fsm = new FSM(new main());
        // écriture arcanique pour faire passer les méthodes de la classe main vers la FSM

        fsm.setFunctionsForAction( "action_transition_b1","yetAnotherfunct");
        //
        //      fsm.setFunctionsForAction("action_transition_b1", main2.yetAnotherfunct());
        fsm.setFunctionsForAction( "action_State_4onexit","REM");
        fsm.activate(Event.b1);
        fsm.activate(Event.b2);
        fsm.activate(Event.b2);
        fsm.activate(Event.b1);
        fsm.activate(Event.b2);

    }


    public void yetAnotherfunct() {
        System.out.println("pezokpzaeokfezpokfepok\n");
    }




    public void REM() {
        System.out.println("It's the end of the hello world, as we know it !\n");
    }

}
