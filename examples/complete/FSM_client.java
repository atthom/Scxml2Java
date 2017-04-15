public class FSM_client {
	private FSM fsm;

	FSM_client() {
		// On connecte la FSM à notre classe pour avoir les fonctions
		fsm = new FSM(this);
		

		fsm.setFunctionsForAction("State_1_1_b1", "State_1_1_b1" );

		fsm.setFunctionsForAction("State_10_b2", "State_10_b2" );

		fsm.setFunctionsForAction("State_9_b1", "State_9_b1" );

		fsm.setFunctionsForAction("State_1_b1", "State_1_b1" );

		fsm.setFunctionsForAction("State_12_b1", "State_12_b1" );

		fsm.setFunctionsForAction("State_11_b2", "State_11_b2" );
	}

	public void exec() {
		fsm.activate(Event.b1);
		fsm.activate(Event.b1);
		fsm.activate(Event.b1);
		fsm.activate(Event.b1);
		fsm.activate(Event.b1);
		fsm.activate(Event.b1);
	}

	public void State_1_1_b1() {
		
	}
	public void State_10_b2() {
		
	}
	public void State_9_b1() {
		
	}
	public void State_1_b1() {
		
	}
	public void State_12_b1() {
		
	}
	public void State_11_b2() {
		
	}

}
