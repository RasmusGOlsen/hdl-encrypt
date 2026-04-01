
module top (input clk, input rst, output reg [7:0] count);

    // Normal code
    always @(posedge clk) begin
        if (rst) count <= 0;
    end

    `pragma protect begin
    // Secret logic
    always @(posedge clk) begin
        if (!rst) count <= count + 1;
    end
    `pragma protect end

    // More normal code
    assign some_signal = count[0];

endmodule
