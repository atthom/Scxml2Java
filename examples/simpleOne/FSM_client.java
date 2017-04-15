public class FSM_client {
	private FSM fsm;

	FSM_client() {
		// On connecte la FSM à notre classe pour avoir les fonctions
		fsm = new FSM(this);
		

		fsm.setFunctionsForAction("State_1_b1", "State_1_b1" );

		fsm.setFunctionsForAction("State_3_b1", "State_3_b1" );

		fsm.setFunctionsForAction("State_2_b2", "State_2_b2" );

		fsm.setFunctionsForAction("State_4_b2", "State_4_b2" );
	}

	public void exec() {
		fsm.activate(Event.b1);
	}

	public void State_1_b1() {
		
	}
	public void State_3_b1() {
		
	}
	public void State_2_b2() {
		
	}
	public void State_4_b2() {
		
	}

}
