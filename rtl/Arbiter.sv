
module Arbiter (clk, 
                rst, 
                Req_N, Req_E, Req_W, Req_S, Req_L, // From LBDR modules (routing logic)
                DCTS, // Getting the CTS signal from the input FIFO of the next router/NI (for hand-shaking)
                Grant_N, Grant_E, Grant_W, Grant_S, Grant_L, // Grants given to LBDR (routing logic) requests (encoded as one-hot)
                Xbar_sel, // select lines for XBAR (crossbar switch)
                RTS // Valid output which is sent to the next router/NI to specify that the data on the output port is valid
            );

    // --                                                                        next
    // --                                     Arbiter                        router or NI
    // --                     --- ---------------------------- ----          ----
    // --   from LBDR  --->  |Req(s)                           RTS | -----> |DRTS
    // --    To FIFO   <---  |Grant(s)                         DCTS| <----- |CTS
    // --    to XBAR   <---  |Xbar_sel                             |        | 
    // --                     --- ---------------------------- ----          ----

    //  --------------------------------------------------------------------------------------------
    //  -- an example of a request/grant + handshake process with next router or NI

    // --CLK      _|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|_|'|__

    // -- Req     _____|'''''''''''''''''''''''''''''''''''''''''''|________

    // --         _________ ___________________ _______ _______ _______ ____
    // -- TX      _________X_______HEADER______X_Body__X_Body__X__Tail_X____

    // -- Grant   _________________________|'''|___|'''|___|'''|____________

    // --  RTS    _________|'''''''''''''''''''|___|'''''''|___|'''''''|____

    // --  DCTS   _________________________|'''|_______|'''|_______|'''|____  (CTS (DCTS) is always maximum 1 clock cycle!)
    // --                                  |<---------clear----------->|
    // --                                  |         to send           |
    //  --------------------------------------------------------------------------------------------

    input   clk, rst;
    input   Req_N, Req_E, Req_W, Req_S, Req_L;
    input   DCTS;
    output  logic Grant_N, Grant_E, Grant_W, Grant_S, Grant_L;
    output  logic [4:0] Xbar_sel;
    output  logic RTS;

    typedef enum bit [5:0] {IDLE = 6'b000001, Local = 6'b000010, North = 6'b000100, East = 6'b001000, West = 6'b010000, South = 6'b100000} STATE_TYPE;

    STATE_TYPE state = IDLE;
    STATE_TYPE state_in = IDLE;
    STATE_TYPE next_state = IDLE;

    logic RTS_FF = 0;
    logic RTS_FF_in = 0;


    // Sequential part
    // rst is active high!
    always @(posedge clk) begin

     if (rst) begin
        state  <= IDLE;
        RTS_FF <= 0;
     end
     else begin
        // no grant given yet, it might be that there is no request to 
        // arbiter or request is there, but the next router's/NI's FIFO is full
        state <= state_in;
        RTS_FF <= RTS_FF_in;   
      end
    end 


    // Anything below here is pure combinational

    assign RTS = RTS_FF;

    always @(RTS_FF, DCTS, state, next_state) begin
        if (RTS_FF && !DCTS) 
            state_in <= state;
        else
            state_in <= next_state;
    end


    always @(state, RTS_FF, DCTS) begin
        if (state == IDLE) begin 
            RTS_FF_in <= 0;
            // if there was a grant given to one of the inputs, 
            // tell the next router/NI that the output data is valid
        end
        else begin
            if (RTS_FF && DCTS)
                RTS_FF_in <= 0;
            else 
                RTS_FF_in <= 1;
        end
    end

    // Sets the grants using round robin 
    // the order is   L --> N --> E --> W --> S  and  back to L
    always @(state, Req_N, Req_E, Req_W, Req_S, Req_L, DCTS, RTS_FF) begin
        Grant_N  <= 0;
        Grant_E  <= 0;
        Grant_W  <= 0;
        Grant_S  <= 0;
        Grant_L  <= 0;
        Xbar_sel <= 5'b00000; 

        case(state)
            IDLE: begin
                Xbar_sel<= 5'b00000; 
                
                if (Req_L) 
                    next_state <= Local;
                else if (Req_N) 
                    next_state <= North;         
                else if (Req_E) 
                    next_state <= East;
                else if (Req_W) 
                    next_state <= West;
                else if (Req_S) 
                    next_state <= South;
                else
                    next_state <= IDLE;
            end

            North: begin
                Grant_N <= DCTS & RTS_FF ;
                Xbar_sel<= 5'b00001;
                
                if (Req_N)  
                    next_state <= North; 
                else if (Req_E) 
                    next_state <= East;
                else if (Req_W) 
                    next_state <= West;
                else if (Req_S) 
                    next_state <= South;
                else if (Req_L) 
                    next_state <= Local;
                else
                    next_state <= IDLE; 
            end 

            East: begin
                Grant_E <= DCTS & RTS_FF;
                Xbar_sel<= 5'b00010;
                
                if (Req_E)  
                    next_state <= East; 
                else if (Req_W) 
                    next_state <= West;
                else if (Req_S) 
                    next_state <= South;
                else if (Req_L) 
                    next_state <= Local;
                else if (Req_N) 
                    next_state <= North;
                else
                    next_state <= IDLE; 
            end 

            West: begin
                Grant_W <= DCTS & RTS_FF;
                Xbar_sel<= 5'b00100;
                
                if (Req_W ) 
                    next_state <= West; 
                else if (Req_S ) 
                    next_state <= South;
                else if (Req_L ) 
                    next_state <= Local;
                else if (Req_N ) 
                    next_state <= North;
                else if (Req_E ) 
                    next_state <= East;
                else
                    next_state <= IDLE; 
            end

            South: begin
                Grant_S <= DCTS & RTS_FF;
                Xbar_sel<= 5'b01000;
                
                if (Req_S )
                    next_state <= South; 
                else if (Req_L)
                    next_state <= Local;
                else if (Req_N)
                    next_state <= North;
                else if (Req_E)
                    next_state <= East;
                else if (Req_W)
                    next_state <= West;
                else
                    next_state <= IDLE; 
            end

            default: begin // Including Local and invalid states (non- onehot!)
                Grant_L <= DCTS & RTS_FF;
                Xbar_sel<= 5'b10000;
                
                if (Req_L)
                    next_state <= Local; 
                else if (Req_N)
                    next_state <= North;         
                else if (Req_E )
                    next_state <= East;
                else if (Req_W )
                    next_state <= West;
                else if (Req_S )
                    next_state <= South;
                else
                    next_state <= IDLE; 
            end
        endcase
    end

endmodule