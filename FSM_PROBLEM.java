
    void activate(Event event) {
		switch (currentState) {
			case State_2:            
				callFunctionForActionWithLog("State_2_onentry","OnEntry du State1");
				callFunctionForActionWithLog("State_1_onentry","OnEntry du State1");
                /*
                should be 
				callFunctionForActionWithLog("State_1_onentry","OnEntry du State1");
                callFunctionForActionWithLog("State_2_onentry","OnEntry du State2");
                */

				if (event == Event.B1) {
					callFunctionForActionWithLog("State_2_B1","execute B1");
					currentState = State.State_2;
				}
				if (event == Event.B2) {
					callFunctionForActionWithLog("State_2_B2","execute B2");
					currentState = State.State_1;
                     /*
                    should be 
                    currentState = State.State_2;
                    */
				}
				if (event == Event.B3) {
					callFunctionForActionWithLog("State_1_B3","execute B3");
					currentState = State.State_1;
                     /*
                    should be 
                    currentState = State.State_2;
                    */
				}
				callFunctionForActionWithLog("State_2_onexit","OnExit du State 1");
				callFunctionForActionWithLog("State_1_onexit","OnExit du State 1");
                 /*
                 should be 
                 callFunctionForActionWithLog("State_2_onexit","OnExit du State 2");
				callFunctionForActionWithLog("State_1_onexit","OnExit du State 1");
                    */
			break;
		}
	}
