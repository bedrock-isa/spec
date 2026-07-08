`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
module bedrock_agu (
	request_i,
	base_reg_value_i,
	index_reg_value_i,
	pc_value_i,
	sp_value_i,
	payload_value_i,
	access_size_bytes_i,
	valid_o,
	address_valid_o,
	effective_address_o,
	immediate_value_o,
	update_write_o,
	update_value_o,
	update_invalid_o
);
	reg _sv2v_0;
	input wire [61:0] request_i;
	input wire [63:0] base_reg_value_i;
	input wire [63:0] index_reg_value_i;
	input wire [63:0] pc_value_i;
	input wire [63:0] sp_value_i;
	input wire [63:0] payload_value_i;
	input wire [3:0] access_size_bytes_i;
	output reg valid_o;
	output reg address_valid_o;
	output reg [63:0] effective_address_o;
	output reg [63:0] immediate_value_o;
	output reg update_write_o;
	output reg [63:0] update_value_o;
	output reg update_invalid_o;
	reg [63:0] base_value;
	reg [63:0] updated_base_value;
	reg [63:0] address_base_value;
	reg [63:0] displacement_value;
	reg [63:0] absolute_value;
	reg [63:0] index_value;
	reg [63:0] scaled_index_value;
	reg [63:0] update_amount;
	reg update_is_pre;
	reg update_is_dec;
	function automatic [63:0] sign_extend_payload;
		input reg [63:0] value;
		input reg [2:0] words;
		(* full_case, parallel_case *)
		case (words)
			3'd0: sign_extend_payload = 64'd0;
			3'd1: sign_extend_payload = {{48 {value[15]}}, value[15:0]};
			3'd2: sign_extend_payload = {{32 {value[31]}}, value[31:0]};
			default: sign_extend_payload = value;
		endcase
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		(* full_case, parallel_case *)
		case (request_i[10-:3])
			3'd1, 3'd2: base_value = base_reg_value_i;
			3'd4: base_value = sp_value_i;
			3'd3: base_value = pc_value_i;
			default: base_value = 64'd0;
		endcase
		displacement_value = (request_i[44] ? sign_extend_payload(payload_value_i, request_i[25-:3]) : 64'd0);
		absolute_value = (request_i[43] ? sign_extend_payload(payload_value_i, request_i[25-:3]) : 64'd0);
		index_value = (request_i[53] ? {{32 {index_reg_value_i[31]}}, index_reg_value_i[31:0]} : index_reg_value_i);
		scaled_index_value = (request_i[45] ? index_value << request_i[1-:2] : 64'd0);
		update_amount = {60'd0, access_size_bytes_i};
		update_is_pre = (request_i[22-:3] == 3'd2) || (request_i[22-:3] == 3'd4);
		update_is_dec = (request_i[22-:3] == 3'd3) || (request_i[22-:3] == 3'd4);
		updated_base_value = (update_is_dec ? base_value - update_amount : base_value + update_amount);
		address_base_value = (update_is_pre ? updated_base_value : base_value);
		effective_address_o = (request_i[43] ? absolute_value : (address_base_value + scaled_index_value) + displacement_value);
		immediate_value_o = payload_value_i;
		update_invalid_o = request_i[47] || (request_i[49] && (access_size_bytes_i == 4'd0));
		valid_o = (request_i[61] && request_i[51]) && !update_invalid_o;
		address_valid_o = valid_o && request_i[56];
		update_write_o = valid_o && request_i[49];
		update_value_o = (request_i[49] ? updated_base_value : base_value);
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
