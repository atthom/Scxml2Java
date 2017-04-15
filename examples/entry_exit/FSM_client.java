public class FSM_client {
	private FSM fsm;

	FSM_client() {
		// On connecte la FSM à notre classe pour avoir les fonctions
		fsm = new FSM(this);
		

		fsm.setFunctionsForAction("State_2_onentry", "State_2_onentry" );

		fsm.setFunctionsForAction("State_2_onexit", "State_2_onexit" );

		fsm.setFunctionsForAction("State_1_onentry", "State_1_onentry" );

		fsm.setFunctionsForAction("State_1_onexit", "State_1_onexit" );

		fsm.setFunctionsForAction("State_1_B3", "State_1_B3" );

		fsm.setFunctionsForAction("State_2_B1", "State_2_B1" );

		fsm.setFunctionsForAction("State_2_B2", "State_2_B2" );
	}

	public void exec() {
		fsm.activate(Event.B1);
	}

	public void State_2_onentry() {
		
	}
	public void State_2_onexit() {
		
	}
	public void State_1_onentry() {
		
	}
	public void State_1_onexit() {
		
	}
	public void State_1_B3() {
		
	}
	public void State_2_B1() {
		
	}
	public void State_2_B2() {
		
	}

}
