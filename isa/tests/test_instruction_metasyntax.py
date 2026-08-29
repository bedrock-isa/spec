import unittest

from engine.instruction_metasyntax import (
    InstructionMetasyntax,
    InstructionMetasyntaxError,
)


class InstructionMetasyntaxTest(unittest.TestCase):
    def test_parses_instruction_without_operands(self) -> None:
        syntax = InstructionMetasyntax("NOP")

        self.assertEqual(syntax.mnemonic, "NOP")
        self.assertEqual(syntax.operands, ())
        self.assertEqual(str(syntax), "NOP")

    def test_parses_fixed_and_selected_size_suffixes(self) -> None:
        fixed = InstructionMetasyntax("MOV.Q Rn(r), SP")
        selected = InstructionMetasyntax(
            "FETCHADD.{B|W|L|Q}(z)/order(o) Rn(s), <ea>(e)"
        )

        self.assertEqual(fixed.fixed_size_suffix, ".Q")
        self.assertEqual(selected.selected_size_codes, ("B", "W", "L", "Q"))
        self.assertEqual(selected.size_field, "z")
        self.assertEqual(selected.order_field, "o")
        self.assertEqual(
            [(operand.name, operand.angled, operand.field) for operand in selected.operands],
            [("Rn", False, "s"), ("ea", True, "e")],
        )

    def test_parses_literals_and_operand_groups(self) -> None:
        literal = InstructionMetasyntax("ADD.Q 8, SP")
        group = InstructionMetasyntax("REPcc Rn(r), (<instruction>)")
        braced = InstructionMetasyntax("REP { <instruction>... }")

        self.assertEqual(literal.operands[0].literal, 8)
        self.assertEqual(group.operands[1].group_style, "parenthesized")
        self.assertEqual(braced.operands[0].group_style, "braced")

    def test_parses_and_flattens_vector_address(self) -> None:
        syntax = InstructionMetasyntax(
            "VGATHER.{B|W|L|Q}(z) Pn(p), Pn(c), "
            "[Rn(b) + Vn(x) * <scale> + <disp16s>], Vn(v)"
        )

        address = syntax.operands[2]
        self.assertEqual(address.kind, "address")
        self.assertNotIn("lane_index", [member.kind for member in address.members])
        self.assertEqual(
            [operand.name for operand in syntax.displayed_operands],
            ["Pn", "Pn", "Rn", "Vn", "disp16s", "Vn"],
        )

    def test_parse_is_idempotent(self) -> None:
        syntax = InstructionMetasyntax("JMP <imm16s>")
        self.assertIs(InstructionMetasyntax.parse(syntax), syntax)

    def test_derives_canonical_encoding_id_without_mnemonic(self) -> None:
        syntax = InstructionMetasyntax("ADD.{L|Q}(z) Rn(s), Rn(d)")
        self.assertEqual(
            syntax.encoding_id,
            "l_q_z_rn_s_rn_d",
        )
        self.assertEqual(InstructionMetasyntax("NOP").encoding_id, "plain")

    def test_encoding_id_keeps_address_operators_without_structural_noise(self) -> None:
        addressed = InstructionMetasyntax("OP [Rn(b) + Rn(i) * 4]")

        self.assertEqual(addressed.encoding_id, "rn_b_add_rn_i_mul_4")
        self.assertNotIn("field", addressed.encoding_id)
        self.assertNotIn("literal", addressed.encoding_id)
        self.assertNotIn("op", addressed.encoding_id)

    def test_rejects_noncanonical_or_malformed_text(self) -> None:
        for value in (
            "",
            "ADD  Rn(s)",
            "ADD Rn(s),Rn(d)",
            "ADD.{B|B}(z) Rn(s)",
            "ADD.{B|W}(Z) Rn(s)",
            "ADD.Q/order(o) Rn(s)",
            "ADD <ea",
            "ADD [Rn(b)",
        ):
            with self.subTest(value=value):
                with self.assertRaises(InstructionMetasyntaxError):
                    InstructionMetasyntax(value)


if __name__ == "__main__":
    unittest.main()
