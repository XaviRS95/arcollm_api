module master_fsm(
    input wire clk,
    input wire reset,
    input wire start,
    output reg request,
    input wire ack,
    output reg done
);

    typedef enum {IDLE, REQUESTED, WAITING, DONE} state_t;
    state_t state, next_state;

    // State transition logic
    always @(posedge clk or posedge reset) begin
        if (reset)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next state logic
    always @(*) begin
        case (state)
            IDLE: 
                if (start == 1'b1)
                    next_state = REQUESTED;
                else
                    next_state = IDLE;
            REQUESTED: 
                next_state = WAITING;
            WAITING: 
                if (ack == 1'b1)
                    next_state = DONE;
                else
                    next_state = WAITING;
            DONE: 
                next_state = IDLE;
            default: 
                next_state = IDLE;
        endcase
    end

    // Output logic
    always @(*) begin
        request = 1'b0;
        done = 1'b0;
        case (state)
            REQUESTED: 
                request = 1'b1;
            DONE: 
                done = 1'b1;
            default: ;
        endcase
    end
endmodule
