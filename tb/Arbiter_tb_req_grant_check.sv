
module Arbiter_tb_req_grant_check();

  // Declaring the port variables for DUT
  reg bfm_clk;
  reg [5:0] bfm_command;
  
  wire bfm_grant;
  
  // BFM commands Declaration
  parameter NOREQ1 = 6'd1,
            REQFL  = 6'd2,
            REQFN  = 6'd3,
            REQFE  = 6'd4,
            REQFW  = 6'd5,
            REQFS  = 6'd6,
            NOREQ2 = 6'd7,
            REQFLN = 6'd8,
            REQFLE = 6'd9,
            REQFLW = 6'd10,
            REQFLS = 6'd11,
            REQFLL = 6'd12,
            REQFNE = 6'd13,
            REQFNW = 6'd14,
            REQFNS = 6'd15,
            REQFNL = 6'd16,
            REQFNN = 6'd17,
            REQFEW = 6'd18,
            REQFES = 6'd19,
            REQFEL = 6'd20,
            REQFEN = 6'd21,
            REQFEE = 6'd22,
            REQFWS = 6'd23,
            REQFWL = 6'd24,
            REQFWN = 6'd25,
            REQFWE = 6'd26,
            REQFWW = 6'd27,
            REQFSL = 6'd28,
            REQFSN = 6'd29,
            REQFSE = 6'd30,
            REQFSW = 6'd31,
            REQFSS = 6'd32;

  // Instantiate BFM
  bfm_arbiter BFM (bfm_clk, bfm_command, bfm_grant);
  
  // Specify the CYCLE parameter
  parameter CYCLE = 10;
  
  // Generating Clock of period 10ns
  initial begin
    bfm_clk = 0;
    forever
      #(CYCLE/2) bfm_clk = ~bfm_clk;
  end
  
  // Applying Commands
  initial begin : SIM
    BFM.reset;
    
    bfm_command = NOREQ1;
    @(posedge bfm_grant);

    bfm_command = REQFL;
    @(posedge bfm_grant);

    bfm_command = REQFN;
    @(posedge bfm_grant);

    bfm_command = REQFE;
    @(posedge bfm_grant);

    bfm_command = REQFW;
    @(posedge bfm_grant);

    bfm_command = REQFS;
    @(posedge bfm_grant);

    bfm_command = NOREQ2;
    @(posedge bfm_grant);

    bfm_command = REQFLN;
    @(posedge bfm_grant);

    bfm_command = REQFNE;
    @(posedge bfm_grant);

    bfm_command = REQFEW;
    @(posedge bfm_grant);

    bfm_command = REQFWS;
    @(posedge bfm_grant);

    bfm_command = REQFSL;
    @(posedge bfm_grant);

    bfm_command = REQFLL;
    @(posedge bfm_grant);

    bfm_command = REQFLE;
    @(posedge bfm_grant);

    bfm_command = REQFES;
    @(posedge bfm_grant);

    bfm_command = REQFSN;
    @(posedge bfm_grant);

    bfm_command = REQFNN;
    @(posedge bfm_grant);

    bfm_command = REQFNW;
    @(posedge bfm_grant);

    bfm_command = REQFWL;
    @(posedge bfm_grant);

    bfm_command = REQFLW;
    @(posedge bfm_grant);

    bfm_command = REQFWE;
    @(posedge bfm_grant);

    bfm_command = REQFEE;
    @(posedge bfm_grant);

    bfm_command = REQFEN;
    @(posedge bfm_grant);

    bfm_command = REQFNL;
    @(posedge bfm_grant);

    bfm_command = REQFLS;
    @(posedge bfm_grant);

    bfm_command = REQFSS;
    @(posedge bfm_grant);

    bfm_command = REQFSW;
    @(posedge bfm_grant);

    bfm_command = REQFWW;
    @(posedge bfm_grant);

    bfm_command = REQFWN;
    @(posedge bfm_grant);

    bfm_command = REQFNS;
    @(posedge bfm_grant);

    bfm_command = REQFSE;
    @(posedge bfm_grant);

    bfm_command = REQFEL;
    @(posedge bfm_grant);

    bfm_command = NOREQ2;
    @(posedge bfm_grant);

    //For toggle coverage of reset
    BFM.reset;

    $display("\n ****** Simulation Complete ********** \n");
    #(CYCLE * 2); 
    $stop;
  
  end


endmodule

