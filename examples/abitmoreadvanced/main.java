/**
 * Created by Thom on 03/03/2017.
 */
public class main {
    public int call_counter = 0;
    static FSM fsm;

    public static void main (String[] args){
        System.out.println("Main func");

        // On connecte la FSM à notre classe pour avoir les fonctions
        fsm = new FSM(new main());

        // on connecte chaque nom de fonction à un état particulier
        fsm.setFunctionsForAction("State_1_b1", "state1" );
        fsm.setFunctionsForAction("State_2_b2", "state2" );
        fsm.setFunctionsForAction("State_3_b1", "state3" );
        fsm.setFunctionsForAction("State_4_b2", "last" );
        fsm.setFunctionsForAction("State_4_onexit", "REM" );

        fsm.activate(Event.b1);
        fsm.activate(Event.b2);
        fsm.activate(Event.b2); // this one should do nothing
        fsm.activate(Event.b1);
        fsm.activate(Event.b2);
        
    }

    public void state1() {
        call_counter++;
    }

    public void state2() {
        call_counter+=10;
    }

    public void state3() {
        call_counter+=100;
    }

    public void last() {
        System.out.println("La variable counter est à " + call_counter);
    }

    public void REM() {
        System.out.println("It's the end of the word as we know it");
    }


}
