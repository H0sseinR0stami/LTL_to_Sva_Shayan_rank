
  // defining the flit ID -- One hot encoding
  `define HEADER  3'b001
  `define PAYLOAD 3'b010
  `define TAIL    3'b100

  // Specifying the FIFO parameters
  `define FIFO_DEPTH 'd4               // 4 flits capacity
  `define PTR_SIZE   `FIFO_DEPTH       // Controls reading and writing (for full and empty) >> Depends on the FIFO_DEPTH
  `define DATA_WIDTH 'd32              // # of data bits with parity