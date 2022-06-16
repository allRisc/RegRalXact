// This is a single line comment

/* 
 * This is a block comment
 */

module sample_module #(
    parameter int test = 1
) (
    input  wire       clk_in,
    input  wire       rst_low_in,
    input  wire [7:0] data_in,
    output wire       data_ready_out,
    output wire [7:0] data_out
);

    logic [7:0] reg_r;
    logic       ready_r;

    always_ff @( posedge clk_in, negedge rst_low_ing ) begin
        if (!rst_low_in) begin
            reg_r <= '0;
            ready_r <= '0;
        end 
        else begin
            reg_r <= data_in;
            ready_r <= |data_in;
        end
    end

    assign data_ready_out <= ready_r;
    assign data_out <= reg_r;
    
endmodule