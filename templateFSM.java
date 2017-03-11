
enum Event {B1, B2};

enum State {State_1, State_2, State_3, State_4, Finish};


class FSM {
    private State currentState;

    public FSM() {
        this.currentState = State.State_1;
    }

    void action1() {
        System.out.print("hey i'm going to state2");
    }

    void action2() {
        System.out.print("hey i'm going to state3");
    }

    void action3() {
        System.out.print("hey i'm going to state4");
    }

    void action4() {
        System.out.print("hey i'm gonna finiiish !");
    }


    void activate(Event event) {
        switch (currentState) {
            case State_1:
                if(event==Event.B1) {
                    action1();
                    currentState = State.State_2;
                }
                break;
            case State_2:
                if(event==Event.B2) {
                    action2();
                    currentState = State.State_3;
                }
                break;
            case State_3:
                if(event==Event.B1) {
                    action3();
                    currentState = State.State_4;
                }
                break;
            case State_4:
                if(event==Event.B2) {
                    action4();
                    currentState = State.Finish;
                }
                break;
            case Finish:
                break;
        }
    }
}