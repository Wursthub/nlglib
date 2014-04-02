import unittest

from nlg.structures import MsgSpec, Message, Paragraph, Section, Document
from nlg.structures import String, PlaceHolder, Clause, NP, VP

from nlg.lexicalisation import templates
from nlg.lexicalisation import lexicalise_message_spec
from nlg.lexicalisation import lexicalise_message
from nlg.lexicalisation import lexicalise_paragraph
from nlg.lexicalisation import lexicalise_section
from nlg.lexicalisation import lexicalise_document


class DummyMsg(MsgSpec):
    def __init__(self):
        super().__init__('dummy')

    def arg_subject(self):
        return NP('Boris')

# add a template for the message spec.
templates.templates['dummy'] = Clause(
            PlaceHolder('arg_subject'), VP('is', 'fast'))

class TestLexicalisation(unittest.TestCase):
    """ Tests for converting a MsgSpec into an NLG Element. """

    def test_lexicalise_msg_spec(self):
        """ Test lexicalisation of MsgSpec. """
        msg = DummyMsg()
        res = lexicalise_message_spec(msg)
        expected = [String('Boris'), String('is'), String('fast')]
        self.assertEqual(expected, list(res.constituents()))

    def test_lexicalise_msg(self):
        """ Test lexicalisation of Message. """
        # a message with 1 nucleus and 2 satelites
        m = Message('Elaboration', DummyMsg(), DummyMsg(), DummyMsg())
        lex = lexicalise_message(m)
        tmp = list(lexicalise_message_spec(DummyMsg()).constituents())
        expected = tmp + tmp + tmp
        self.assertEqual(expected, list(lex.constituents()))

    def test_lexicalise_paragraph(self):
        """ Test lixicalisation of Paragraph. """
        m = Message('Elaboration', DummyMsg(), DummyMsg(), DummyMsg())
        p = Paragraph(m)
        tmp = lexicalise_paragraph(p)
        expected = '\tBoris is fast Boris is fast Boris is fast'
        self.assertEqual(expected, str(tmp))

    def test_lexicalise_paragraph(self):
        """ Test lixicalisation of Paragraph. """
        m = Message('Elaboration', DummyMsg(), DummyMsg(), DummyMsg())
        p = Paragraph(m)
        tmp = lexicalise_paragraph(p)
        expected = '\tBoris is fast Boris is fast Boris is fast'
        self.assertEqual(expected, str(tmp))

    def test_lexicalise_section(self):
        """ Test lixicalisation of Section. """
        m = Message('Elaboration', DummyMsg(), DummyMsg(), DummyMsg())
        p = Paragraph(m)
        s = Section('Section 1', p)
        tmp = lexicalise_section(s)
        expected = 'Section 1\n\tBoris is fast Boris is fast Boris is fast'
        self.assertEqual(expected, str(tmp))

        s = Section('Section 1', p, p, p)
        tmp = lexicalise_section(s)
        expected = 'Section 1' + \
            '\n\tBoris is fast Boris is fast Boris is fast' + \
            '\n\tBoris is fast Boris is fast Boris is fast' + \
            '\n\tBoris is fast Boris is fast Boris is fast'
        self.assertEqual(expected, str(tmp))

    def test_lexicalise_document(self):
        """ Test lixicalisation of Document. """
        m1 = Message('Leaf', DummyMsg())
        m2 = Message('Elaboration', DummyMsg(), DummyMsg())
        p = Paragraph(m1, m2)
        s = Section('Section One', Paragraph(m1))
        d = Document('Doc Title', s, Section('Section Two', Paragraph(m2)))
        tmp = lexicalise_document(d)
        expected = 'Doc Title\n' + \
            'Section One' + \
            '\n\tBoris is fast' + \
            '\n\nSection Two' + \
            '\n\tBoris is fast Boris is fast'
        self.assertEqual(expected, str(tmp))


if __name__ == '__main__':
    unittest.main()