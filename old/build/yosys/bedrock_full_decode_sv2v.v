`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
`default_nettype wire
`default_nettype none
module bedrock_decode (
	primary_payload_i,
	extension_word_i,
	valid_o,
	needs_extension_o,
	opcode_id_o,
	field_format_id_o,
	required_words_o,
	ext_root_o,
	repcc_allowed_o,
	repg_allowed_o,
	repg_fast_candidate_o
);
	reg _sv2v_0;
	localparam signed [31:0] bedrock_pkg_PRIMARY_PAYLOAD_BITS = 12;
	input wire [11:0] primary_payload_i;
	input wire [15:0] extension_word_i;
	output reg valid_o;
	output reg needs_extension_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_OPCODE_ID_BITS = 8;
	output reg [7:0] opcode_id_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_FIELD_FORMAT_ID_BITS = 6;
	output reg [5:0] field_format_id_o;
	output reg [3:0] required_words_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_EXT_ROOT_BITS = 5;
	output reg [4:0] ext_root_o;
	output reg repcc_allowed_o;
	output reg repg_allowed_o;
	output reg repg_fast_candidate_o;
	reg [27:0] primary_decode;
	reg [21:0] extended_decode;
	reg [3:0] field_format_token_words;
	reg repcc_allowed;
	reg repg_allowed;
	reg repg_fast_candidate;
	function automatic [7:0] sv2v_cast_BD1B7;
		input reg [7:0] inp;
		sv2v_cast_BD1B7 = inp;
	endfunction
	function automatic [5:0] sv2v_cast_6D350;
		input reg [5:0] inp;
		sv2v_cast_6D350 = inp;
	endfunction
	function automatic [4:0] sv2v_cast_7D91B;
		input reg [4:0] inp;
		sv2v_cast_7D91B = inp;
	endfunction
	function automatic [21:0] bedrock_decode_pkg_bedrock_decode_extended_opcode;
		input reg [4:0] ext_root;
		input reg [15:0] extension_word;
		reg [21:0] r;
		begin
			r = 1'sb0;
			r[20-:8] = sv2v_cast_BD1B7(8'd0);
			r[12-:6] = sv2v_cast_6D350(6'd0);
			r[6-:4] = 4'd2;
			(* full_case, parallel_case *)
			case (ext_root)
				sv2v_cast_7D91B(5'd1):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000000000000zz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd26);
							r[12-:6] = sv2v_cast_6D350(6'd63);
						end
						16'b0000000000000100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd64);
							r[12-:6] = sv2v_cast_6D350(6'd62);
						end
						16'b0000000000000101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd65);
							r[12-:6] = sv2v_cast_6D350(6'd62);
						end
						16'b0000000000000110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd66);
							r[12-:6] = sv2v_cast_6D350(6'd62);
						end
						16'b0000000000000111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd67);
							r[12-:6] = sv2v_cast_6D350(6'd62);
						end
						16'b0000000000001000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd68);
							r[12-:6] = sv2v_cast_6D350(6'd62);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd2):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd152);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd3):
					if (extension_word <= 16'h07ff) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd36);
						r[12-:6] = sv2v_cast_6D350(6'd61);
					end
					else if ((extension_word >= 16'h0800) && (extension_word <= 16'h0bff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd86);
						r[12-:6] = sv2v_cast_6D350(6'd55);
					end
					else if ((extension_word >= 16'h0c00) && (extension_word <= 16'h0c7f)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd121);
						r[12-:6] = sv2v_cast_6D350(6'd28);
					end
					else if ((extension_word >= 16'h0c00) && (extension_word <= 16'h0c7f)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd120);
						r[12-:6] = sv2v_cast_6D350(6'd54);
					end
					else if (extension_word == 16'h0c80) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd192);
						r[12-:6] = sv2v_cast_6D350(6'd0);
					end
					else if (extension_word == 16'h0c80) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd193);
						r[12-:6] = sv2v_cast_6D350(6'd8);
					end
					else if ((extension_word >= 16'h0d00) && (extension_word <= 16'h0dff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd179);
						r[12-:6] = sv2v_cast_6D350(6'd53);
					end
					else if ((extension_word >= 16'h1000) && (extension_word <= 16'h17ff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd134);
						r[12-:6] = sv2v_cast_6D350(6'd60);
					end
					else if ((extension_word >= 16'h1800) && (extension_word <= 16'h1fff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd134);
						r[12-:6] = sv2v_cast_6D350(6'd61);
					end
					else if ((extension_word >= 16'h2000) && (extension_word <= 16'h27ff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd134);
						r[12-:6] = sv2v_cast_6D350(6'd60);
					end
					else if ((extension_word >= 16'h2800) && (extension_word <= 16'h2fff)) begin
						r[21] = 1'b1;
						r[20-:8] = sv2v_cast_BD1B7(8'd134);
						r[12-:6] = sv2v_cast_6D350(6'd61);
					end
				sv2v_cast_7D91B(5'd4):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd19);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000001000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd125);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000001zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd122);
							r[12-:6] = sv2v_cast_6D350(6'd21);
						end
						16'b0000010zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd124);
							r[12-:6] = sv2v_cast_6D350(6'd21);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd5):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd133);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd133);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd203);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd203);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd133);
							r[12-:6] = sv2v_cast_6D350(6'd43);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd6):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000000zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd109);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000001zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd178);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b000000000001zzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd135);
							r[12-:6] = sv2v_cast_6D350(6'd10);
						end
						16'b000000000010zzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd136);
							r[12-:6] = sv2v_cast_6D350(6'd10);
						end
						16'b000000000011zzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd178);
							r[12-:6] = sv2v_cast_6D350(6'd2);
						end
						16'b000000000100zzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd204);
							r[12-:6] = sv2v_cast_6D350(6'd10);
						end
						16'b000000000101zzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd205);
							r[12-:6] = sv2v_cast_6D350(6'd10);
						end
						16'b00000001zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd137);
							r[12-:6] = sv2v_cast_6D350(6'd31);
						end
						16'b00000010zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd206);
							r[12-:6] = sv2v_cast_6D350(6'd31);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd7):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd123);
							r[12-:6] = sv2v_cast_6D350(6'd19);
						end
						16'b0000001zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd177);
							r[12-:6] = sv2v_cast_6D350(6'd19);
						end
						16'b0000010000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd190);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd8):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd44);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000000001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd44);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000000010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd46);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000000000011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd50);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b000000000000010z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd50);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b000000000000011z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd51);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000001000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd51);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000001001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd52);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b000000000000101z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd52);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b000000000000110z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd53);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000001110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd53);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000001111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd54);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd54);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd58);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd63);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000000010011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd71);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd71);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd72);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd73);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000010111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd74);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000011000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd74);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000011001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd75);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000011010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd75);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000000011011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd81);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000000001110z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd81);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000000001111z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd81);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00000000001zzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd56);
							r[12-:6] = sv2v_cast_6D350(6'd6);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000001zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd56);
							r[12-:6] = sv2v_cast_6D350(6'd5);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd82);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010000001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd83);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010000010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd84);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010000011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd88);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001000010z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd88);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001000011z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd88);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010001000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd89);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010001001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd90);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010001010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd90);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010001011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd91);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001000110z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd91);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001000111z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd91);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001001000z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd92);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b000000001001001z: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd92);
							r[12-:6] = sv2v_cast_6D350(6'd59);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010010100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd92);
							r[12-:6] = sv2v_cast_6D350(6'd58);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000010010101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd93);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000010010110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd94);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010010111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd95);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010011000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd95);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000010011001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd96);
							r[12-:6] = sv2v_cast_6D350(6'd50);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b000001zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd108);
							r[12-:6] = sv2v_cast_6D350(6'd24);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd44);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd46);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd54);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd63);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd71);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd72);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd73);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd74);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd75);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd82);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd83);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd84);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd89);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd90);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd94);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd95);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd96);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b1001zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd100);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b1010zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd100);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd100);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd101);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b1100zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd101);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b1101zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd106);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b1110zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd106);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd106);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd9):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd57);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000100000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd105);
							r[12-:6] = sv2v_cast_6D350(6'd25);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00001000010zzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd87);
							r[12-:6] = sv2v_cast_6D350(6'd26);
						end
						16'b00001001zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd61);
							r[12-:6] = sv2v_cast_6D350(6'd15);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000101zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd55);
							r[12-:6] = sv2v_cast_6D350(6'd38);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00001100zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd61);
							r[12-:6] = sv2v_cast_6D350(6'd15);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00001101zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd62);
							r[12-:6] = sv2v_cast_6D350(6'd15);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00001110zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd62);
							r[12-:6] = sv2v_cast_6D350(6'd15);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0001zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd57);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b001000000zzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd105);
							r[12-:6] = sv2v_cast_6D350(6'd22);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b001001zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd61);
							r[12-:6] = sv2v_cast_6D350(6'd24);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd85);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0011zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd85);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0100zzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd85);
							r[12-:6] = sv2v_cast_6D350(6'd44);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b010100zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd62);
							r[12-:6] = sv2v_cast_6D350(6'd24);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd10):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd45);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd47);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd48);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd49);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd59);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd60);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd69);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd70);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd76);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd77);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd78);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd79);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd97);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd98);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd99);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd102);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd103);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd104);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd107);
							r[12-:6] = sv2v_cast_6D350(6'd51);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd11):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000000zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd1);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000100000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd2);
							r[12-:6] = sv2v_cast_6D350(6'd46);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000100000001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd2);
							r[12-:6] = sv2v_cast_6D350(6'd46);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000100000010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd2);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000100000011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd3);
							r[12-:6] = sv2v_cast_6D350(6'd46);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100000100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd3);
							r[12-:6] = sv2v_cast_6D350(6'd46);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100000101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd3);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100000110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd5);
							r[12-:6] = sv2v_cast_6D350(6'd46);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100000111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd5);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd25);
							r[12-:6] = sv2v_cast_6D350(6'd49);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd25);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd38);
							r[12-:6] = sv2v_cast_6D350(6'd47);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd39);
							r[12-:6] = sv2v_cast_6D350(6'd48);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd40);
							r[12-:6] = sv2v_cast_6D350(6'd23);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd41);
							r[12-:6] = sv2v_cast_6D350(6'd47);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd42);
							r[12-:6] = sv2v_cast_6D350(6'd48);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100001111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd43);
							r[12-:6] = sv2v_cast_6D350(6'd23);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100010000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd147);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100010001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd176);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0000000100010010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd182);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100010011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd189);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000000100010100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd207);
							r[12-:6] = sv2v_cast_6D350(6'd52);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00000001001zzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd183);
							r[12-:6] = sv2v_cast_6D350(6'd30);
						end
						16'b0000000101zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd22);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b000000011zzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd38);
							r[12-:6] = sv2v_cast_6D350(6'd36);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000001zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd3);
							r[12-:6] = sv2v_cast_6D350(6'd19);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0000010zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd25);
							r[12-:6] = sv2v_cast_6D350(6'd19);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00000110zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd30);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000111zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd31);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd5);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd25);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd25);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b001000zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd38);
							r[12-:6] = sv2v_cast_6D350(6'd40);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b001001zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd38);
							r[12-:6] = sv2v_cast_6D350(6'd40);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd39);
							r[12-:6] = sv2v_cast_6D350(6'd41);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b00110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd39);
							r[12-:6] = sv2v_cast_6D350(6'd41);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0011100zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd40);
							r[12-:6] = sv2v_cast_6D350(6'd21);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b0011101zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd40);
							r[12-:6] = sv2v_cast_6D350(6'd21);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b001111zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd41);
							r[12-:6] = sv2v_cast_6D350(6'd40);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b010000zzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd41);
							r[12-:6] = sv2v_cast_6D350(6'd40);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01000100zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd112);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000101zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd113);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000110zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd144);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000111zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd146);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd42);
							r[12-:6] = sv2v_cast_6D350(6'd41);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd42);
							r[12-:6] = sv2v_cast_6D350(6'd41);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b01011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd127);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd127);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd128);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd128);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd129);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd129);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd130);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd130);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd147);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b10100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd147);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b10101000zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd170);
							r[12-:6] = sv2v_cast_6D350(6'd37);
						end
						16'b10101001000zzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd183);
							r[12-:6] = sv2v_cast_6D350(6'd35);
						end
						16'b1010101zzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd182);
							r[12-:6] = sv2v_cast_6D350(6'd19);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b10110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd170);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b10111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd170);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b11000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd176);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd176);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd182);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b11011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd182);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b11100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd189);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b11101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd189);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b11110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd207);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						16'b11111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd207);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
							r[0] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd12):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000000zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd6);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000001zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd7);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000010zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd17);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000011zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd18);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000100zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd148);
							r[12-:6] = sv2v_cast_6D350(6'd20);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000101zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd157);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000110zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd158);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00000111zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd169);
							r[12-:6] = sv2v_cast_6D350(6'd37);
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd6);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd7);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd17);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd18);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd23);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd24);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd28);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd29);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd150);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd157);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd158);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd169);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b01101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd169);
							r[12-:6] = sv2v_cast_6D350(6'd42);
						end
						16'b01110000zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd172);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110001zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd173);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110010zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd174);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110011zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd180);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01110100zzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd181);
							r[12-:6] = sv2v_cast_6D350(6'd37);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd172);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd173);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd174);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd180);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd181);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd13):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd6);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd7);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd17);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd18);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd14):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd157);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd158);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd172);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd173);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd15):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd180);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd181);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd174);
							r[12-:6] = sv2v_cast_6D350(6'd45);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd16):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd9);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd10);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd11);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd12);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd17):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd13);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd14);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd15);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd16);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd18):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd126);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd138);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd19):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b00000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd20);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd20);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd21);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd21);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b0010000000000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd32);
							r[12-:6] = sv2v_cast_6D350(6'd57);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd34);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd34);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b00111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd35);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b01zzzzzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd33);
							r[12-:6] = sv2v_cast_6D350(6'd56);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd35);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd131);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd131);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd132);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd132);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd139);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd139);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b10111zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd140);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11000zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd140);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11001zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd141);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11010zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd141);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11011zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd142);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11100zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd142);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11101zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd143);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						16'b11110zzzzzzzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd143);
							r[12-:6] = sv2v_cast_6D350(6'd42);
							r[2] = 1'b1;
							r[1] = 1'b1;
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd20):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000000zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd159);
							r[12-:6] = sv2v_cast_6D350(6'd17);
						end
						16'b0000000000001zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd198);
							r[12-:6] = sv2v_cast_6D350(6'd17);
						end
						16'b0000000000010zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd160);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000011zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd199);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000100zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd165);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000101zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd202);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000110000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd4);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd119);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd145);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110011: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd166);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110100: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd171);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110101: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd187);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110110: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd188);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000110111: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd195);
							r[12-:6] = sv2v_cast_6D350(6'd0);
							r[1] = 1'b1;
						end
						16'b0000000000111zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd27);
							r[12-:6] = sv2v_cast_6D350(6'd4);
							r[1] = 1'b1;
						end
						16'b0000000001zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd164);
							r[12-:6] = sv2v_cast_6D350(6'd27);
						end
						16'b0000000010zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd201);
							r[12-:6] = sv2v_cast_6D350(6'd16);
						end
						16'b0000000011zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd175);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000100zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd167);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000101000zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd161);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000101001zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd162);
							r[12-:6] = sv2v_cast_6D350(6'd18);
						end
						16'b0000000101010000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd196);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000101010001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd208);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000101011zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd200);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd21):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000000000: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd118);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000000001: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd114);
							r[12-:6] = sv2v_cast_6D350(6'd9);
						end
						16'b0000000000000010: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd8);
							r[12-:6] = sv2v_cast_6D350(6'd0);
						end
						16'b0000000000001zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd184);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000000010zzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd163);
							r[12-:6] = sv2v_cast_6D350(6'd4);
						end
						16'b0000000001zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd117);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000010zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd185);
							r[12-:6] = sv2v_cast_6D350(6'd14);
						end
						16'b0000000011zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd115);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000100zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd197);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000101zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd80);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000110zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd116);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000000111zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd186);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000001000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd153);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000001001zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd154);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						16'b0000001010zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd194);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						default:
							;
					endcase
				sv2v_cast_7D91B(5'd22):
					(* full_case, parallel_case *)
					casez (extension_word)
						16'b0000000000zzzzzz: begin
							r[21] = 1'b1;
							r[20-:8] = sv2v_cast_BD1B7(8'd37);
							r[12-:6] = sv2v_cast_6D350(6'd5);
						end
						default:
							;
					endcase
				default:
					;
			endcase
			bedrock_decode_pkg_bedrock_decode_extended_opcode = r;
		end
	endfunction
	function automatic [3:0] bedrock_decode_pkg_bedrock_decode_field_format_token_words;
		input reg [5:0] field_format_id;
		reg [3:0] r;
		begin
			r = 4'd1;
			(* full_case, parallel_case *)
			case (field_format_id)
				sv2v_cast_6D350(6'd2): r = 4'd2;
				sv2v_cast_6D350(6'd4): r = 4'd2;
				sv2v_cast_6D350(6'd5): r = 4'd2;
				sv2v_cast_6D350(6'd6): r = 4'd2;
				sv2v_cast_6D350(6'd9): r = 4'd3;
				sv2v_cast_6D350(6'd10): r = 4'd3;
				sv2v_cast_6D350(6'd14): r = 4'd2;
				sv2v_cast_6D350(6'd15): r = 4'd2;
				sv2v_cast_6D350(6'd16): r = 4'd2;
				sv2v_cast_6D350(6'd17): r = 4'd3;
				sv2v_cast_6D350(6'd18): r = 4'd3;
				sv2v_cast_6D350(6'd19): r = 4'd2;
				sv2v_cast_6D350(6'd20): r = 4'd2;
				sv2v_cast_6D350(6'd21): r = 4'd2;
				sv2v_cast_6D350(6'd22): r = 4'd2;
				sv2v_cast_6D350(6'd23): r = 4'd3;
				sv2v_cast_6D350(6'd24): r = 4'd2;
				sv2v_cast_6D350(6'd25): r = 4'd2;
				sv2v_cast_6D350(6'd26): r = 4'd3;
				sv2v_cast_6D350(6'd27): r = 4'd2;
				sv2v_cast_6D350(6'd28): r = 4'd2;
				sv2v_cast_6D350(6'd30): r = 4'd3;
				sv2v_cast_6D350(6'd31): r = 4'd3;
				sv2v_cast_6D350(6'd35): r = 4'd3;
				sv2v_cast_6D350(6'd36): r = 4'd2;
				sv2v_cast_6D350(6'd37): r = 4'd2;
				sv2v_cast_6D350(6'd38): r = 4'd2;
				sv2v_cast_6D350(6'd40): r = 4'd2;
				sv2v_cast_6D350(6'd41): r = 4'd2;
				sv2v_cast_6D350(6'd42): r = 4'd2;
				sv2v_cast_6D350(6'd43): r = 4'd2;
				sv2v_cast_6D350(6'd44): r = 4'd2;
				sv2v_cast_6D350(6'd45): r = 4'd2;
				sv2v_cast_6D350(6'd46): r = 4'd3;
				sv2v_cast_6D350(6'd47): r = 4'd3;
				sv2v_cast_6D350(6'd48): r = 4'd3;
				sv2v_cast_6D350(6'd49): r = 4'd3;
				sv2v_cast_6D350(6'd50): r = 4'd3;
				sv2v_cast_6D350(6'd51): r = 4'd2;
				sv2v_cast_6D350(6'd52): r = 4'd3;
				sv2v_cast_6D350(6'd53): r = 4'd2;
				sv2v_cast_6D350(6'd54): r = 4'd2;
				sv2v_cast_6D350(6'd55): r = 4'd2;
				sv2v_cast_6D350(6'd56): r = 4'd2;
				sv2v_cast_6D350(6'd57): r = 4'd3;
				sv2v_cast_6D350(6'd58): r = 4'd3;
				sv2v_cast_6D350(6'd59): r = 4'd3;
				sv2v_cast_6D350(6'd60): r = 4'd2;
				sv2v_cast_6D350(6'd61): r = 4'd2;
				sv2v_cast_6D350(6'd62): r = 4'd3;
				sv2v_cast_6D350(6'd63): r = 4'd3;
				default:
					;
			endcase
			bedrock_decode_pkg_bedrock_decode_field_format_token_words = r;
		end
	endfunction
	function automatic [27:0] bedrock_decode_pkg_bedrock_decode_primary_payload;
		input reg [11:0] payload;
		reg [27:0] r;
		begin
			r = 1'sb0;
			r[25-:8] = sv2v_cast_BD1B7(8'd0);
			r[17-:6] = sv2v_cast_6D350(6'd0);
			r[11-:4] = 4'd1;
			r[7-:5] = sv2v_cast_7D91B(5'd0);
			(* full_case *)
			casez (payload)
				12'b000000000000: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd110);
					r[17-:6] = sv2v_cast_6D350(6'd0);
				end
				12'b000000000001: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd19);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd3;
				end
				12'b000000000010: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd19);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd5;
				end
				12'b000000000011: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd168);
					r[17-:6] = sv2v_cast_6D350(6'd0);
				end
				12'b000000000100: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd156);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b000000000101: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd151);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b000000000110: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd135);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b000000000111: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd136);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b000000001zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd155);
					r[17-:6] = sv2v_cast_6D350(6'd3);
				end
				12'b00000001zzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd5);
					r[17-:6] = sv2v_cast_6D350(6'd13);
					r[11-:4] = 4'd2;
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b0000001zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd30);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b000001zzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd40);
					r[17-:6] = sv2v_cast_6D350(6'd12);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b00001zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd3);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b00010zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd39);
					r[17-:6] = sv2v_cast_6D350(6'd33);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b000110zzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd39);
					r[17-:6] = sv2v_cast_6D350(6'd33);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b0001110zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd112);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b0001111zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd1);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b00100zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd42);
					r[17-:6] = sv2v_cast_6D350(6'd33);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b001010zzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd42);
					r[17-:6] = sv2v_cast_6D350(6'd33);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b0010110zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd31);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b0010111zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd113);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b00110zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd5);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b00111zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd25);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b01zzzzzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd133);
					r[17-:6] = sv2v_cast_6D350(6'd39);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b10zzzzzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd133);
					r[17-:6] = sv2v_cast_6D350(6'd39);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11000zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd147);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11001zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd182);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11010zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd189);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11011zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd207);
					r[17-:6] = sv2v_cast_6D350(6'd34);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11100zzzzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd41);
					r[17-:6] = sv2v_cast_6D350(6'd32);
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b1110100zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd144);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b1110101zzzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd146);
					r[17-:6] = sv2v_cast_6D350(6'd11);
					r[2] = 1'b1;
					r[1] = 1'b1;
				end
				12'b111011000000: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd121);
					r[17-:6] = sv2v_cast_6D350(6'd7);
					r[11-:4] = 4'd2;
				end
				12'b111011010000: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd121);
					r[17-:6] = sv2v_cast_6D350(6'd7);
					r[11-:4] = 4'd2;
				end
				12'b11101100001z: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b1110110001zz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b111011001zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b11101101001z: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b1110110101zz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b111011011zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd120);
					r[17-:6] = sv2v_cast_6D350(6'd29);
					r[11-:4] = 4'd2;
				end
				12'b111011000001: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd204);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b111011010001: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd205);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b11101110zzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd147);
					r[17-:6] = sv2v_cast_6D350(6'd13);
					r[11-:4] = 4'd2;
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b11101111zzzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd207);
					r[17-:6] = sv2v_cast_6D350(6'd13);
					r[11-:4] = 4'd2;
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b111100000zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd155);
					r[17-:6] = sv2v_cast_6D350(6'd1);
				end
				12'b111100001zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd149);
					r[17-:6] = sv2v_cast_6D350(6'd3);
				end
				12'b111100010zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd149);
					r[17-:6] = sv2v_cast_6D350(6'd1);
				end
				12'b111100011zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd22);
					r[17-:6] = sv2v_cast_6D350(6'd1);
				end
				12'b111100100zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd22);
					r[17-:6] = sv2v_cast_6D350(6'd3);
				end
				12'b111100101zzz: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd133);
					r[17-:6] = sv2v_cast_6D350(6'd1);
					r[11-:4] = 4'd5;
					r[2] = 1'b1;
					r[1] = 1'b1;
					r[0] = 1'b1;
				end
				12'b111100110000: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd191);
					r[17-:6] = sv2v_cast_6D350(6'd0);
					r[11-:4] = 4'd2;
				end
				12'b111111111111: begin
					r[27] = 1'b1;
					r[25-:8] = sv2v_cast_BD1B7(8'd111);
					r[17-:6] = sv2v_cast_6D350(6'd0);
				end
				12'b111101010000: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd1);
				end
				12'b111101010001: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd2);
				end
				12'b11110100zzzz: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd3);
				end
				12'b111100111101: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd4);
				end
				12'b111100111010: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd5);
				end
				12'b111100111011: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd6);
				end
				12'b111100111100: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd7);
				end
				12'b111101010110: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd8);
				end
				12'b111101010101: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd9);
				end
				12'b111101010111: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd10);
				end
				12'b111100110001: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd11);
				end
				12'b111100110110: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd12);
				end
				12'b111100110111: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd13);
				end
				12'b111100111000: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd14);
				end
				12'b111100111001: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd15);
				end
				12'b111100110010: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd16);
				end
				12'b111100110011: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd17);
				end
				12'b111100110101: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd18);
				end
				12'b111100110100: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd19);
				end
				12'b111101010011: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd20);
				end
				12'b111101010010: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd21);
				end
				12'b111101010100: begin
					r[27] = 1'b1;
					r[26] = 1'b1;
					r[7-:5] = sv2v_cast_7D91B(5'd22);
				end
				default:
					;
			endcase
			bedrock_decode_pkg_bedrock_decode_primary_payload = r;
		end
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		primary_decode = bedrock_decode_pkg_bedrock_decode_primary_payload(primary_payload_i);
		extended_decode = 1'sb0;
		extended_decode[20-:8] = sv2v_cast_BD1B7(8'd0);
		extended_decode[12-:6] = sv2v_cast_6D350(6'd0);
		field_format_token_words = 4'd1;
		valid_o = primary_decode[27];
		needs_extension_o = primary_decode[26];
		opcode_id_o = primary_decode[25-:8];
		field_format_id_o = primary_decode[17-:6];
		required_words_o = primary_decode[11-:4];
		ext_root_o = primary_decode[7-:5];
		repcc_allowed = primary_decode[2];
		repg_allowed = primary_decode[1];
		repg_fast_candidate = primary_decode[0];
		if (primary_decode[26]) begin
			extended_decode = bedrock_decode_pkg_bedrock_decode_extended_opcode(primary_decode[7-:5], extension_word_i);
			valid_o = extended_decode[21];
			opcode_id_o = extended_decode[20-:8];
			field_format_id_o = extended_decode[12-:6];
			required_words_o = extended_decode[6-:4];
			repcc_allowed = extended_decode[2];
			repg_allowed = extended_decode[1];
			repg_fast_candidate = extended_decode[0];
		end
		if (valid_o) begin
			field_format_token_words = bedrock_decode_pkg_bedrock_decode_field_format_token_words(field_format_id_o);
			if (field_format_token_words > required_words_o)
				required_words_o = field_format_token_words;
		end
		repcc_allowed_o = valid_o && repcc_allowed;
		repg_allowed_o = valid_o && repg_allowed;
		repg_fast_candidate_o = valid_o && repg_fast_candidate;
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module bedrock_prefix_decode (
	prefix_word_i,
	valid_o,
	nospec_o,
	saturate_o,
	nontemporal_o,
	update_mode_o,
	access_mode_o,
	repeat_kind_o,
	repeat_condition_o,
	repeat_counter_o,
	end_group_o
);
	reg _sv2v_0;
	input wire [15:0] prefix_word_i;
	output reg valid_o;
	output reg nospec_o;
	output reg saturate_o;
	output reg nontemporal_o;
	output reg [2:0] update_mode_o;
	output reg [1:0] access_mode_o;
	output reg [1:0] repeat_kind_o;
	output reg [3:0] repeat_condition_o;
	output reg [2:0] repeat_counter_o;
	output reg end_group_o;
	reg [42:0] decode;
	function automatic [42:0] bedrock_prefix_decode_pkg_bedrock_apply_prefix_byte;
		input reg [42:0] state;
		input reg [11:0] prefix;
		reg [42:0] r;
		begin
			r = state;
			r[42] = r[42] && prefix[11];
			(* full_case, parallel_case *)
			case (prefix[10-:4])
				4'd1:
					;
				4'd2: r[17] = 1'b1;
				4'd3: r[16] = 1'b1;
				4'd4: r[15] = 1'b1;
				4'd5: r[14-:3] = 3'd1;
				4'd6: r[14-:3] = 3'd2;
				4'd7: r[14-:3] = 3'd3;
				4'd8: r[14-:3] = 3'd4;
				4'd9: r[11-:2] = 2'd1;
				4'd10: r[11-:2] = 2'd2;
				4'd11: r[11-:2] = 2'd3;
				4'd12: r[0] = 1'b1;
				4'd13: begin
					r[9-:2] = 2'd1;
					r[7-:4] = prefix[6-:4];
					r[3-:3] = prefix[2-:3];
				end
				4'd14: begin
					r[9-:2] = 2'd2;
					r[7-:4] = prefix[6-:4];
					r[3-:3] = prefix[2-:3];
				end
				default:
					;
			endcase
			bedrock_prefix_decode_pkg_bedrock_apply_prefix_byte = r;
		end
	endfunction
	function automatic [11:0] bedrock_prefix_decode_pkg_bedrock_decode_prefix_byte;
		input reg [7:0] prefix_byte;
		reg [11:0] r;
		begin
			r = 1'sb0;
			(* full_case, parallel_case *)
			casez (prefix_byte)
				8'h00: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd1;
				end
				8'h01: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd2;
				end
				8'h02: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd3;
				end
				8'h03: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd4;
				end
				8'h04: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd5;
				end
				8'h05: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd6;
				end
				8'h06: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd7;
				end
				8'h07: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd8;
				end
				8'h08: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd9;
				end
				8'h09: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd10;
				end
				8'h0a: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd11;
				end
				8'h78: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd12;
				end
				8'b1zzzzzzz: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd13;
					r[6-:4] = prefix_byte[6:3];
					r[2-:3] = prefix_byte[2:0];
				end
				8'b01110zzz: begin
					r[11] = 1'b1;
					r[10-:4] = 4'd14;
					r[2-:3] = prefix_byte[2:0];
				end
				default: r[10-:4] = 4'd0;
			endcase
			bedrock_prefix_decode_pkg_bedrock_decode_prefix_byte = r;
		end
	endfunction
	function automatic [42:0] bedrock_prefix_decode_pkg_bedrock_decode_prefix_word;
		input reg [15:0] prefix_word;
		reg [42:0] r;
		begin
			r = 1'sb0;
			r[42] = 1'b1;
			r[41-:12] = bedrock_prefix_decode_pkg_bedrock_decode_prefix_byte(prefix_word[7:0]);
			r[29-:12] = bedrock_prefix_decode_pkg_bedrock_decode_prefix_byte(prefix_word[15:8]);
			r = bedrock_prefix_decode_pkg_bedrock_apply_prefix_byte(r, r[41-:12]);
			r = bedrock_prefix_decode_pkg_bedrock_apply_prefix_byte(r, r[29-:12]);
			bedrock_prefix_decode_pkg_bedrock_decode_prefix_word = r;
		end
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		decode = bedrock_prefix_decode_pkg_bedrock_decode_prefix_word(prefix_word_i);
		valid_o = decode[42];
		nospec_o = decode[17];
		saturate_o = decode[16];
		nontemporal_o = decode[15];
		update_mode_o = decode[14-:3];
		access_mode_o = decode[11-:2];
		repeat_kind_o = decode[9-:2];
		repeat_condition_o = decode[7-:4];
		repeat_counter_o = decode[3-:3];
		end_group_o = decode[0];
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module bedrock_ea_decode (
	ea_i,
	descriptor_i,
	valid_o,
	reserved_o,
	needs_descriptor_o,
	form_o,
	is_register_o,
	is_memory_o,
	is_immediate_o,
	update_eligible_o,
	signed32_index_escape_o,
	segment_selectable_o,
	segment_valid_o,
	has_base_reg_o,
	has_index_reg_o,
	has_displacement_o,
	has_absolute_o,
	segment_o,
	base_o,
	base_reg_o,
	index_reg_o,
	scale_log2_o,
	displacement_words_o,
	payload_words_o
);
	reg _sv2v_0;
	input wire [5:0] ea_i;
	input wire [15:0] descriptor_i;
	output reg valid_o;
	output reg reserved_o;
	output reg needs_descriptor_o;
	output reg [5:0] form_o;
	output reg is_register_o;
	output reg is_memory_o;
	output reg is_immediate_o;
	output reg update_eligible_o;
	output reg signed32_index_escape_o;
	output reg segment_selectable_o;
	output reg segment_valid_o;
	output reg has_base_reg_o;
	output reg has_index_reg_o;
	output reg has_displacement_o;
	output reg has_absolute_o;
	output reg [2:0] segment_o;
	output reg [2:0] base_o;
	output reg [2:0] base_reg_o;
	output reg [2:0] index_reg_o;
	output reg [1:0] scale_log2_o;
	output reg [2:0] displacement_words_o;
	output reg [2:0] payload_words_o;
	reg [39:0] decode;
	function automatic [39:0] bedrock_ea_decode_pkg_bedrock_decode_compact_ea;
		input reg [5:0] ea;
		reg [39:0] r;
		begin
			r = 1'sb0;
			r[24] = 1'b1;
			(* full_case, parallel_case *)
			casez (ea)
				6'b000zzz: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd1;
					r[29] = 1'b1;
					r[28] = 1'b0;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd1;
					r[17] = 1'b1;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
					r[15-:3] = ea[2:0];
				end
				6'b001zzz: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd2;
					r[29] = 1'b1;
					r[28] = 1'b0;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd2;
					r[17] = 1'b1;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
					r[15-:3] = ea[2:0];
				end
				6'b010zzz: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd3;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b1;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd2;
					r[17] = 1'b1;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
					r[15-:3] = ea[2:0];
				end
				6'b011zzz: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd4;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd2;
					r[17] = 1'b1;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd1;
					r[2-:3] = 3'd1;
					r[15-:3] = ea[2:0];
				end
				6'b100zzz: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd5;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd2;
					r[17] = 1'b1;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd2;
					r[2-:3] = 3'd2;
					r[15-:3] = ea[2:0];
				end
				6'b101000: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd6;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd0;
					r[20-:3] = 3'd3;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd1;
					r[2-:3] = 3'd1;
				end
				6'b101001: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd7;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd0;
					r[20-:3] = 3'd3;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd2;
					r[2-:3] = 3'd2;
				end
				6'b101010: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd8;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd0;
					r[20-:3] = 3'd3;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd4;
					r[2-:3] = 3'd4;
				end
				6'b101100: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd9;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd7;
					r[20-:3] = 3'd4;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd1;
					r[2-:3] = 3'd1;
				end
				6'b101101: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd10;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd7;
					r[20-:3] = 3'd4;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd2;
					r[2-:3] = 3'd2;
				end
				6'b101110: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd11;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd7;
					r[20-:3] = 3'd4;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b1;
					r[6] = 1'b0;
					r[5-:3] = 3'd4;
					r[2-:3] = 3'd4;
				end
				6'b101111: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd12;
					r[29] = 1'b1;
					r[28] = 1'b0;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd4;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
				end
				6'b110000: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd13;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd5;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b1;
					r[5-:3] = 3'd2;
					r[2-:3] = 3'd2;
				end
				6'b110001: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd14;
					r[29] = 1'b0;
					r[28] = 1'b1;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd5;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b1;
					r[5-:3] = 3'd4;
					r[2-:3] = 3'd4;
				end
				6'b110010: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd15;
					r[29] = 1'b0;
					r[28] = 1'b0;
					r[27] = 1'b1;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd6;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd1;
					r[2-:3] = 3'd1;
				end
				6'b110011: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd16;
					r[29] = 1'b0;
					r[28] = 1'b0;
					r[27] = 1'b1;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd6;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd2;
					r[2-:3] = 3'd2;
				end
				6'b110100: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd17;
					r[29] = 1'b0;
					r[28] = 1'b0;
					r[27] = 1'b1;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd6;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd4;
					r[2-:3] = 3'd4;
				end
				6'b111110: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd18;
					r[29] = 1'b0;
					r[28] = 1'b0;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd0;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
					r[37] = 1'b1;
					r[36] = 1'b1;
					r[2-:3] = 3'd1;
				end
				6'b111111: begin
					r[39] = 1'b1;
					r[35-:6] = 6'd19;
					r[29] = 1'b0;
					r[28] = 1'b0;
					r[27] = 1'b0;
					r[26] = 1'b0;
					r[25] = 1'b0;
					r[23-:3] = 3'd1;
					r[20-:3] = 3'd0;
					r[17] = 1'b0;
					r[16] = 1'b0;
					r[7] = 1'b0;
					r[6] = 1'b0;
					r[5-:3] = 3'd0;
					r[2-:3] = 3'd0;
					r[37] = 1'b1;
					r[2-:3] = 3'd1;
				end
				6'b101011: r[38] = 1'b1;
				6'b110101: r[38] = 1'b1;
				6'b110110: r[38] = 1'b1;
				6'b110111: r[38] = 1'b1;
				6'b111000: r[38] = 1'b1;
				6'b111001: r[38] = 1'b1;
				6'b111010: r[38] = 1'b1;
				6'b111011: r[38] = 1'b1;
				6'b111100: r[38] = 1'b1;
				6'b111101: r[38] = 1'b1;
				default: r[38] = 1'b1;
			endcase
			bedrock_ea_decode_pkg_bedrock_decode_compact_ea = r;
		end
	endfunction
	function automatic [2:0] bedrock_ea_decode_pkg_bedrock_ea_segment_decode;
		input reg [2:0] segment;
		(* full_case, parallel_case *)
		case (segment)
			3'd0: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd0;
			3'd1: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd1;
			3'd3: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd2;
			3'd4: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd3;
			3'd5: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd4;
			3'd6: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd5;
			3'd7: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd6;
			3'd2: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd7;
			default: bedrock_ea_decode_pkg_bedrock_ea_segment_decode = 3'd7;
		endcase
	endfunction
	function automatic [39:0] bedrock_ea_decode_pkg_bedrock_decode_extended_ea;
		input reg signed32_index_escape;
		input reg [15:0] descriptor;
		reg [39:0] r;
		reg [4:0] mode;
		reg [2:0] segment;
		reg [7:0] extra;
		begin
			r = 1'sb0;
			r[36] = signed32_index_escape;
			mode = descriptor[15:11];
			segment = descriptor[10:8];
			extra = descriptor[7:0];
			r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
			r[24] = 1'b1;
			(* full_case, parallel_case *)
			case (mode)
				5'h00:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd20;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b0;
						r[6] = 1'b0;
						r[5-:3] = 3'd0;
						r[2-:3] = 3'd1;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd35;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b0;
						r[6] = 1'b0;
						r[5-:3] = 3'd0;
						r[2-:3] = 3'd1;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h01:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd21;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd36;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h02:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd22;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd37;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h03:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd23;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd38;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[15-:3] = extra[7:5];
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h04:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd24;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b1;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b0;
						r[7] = 1'b0;
						r[6] = 1'b0;
						r[5-:3] = 3'd0;
						r[2-:3] = 3'd1;
						r[15-:3] = extra[7:5];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h05:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd25;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b0;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[15-:3] = extra[7:5];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h06:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd26;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd2;
						r[17] = 1'b1;
						r[16] = 1'b0;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[15-:3] = extra[7:5];
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h07:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd27;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd5;
						r[17] = 1'b0;
						r[16] = 1'b0;
						r[7] = 1'b0;
						r[6] = 1'b1;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h08:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd28;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b1;
						r[23-:3] = 3'd1;
						r[20-:3] = 3'd5;
						r[17] = 1'b0;
						r[16] = 1'b0;
						r[7] = 1'b0;
						r[6] = 1'b1;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[23-:3] = bedrock_ea_decode_pkg_bedrock_ea_segment_decode(segment);
						r[24] = 1'b1;
					end
					else
						r[38] = 1'b1;
				5'h09:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd29;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd39;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else
						r[38] = 1'b1;
				5'h0a:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd30;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd40;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else
						r[38] = 1'b1;
				5'h0b:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd31;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd41;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd7;
						r[20-:3] = 3'd4;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd7;
					end
					else
						r[38] = 1'b1;
				5'h0c:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd32;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd42;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd1;
						r[2-:3] = 3'd2;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else
						r[38] = 1'b1;
				5'h0d:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd33;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd43;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd2;
						r[2-:3] = 3'd3;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else
						r[38] = 1'b1;
				5'h0e:
					if (!signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd34;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else if (signed32_index_escape) begin
						r[39] = 1'b1;
						r[35-:6] = 6'd44;
						r[29] = 1'b0;
						r[28] = 1'b1;
						r[27] = 1'b0;
						r[26] = 1'b0;
						r[25] = 1'b0;
						r[23-:3] = 3'd0;
						r[20-:3] = 3'd3;
						r[17] = 1'b0;
						r[16] = 1'b1;
						r[7] = 1'b1;
						r[6] = 1'b0;
						r[5-:3] = 3'd4;
						r[2-:3] = 3'd5;
						r[12-:3] = extra[4:2];
						r[9-:2] = extra[1:0];
						r[36] = 1'b1;
						r[24] = segment == 3'd0;
						r[23-:3] = 3'd0;
					end
					else
						r[38] = 1'b1;
				default: r[38] = 1'b1;
			endcase
			r[39] = r[39] && r[24];
			bedrock_ea_decode_pkg_bedrock_decode_extended_ea = r;
		end
	endfunction
	function automatic [39:0] bedrock_ea_decode_pkg_bedrock_decode_ea;
		input reg [5:0] ea;
		input reg [15:0] descriptor;
		reg [39:0] compact;
		reg [0:1] _sv2v_jump;
		begin
			_sv2v_jump = 2'b00;
			compact = bedrock_ea_decode_pkg_bedrock_decode_compact_ea(ea);
			if (compact[37]) begin
				bedrock_ea_decode_pkg_bedrock_decode_ea = bedrock_ea_decode_pkg_bedrock_decode_extended_ea(compact[36], descriptor);
				_sv2v_jump = 2'b11;
			end
			if (_sv2v_jump == 2'b00) begin
				bedrock_ea_decode_pkg_bedrock_decode_ea = compact;
				_sv2v_jump = 2'b11;
			end
		end
	endfunction
	always @(*) begin
		if (_sv2v_0)
			;
		decode = bedrock_ea_decode_pkg_bedrock_decode_ea(ea_i, descriptor_i);
		valid_o = decode[39];
		reserved_o = decode[38];
		needs_descriptor_o = decode[37];
		form_o = decode[35-:6];
		is_register_o = decode[29];
		is_memory_o = decode[28];
		is_immediate_o = decode[27];
		update_eligible_o = decode[26];
		signed32_index_escape_o = decode[36];
		segment_selectable_o = decode[25];
		segment_valid_o = decode[24];
		has_base_reg_o = decode[17];
		has_index_reg_o = decode[16];
		has_displacement_o = decode[7];
		has_absolute_o = decode[6];
		segment_o = decode[23-:3];
		base_o = decode[20-:3];
		base_reg_o = decode[15-:3];
		index_reg_o = decode[12-:3];
		scale_log2_o = decode[9-:2];
		displacement_words_o = decode[5-:3];
		payload_words_o = decode[2-:3];
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module bedrock_agu_request_build (
	ea_present_i,
	ea_value_i,
	descriptor_token_i,
	ea_valid_i,
	ea_reserved_i,
	ea_needs_descriptor_i,
	ea_form_i,
	ea_is_register_i,
	ea_is_memory_i,
	ea_is_immediate_i,
	ea_update_eligible_i,
	ea_signed32_index_escape_i,
	ea_segment_selectable_i,
	ea_segment_valid_i,
	ea_has_base_reg_i,
	ea_has_index_reg_i,
	ea_has_displacement_i,
	ea_has_absolute_i,
	ea_segment_i,
	ea_base_i,
	ea_base_reg_i,
	ea_index_reg_i,
	ea_scale_log2_i,
	ea_displacement_words_i,
	ea_payload_words_i,
	update_mode_i,
	request_o
);
	reg _sv2v_0;
	input wire ea_present_i;
	input wire [5:0] ea_value_i;
	input wire [3:0] descriptor_token_i;
	input wire ea_valid_i;
	input wire ea_reserved_i;
	input wire ea_needs_descriptor_i;
	input wire [5:0] ea_form_i;
	input wire ea_is_register_i;
	input wire ea_is_memory_i;
	input wire ea_is_immediate_i;
	input wire ea_update_eligible_i;
	input wire ea_signed32_index_escape_i;
	input wire ea_segment_selectable_i;
	input wire ea_segment_valid_i;
	input wire ea_has_base_reg_i;
	input wire ea_has_index_reg_i;
	input wire ea_has_displacement_i;
	input wire ea_has_absolute_i;
	input wire [2:0] ea_segment_i;
	input wire [2:0] ea_base_i;
	input wire [2:0] ea_base_reg_i;
	input wire [2:0] ea_index_reg_i;
	input wire [1:0] ea_scale_log2_i;
	input wire [2:0] ea_displacement_words_i;
	input wire [2:0] ea_payload_words_i;
	input wire [2:0] update_mode_i;
	output reg [61:0] request_o;
	reg update_requested;
	always @(*) begin
		if (_sv2v_0)
			;
		update_requested = update_mode_i != 3'd0;
		request_o = 1'sb0;
		request_o[60] = ea_present_i;
		request_o[59] = ea_valid_i;
		request_o[58] = ea_reserved_i;
		request_o[61] = (ea_present_i && ea_valid_i) && !ea_reserved_i;
		request_o[57] = ea_is_register_i;
		request_o[56] = ea_is_memory_i;
		request_o[55] = ea_is_immediate_i;
		request_o[54] = ea_needs_descriptor_i;
		request_o[53] = ea_signed32_index_escape_i;
		request_o[52] = ea_segment_selectable_i;
		request_o[51] = ea_segment_valid_i;
		request_o[50] = ea_update_eligible_i;
		request_o[49] = ea_present_i && update_requested;
		request_o[48] = !request_o[49] || ea_update_eligible_i;
		request_o[47] = request_o[49] && !ea_update_eligible_i;
		request_o[46] = ea_has_base_reg_i;
		request_o[45] = ea_has_index_reg_i;
		request_o[44] = ea_has_displacement_i;
		request_o[43] = ea_has_absolute_i;
		request_o[42-:6] = ea_value_i;
		request_o[36-:4] = descriptor_token_i;
		request_o[32-:4] = descriptor_token_i + (ea_needs_descriptor_i ? 4'd1 : 4'd0);
		request_o[28-:3] = ea_payload_words_i;
		request_o[25-:3] = ea_displacement_words_i;
		request_o[22-:3] = update_mode_i;
		request_o[19-:6] = ea_form_i;
		request_o[13-:3] = ea_segment_i;
		request_o[10-:3] = ea_base_i;
		request_o[7-:3] = ea_base_reg_i;
		request_o[4-:3] = ea_index_reg_i;
		request_o[1-:2] = ea_scale_log2_i;
	end
	initial _sv2v_0 = 0;
endmodule
`default_nettype wire
`default_nettype none
module bedrock_full_decode (
	words_i,
	valid_o,
	prefix_present_o,
	prefix_valid_o,
	decode_valid_o,
	undersized_o,
	length_words_o,
	required_words_o,
	opcode_id_o,
	field_format_id_o,
	ext_root_o,
	needs_extension_o,
	nospec_o,
	saturate_o,
	nontemporal_o,
	update_mode_o,
	access_mode_o,
	repeat_kind_o,
	repeat_condition_o,
	repeat_counter_o,
	end_group_o,
	repcc_allowed_o,
	repg_allowed_o,
	repg_fast_candidate_o,
	repcc_valid_o,
	repg_valid_o,
	repeat_present_o,
	repeat_valid_o,
	repeat_invalid_o,
	ea_present_o,
	ea_value_o,
	ea_descriptor_token_o,
	ea_valid_o,
	ea_reserved_o,
	ea_needs_descriptor_o,
	ea_form_o,
	ea_is_register_o,
	ea_is_memory_o,
	ea_is_immediate_o,
	ea_update_eligible_o,
	ea_segment_o,
	ea_base_o,
	ea_base_reg_o,
	ea_index_reg_o,
	ea_scale_log2_o,
	ea_payload_words_o,
	agu_request_o
);
	localparam signed [31:0] bedrock_pkg_MAX_INSTRUCTION_WORDS = 8;
	localparam signed [31:0] bedrock_pkg_WORD_BITS = 16;
	input wire [(bedrock_pkg_MAX_INSTRUCTION_WORDS * bedrock_pkg_WORD_BITS) - 1:0] words_i;
	output wire valid_o;
	output wire prefix_present_o;
	output wire prefix_valid_o;
	output wire decode_valid_o;
	output wire undersized_o;
	output wire [3:0] length_words_o;
	output wire [3:0] required_words_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_OPCODE_ID_BITS = 8;
	output wire [7:0] opcode_id_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_FIELD_FORMAT_ID_BITS = 6;
	output wire [5:0] field_format_id_o;
	localparam signed [31:0] bedrock_decode_pkg_BEDROCK_DECODE_EXT_ROOT_BITS = 5;
	output wire [4:0] ext_root_o;
	output wire needs_extension_o;
	output wire nospec_o;
	output wire saturate_o;
	output wire nontemporal_o;
	output wire [2:0] update_mode_o;
	output wire [1:0] access_mode_o;
	output wire [1:0] repeat_kind_o;
	output wire [3:0] repeat_condition_o;
	output wire [2:0] repeat_counter_o;
	output wire end_group_o;
	output wire repcc_allowed_o;
	output wire repg_allowed_o;
	output wire repg_fast_candidate_o;
	output wire repcc_valid_o;
	output wire repg_valid_o;
	output wire repeat_present_o;
	output wire repeat_valid_o;
	output wire repeat_invalid_o;
	output wire [1:0] ea_present_o;
	output wire [11:0] ea_value_o;
	output wire [7:0] ea_descriptor_token_o;
	output wire [0:1] ea_valid_o;
	output wire [0:1] ea_reserved_o;
	output wire [0:1] ea_needs_descriptor_o;
	output wire [11:0] ea_form_o;
	output wire [0:1] ea_is_register_o;
	output wire [0:1] ea_is_memory_o;
	output wire [0:1] ea_is_immediate_o;
	output wire [0:1] ea_update_eligible_o;
	output wire [5:0] ea_segment_o;
	output wire [5:0] ea_base_o;
	output wire [5:0] ea_base_reg_o;
	output wire [5:0] ea_index_reg_o;
	output wire [3:0] ea_scale_log2_o;
	output wire [5:0] ea_payload_words_o;
	output wire [123:0] agu_request_o;
	wire [15:0] word0;
	localparam signed [31:0] bedrock_pkg_PRIMARY_PAYLOAD_BITS = 12;
	wire [11:0] primary_payload;
	wire [15:0] prefix_word;
	wire [15:0] extension_word;
	wire [15:0] token0_word;
	wire [15:0] token1_word;
	wire [15:0] token2_word;
	wire [15:0] token3_word;
	wire [15:0] token4_word;
	wire [15:0] token5_word;
	wire [15:0] token6_word;
	wire [15:0] token7_word;
	wire prefix_decode_valid;
	wire instruction_decode_valid;
	wire [3:0] decode_required_words;
	wire [3:0] field_token_words;
	wire [3:0] dynamic_required_words;
	wire [3:0] total_required_words;
	wire [3:0] ea_payload_words_sum;
	wire all_ea_valid;
	wire base_valid;
	wire [3:0] ea0_descriptor_token;
	wire [3:0] ea1_descriptor_token;
	wire [15:0] ea0_descriptor_word;
	wire [15:0] ea1_descriptor_word;
	wire ea_signed32_index_escape [0:1];
	wire ea_segment_selectable [0:1];
	wire ea_segment_valid [0:1];
	wire ea_has_base_reg [0:1];
	wire ea_has_index_reg [0:1];
	wire ea_has_displacement [0:1];
	wire ea_has_absolute [0:1];
	wire [2:0] ea_displacement_words [0:1];
	wire [2:0] ea0_payload_words;
	wire [2:0] ea1_payload_words;
	wire [33:0] field_extract;
	function automatic [15:0] sv2v_cast_445EA;
		input reg [15:0] inp;
		sv2v_cast_445EA = inp;
	endfunction
	function automatic [15:0] physical_word_at;
		input reg [31:0] index;
		if (index < bedrock_pkg_MAX_INSTRUCTION_WORDS)
			physical_word_at = words_i[index * bedrock_pkg_WORD_BITS+:bedrock_pkg_WORD_BITS];
		else
			physical_word_at = sv2v_cast_445EA(16'h0000);
	endfunction
	assign word0 = physical_word_at(0);
	localparam signed [31:0] bedrock_pkg_WORD0_PREFIX_BIT = 15;
	function automatic bedrock_pkg_word0_prefix_present;
		input reg [15:0] word0;
		bedrock_pkg_word0_prefix_present = word0[bedrock_pkg_WORD0_PREFIX_BIT];
	endfunction
	assign prefix_present_o = bedrock_pkg_word0_prefix_present(word0);
	localparam signed [31:0] bedrock_pkg_WORD0_LENGTH_LSB = 12;
	localparam signed [31:0] bedrock_pkg_WORD0_LENGTH_MSB = 14;
	function automatic [2:0] bedrock_pkg_word0_length_field;
		input reg [15:0] word0;
		bedrock_pkg_word0_length_field = word0[bedrock_pkg_WORD0_LENGTH_MSB:bedrock_pkg_WORD0_LENGTH_LSB];
	endfunction
	function automatic [3:0] sv2v_cast_4;
		input reg [3:0] inp;
		sv2v_cast_4 = inp;
	endfunction
	function automatic [3:0] bedrock_pkg_word0_length_words;
		input reg [15:0] word0;
		bedrock_pkg_word0_length_words = sv2v_cast_4(bedrock_pkg_word0_length_field(word0)) + 4'd1;
	endfunction
	assign length_words_o = bedrock_pkg_word0_length_words(word0);
	localparam signed [31:0] bedrock_pkg_WORD0_PAYLOAD_LSB = 0;
	localparam signed [31:0] bedrock_pkg_WORD0_PAYLOAD_MSB = 11;
	function automatic [11:0] bedrock_pkg_word0_primary_payload;
		input reg [15:0] word0;
		bedrock_pkg_word0_primary_payload = word0[bedrock_pkg_WORD0_PAYLOAD_MSB:bedrock_pkg_WORD0_PAYLOAD_LSB];
	endfunction
	assign primary_payload = bedrock_pkg_word0_primary_payload(word0);
	assign prefix_word = (prefix_present_o ? physical_word_at(1) : sv2v_cast_445EA(16'h0000));
	assign token0_word = word0;
	assign token1_word = (prefix_present_o ? physical_word_at(2) : physical_word_at(1));
	assign token2_word = (prefix_present_o ? physical_word_at(3) : physical_word_at(2));
	assign token3_word = (prefix_present_o ? physical_word_at(4) : physical_word_at(3));
	assign token4_word = (prefix_present_o ? physical_word_at(5) : physical_word_at(4));
	assign token5_word = (prefix_present_o ? physical_word_at(6) : physical_word_at(5));
	assign token6_word = (prefix_present_o ? physical_word_at(7) : physical_word_at(6));
	assign token7_word = (prefix_present_o ? physical_word_at(8) : physical_word_at(7));
	assign extension_word = token1_word;
	bedrock_prefix_decode prefix_decode(
		.prefix_word_i(prefix_word),
		.valid_o(prefix_decode_valid),
		.nospec_o(nospec_o),
		.saturate_o(saturate_o),
		.nontemporal_o(nontemporal_o),
		.update_mode_o(update_mode_o),
		.access_mode_o(access_mode_o),
		.repeat_kind_o(repeat_kind_o),
		.repeat_condition_o(repeat_condition_o),
		.repeat_counter_o(repeat_counter_o),
		.end_group_o(end_group_o)
	);
	bedrock_decode decode(
		.primary_payload_i(primary_payload),
		.extension_word_i(extension_word),
		.valid_o(instruction_decode_valid),
		.needs_extension_o(needs_extension_o),
		.opcode_id_o(opcode_id_o),
		.field_format_id_o(field_format_id_o),
		.required_words_o(decode_required_words),
		.ext_root_o(ext_root_o),
		.repcc_allowed_o(repcc_allowed_o),
		.repg_allowed_o(repg_allowed_o),
		.repg_fast_candidate_o(repg_fast_candidate_o)
	);
	function automatic [5:0] sv2v_cast_6D350;
		input reg [5:0] inp;
		sv2v_cast_6D350 = inp;
	endfunction
	function automatic [33:0] bedrock_decode_pkg_bedrock_decode_extract_fields;
		input reg [5:0] field_format_id;
		input reg [15:0] token0_word;
		input reg [15:0] token1_word;
		input reg [15:0] token2_word;
		input reg [15:0] token3_word;
		input reg [15:0] token4_word;
		input reg [15:0] token5_word;
		input reg [15:0] token6_word;
		input reg [15:0] token7_word;
		reg [33:0] r;
		begin
			r = 1'sb0;
			r[33-:4] = 4'd1;
			r[15-:bedrock_pkg_WORD_BITS] = sv2v_cast_445EA(16'h0000);
			(* full_case, parallel_case *)
			case (field_format_id)
				sv2v_cast_6D350(6'd1): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd2): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd3): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd4): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd5): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd6): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd7): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd8): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd9): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd10): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd11): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd12): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd13): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd14): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd15): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd16): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd17): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd18): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd19): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd20): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd21): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd22): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd23): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
					r[29] = 1'b1;
					r[27:22] = token2_word[11:6];
				end
				sv2v_cast_6D350(6'd24): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd25): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd26): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd27): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd28): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[6:1];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd29): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd30): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd31): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd32): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd33): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd34): r[33-:4] = 4'd1;
				sv2v_cast_6D350(6'd35): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd36): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd37): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd38): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd39): begin
					r[33-:4] = 4'd1;
					r[28] = 1'b1;
					r[21:16] = token0_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token1_word;
				end
				sv2v_cast_6D350(6'd40): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd41): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd42): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd43): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
					r[29] = 1'b1;
					r[27:22] = token1_word[11:6];
				end
				sv2v_cast_6D350(6'd44): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd45): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd46): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				sv2v_cast_6D350(6'd47): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
					r[29] = 1'b1;
					r[27:22] = token2_word[11:6];
				end
				sv2v_cast_6D350(6'd48): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
					r[29] = 1'b1;
					r[27:22] = token2_word[11:6];
				end
				sv2v_cast_6D350(6'd49): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
					r[29] = 1'b1;
					r[27:22] = token2_word[11:6];
				end
				sv2v_cast_6D350(6'd50): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				sv2v_cast_6D350(6'd51): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd52): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
					r[29] = 1'b1;
					r[27:22] = token2_word[11:6];
				end
				sv2v_cast_6D350(6'd53): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd54): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd55): r[33-:4] = 4'd2;
				sv2v_cast_6D350(6'd56): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd57): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				sv2v_cast_6D350(6'd58): r[33-:4] = 4'd3;
				sv2v_cast_6D350(6'd59): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				sv2v_cast_6D350(6'd60): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd61): begin
					r[33-:4] = 4'd2;
					r[28] = 1'b1;
					r[21:16] = token1_word[5:0];
					r[15-:bedrock_pkg_WORD_BITS] = token2_word;
				end
				sv2v_cast_6D350(6'd62): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[8:3];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				sv2v_cast_6D350(6'd63): begin
					r[33-:4] = 4'd3;
					r[28] = 1'b1;
					r[21:16] = token2_word[8:3];
					r[15-:bedrock_pkg_WORD_BITS] = token3_word;
				end
				default:
					;
			endcase
			bedrock_decode_pkg_bedrock_decode_extract_fields = r;
		end
	endfunction
	assign field_extract = bedrock_decode_pkg_bedrock_decode_extract_fields(field_format_id_o, token0_word, token1_word, token2_word, token3_word, token4_word, token5_word, token6_word, token7_word);
	function automatic [15:0] bedrock_decode_pkg_bedrock_decode_ea1_descriptor_word;
		input reg [5:0] field_format_id;
		input reg [2:0] ea0_payload_words;
		input reg [15:0] token0_word;
		input reg [15:0] token1_word;
		input reg [15:0] token2_word;
		input reg [15:0] token3_word;
		input reg [15:0] token4_word;
		input reg [15:0] token5_word;
		input reg [15:0] token6_word;
		input reg [15:0] token7_word;
		reg [15:0] r;
		begin
			r = sv2v_cast_445EA(16'h0000);
			(* full_case, parallel_case *)
			case (field_format_id)
				sv2v_cast_6D350(6'd23):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token3_word;
						3'd1: r = token4_word;
						3'd2: r = token5_word;
						3'd3: r = token6_word;
						3'd4: r = token7_word;
						default:
							;
					endcase
				sv2v_cast_6D350(6'd43):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token2_word;
						3'd1: r = token3_word;
						3'd2: r = token4_word;
						3'd3: r = token5_word;
						3'd4: r = token6_word;
						3'd5: r = token7_word;
						default:
							;
					endcase
				sv2v_cast_6D350(6'd47):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token3_word;
						3'd1: r = token4_word;
						3'd2: r = token5_word;
						3'd3: r = token6_word;
						3'd4: r = token7_word;
						default:
							;
					endcase
				sv2v_cast_6D350(6'd48):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token3_word;
						3'd1: r = token4_word;
						3'd2: r = token5_word;
						3'd3: r = token6_word;
						3'd4: r = token7_word;
						default:
							;
					endcase
				sv2v_cast_6D350(6'd49):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token3_word;
						3'd1: r = token4_word;
						3'd2: r = token5_word;
						3'd3: r = token6_word;
						3'd4: r = token7_word;
						default:
							;
					endcase
				sv2v_cast_6D350(6'd52):
					(* full_case, parallel_case *)
					case (ea0_payload_words)
						3'd0: r = token3_word;
						3'd1: r = token4_word;
						3'd2: r = token5_word;
						3'd3: r = token6_word;
						3'd4: r = token7_word;
						default:
							;
					endcase
				default:
					;
			endcase
			bedrock_decode_pkg_bedrock_decode_ea1_descriptor_word = r;
		end
	endfunction
	assign ea1_descriptor_word = bedrock_decode_pkg_bedrock_decode_ea1_descriptor_word(field_format_id_o, ea0_payload_words, token0_word, token1_word, token2_word, token3_word, token4_word, token5_word, token6_word, token7_word);
	assign ea_present_o = field_extract[29-:2];
	assign ea_value_o[6+:6] = field_extract[21:16];
	assign ea_value_o[0+:6] = field_extract[27:22];
	assign field_token_words = field_extract[33-:4];
	assign ea0_descriptor_token = field_token_words;
	assign ea1_descriptor_token = field_token_words + {1'b0, ea0_payload_words};
	assign ea0_descriptor_word = field_extract[15-:bedrock_pkg_WORD_BITS];
	assign ea_descriptor_token_o[4+:4] = ea0_descriptor_token;
	assign ea_descriptor_token_o[0+:4] = ea1_descriptor_token;
	assign ea_payload_words_o[3+:3] = ea0_payload_words;
	assign ea_payload_words_o[0+:3] = ea1_payload_words;
	bedrock_ea_decode ea0_decode(
		.ea_i(ea_value_o[6+:6]),
		.descriptor_i(ea0_descriptor_word),
		.valid_o(ea_valid_o[0]),
		.reserved_o(ea_reserved_o[0]),
		.needs_descriptor_o(ea_needs_descriptor_o[0]),
		.form_o(ea_form_o[6+:6]),
		.is_register_o(ea_is_register_o[0]),
		.is_memory_o(ea_is_memory_o[0]),
		.is_immediate_o(ea_is_immediate_o[0]),
		.update_eligible_o(ea_update_eligible_o[0]),
		.signed32_index_escape_o(ea_signed32_index_escape[0]),
		.segment_selectable_o(ea_segment_selectable[0]),
		.segment_valid_o(ea_segment_valid[0]),
		.has_base_reg_o(ea_has_base_reg[0]),
		.has_index_reg_o(ea_has_index_reg[0]),
		.has_displacement_o(ea_has_displacement[0]),
		.has_absolute_o(ea_has_absolute[0]),
		.segment_o(ea_segment_o[3+:3]),
		.base_o(ea_base_o[3+:3]),
		.base_reg_o(ea_base_reg_o[3+:3]),
		.index_reg_o(ea_index_reg_o[3+:3]),
		.scale_log2_o(ea_scale_log2_o[2+:2]),
		.displacement_words_o(ea_displacement_words[0]),
		.payload_words_o(ea0_payload_words)
	);
	bedrock_ea_decode ea1_decode(
		.ea_i(ea_value_o[0+:6]),
		.descriptor_i(ea1_descriptor_word),
		.valid_o(ea_valid_o[1]),
		.reserved_o(ea_reserved_o[1]),
		.needs_descriptor_o(ea_needs_descriptor_o[1]),
		.form_o(ea_form_o[0+:6]),
		.is_register_o(ea_is_register_o[1]),
		.is_memory_o(ea_is_memory_o[1]),
		.is_immediate_o(ea_is_immediate_o[1]),
		.update_eligible_o(ea_update_eligible_o[1]),
		.signed32_index_escape_o(ea_signed32_index_escape[1]),
		.segment_selectable_o(ea_segment_selectable[1]),
		.segment_valid_o(ea_segment_valid[1]),
		.has_base_reg_o(ea_has_base_reg[1]),
		.has_index_reg_o(ea_has_index_reg[1]),
		.has_displacement_o(ea_has_displacement[1]),
		.has_absolute_o(ea_has_absolute[1]),
		.segment_o(ea_segment_o[0+:3]),
		.base_o(ea_base_o[0+:3]),
		.base_reg_o(ea_base_reg_o[0+:3]),
		.index_reg_o(ea_index_reg_o[0+:3]),
		.scale_log2_o(ea_scale_log2_o[0+:2]),
		.displacement_words_o(ea_displacement_words[1]),
		.payload_words_o(ea1_payload_words)
	);
	bedrock_agu_request_build agu0_request(
		.ea_present_i(ea_present_o[0]),
		.ea_value_i(ea_value_o[6+:6]),
		.descriptor_token_i(ea_descriptor_token_o[4+:4]),
		.ea_valid_i(ea_valid_o[0]),
		.ea_reserved_i(ea_reserved_o[0]),
		.ea_needs_descriptor_i(ea_needs_descriptor_o[0]),
		.ea_form_i(ea_form_o[6+:6]),
		.ea_is_register_i(ea_is_register_o[0]),
		.ea_is_memory_i(ea_is_memory_o[0]),
		.ea_is_immediate_i(ea_is_immediate_o[0]),
		.ea_update_eligible_i(ea_update_eligible_o[0]),
		.ea_signed32_index_escape_i(ea_signed32_index_escape[0]),
		.ea_segment_selectable_i(ea_segment_selectable[0]),
		.ea_segment_valid_i(ea_segment_valid[0]),
		.ea_has_base_reg_i(ea_has_base_reg[0]),
		.ea_has_index_reg_i(ea_has_index_reg[0]),
		.ea_has_displacement_i(ea_has_displacement[0]),
		.ea_has_absolute_i(ea_has_absolute[0]),
		.ea_segment_i(ea_segment_o[3+:3]),
		.ea_base_i(ea_base_o[3+:3]),
		.ea_base_reg_i(ea_base_reg_o[3+:3]),
		.ea_index_reg_i(ea_index_reg_o[3+:3]),
		.ea_scale_log2_i(ea_scale_log2_o[2+:2]),
		.ea_displacement_words_i(ea_displacement_words[0]),
		.ea_payload_words_i(ea0_payload_words),
		.update_mode_i(update_mode_o),
		.request_o(agu_request_o[62+:62])
	);
	bedrock_agu_request_build agu1_request(
		.ea_present_i(ea_present_o[1]),
		.ea_value_i(ea_value_o[0+:6]),
		.descriptor_token_i(ea_descriptor_token_o[0+:4]),
		.ea_valid_i(ea_valid_o[1]),
		.ea_reserved_i(ea_reserved_o[1]),
		.ea_needs_descriptor_i(ea_needs_descriptor_o[1]),
		.ea_form_i(ea_form_o[0+:6]),
		.ea_is_register_i(ea_is_register_o[1]),
		.ea_is_memory_i(ea_is_memory_o[1]),
		.ea_is_immediate_i(ea_is_immediate_o[1]),
		.ea_update_eligible_i(ea_update_eligible_o[1]),
		.ea_signed32_index_escape_i(ea_signed32_index_escape[1]),
		.ea_segment_selectable_i(ea_segment_selectable[1]),
		.ea_segment_valid_i(ea_segment_valid[1]),
		.ea_has_base_reg_i(ea_has_base_reg[1]),
		.ea_has_index_reg_i(ea_has_index_reg[1]),
		.ea_has_displacement_i(ea_has_displacement[1]),
		.ea_has_absolute_i(ea_has_absolute[1]),
		.ea_segment_i(ea_segment_o[0+:3]),
		.ea_base_i(ea_base_o[0+:3]),
		.ea_base_reg_i(ea_base_reg_o[0+:3]),
		.ea_index_reg_i(ea_index_reg_o[0+:3]),
		.ea_scale_log2_i(ea_scale_log2_o[0+:2]),
		.ea_displacement_words_i(ea_displacement_words[1]),
		.ea_payload_words_i(ea1_payload_words),
		.update_mode_i(update_mode_o),
		.request_o(agu_request_o[0+:62])
	);
	assign prefix_valid_o = !prefix_present_o || prefix_decode_valid;
	assign decode_valid_o = instruction_decode_valid;
	assign repeat_present_o = prefix_present_o && (repeat_kind_o != 2'd0);
	assign repcc_valid_o = (base_valid && (repeat_kind_o == 2'd1)) && repcc_allowed_o;
	assign repg_valid_o = (base_valid && (repeat_kind_o == 2'd2)) && repg_allowed_o;
	assign repeat_valid_o = (!repeat_present_o || repcc_valid_o) || repg_valid_o;
	assign repeat_invalid_o = repeat_present_o && !repeat_valid_o;
	assign all_ea_valid = (!ea_present_o[0] || (ea_valid_o[0] && !ea_reserved_o[0])) && (!ea_present_o[1] || (ea_valid_o[1] && !ea_reserved_o[1]));
	assign ea_payload_words_sum = (ea_present_o[0] ? {1'b0, ea0_payload_words} : 4'd0) + (ea_present_o[1] ? {1'b0, ea1_payload_words} : 4'd0);
	assign dynamic_required_words = ((field_token_words + ea_payload_words_sum) > decode_required_words ? field_token_words + ea_payload_words_sum : decode_required_words);
	assign total_required_words = dynamic_required_words + (prefix_present_o ? 4'd1 : 4'd0);
	assign required_words_o = total_required_words;
	assign undersized_o = length_words_o < total_required_words;
	assign base_valid = ((prefix_valid_o && decode_valid_o) && all_ea_valid) && !undersized_o;
	assign valid_o = base_valid && !repeat_invalid_o;
endmodule
`default_nettype wire
