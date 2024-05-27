import unittest
from lab2 import parse_markdown, parse_markdown_to_ansi

class TestMarkdownParser(unittest.TestCase):

    def test_bold_html(self):
        md_content = "This is **bold** text."
        expected_output = "<p>This is <b>bold</b> text.</p>"
        self.assertEqual(parse_markdown(md_content), expected_output)

    def test_italic_html(self):
        md_content = "This is _italic_ text."
        expected_output = "<p>This is <i>italic</i> text.</p>"
        self.assertEqual(parse_markdown(md_content), expected_output)

    def test_monospaced_html(self):
        md_content = "This is `monospaced` text."
        expected_output = "<p>This is <tt>monospaced</tt> text.</p>"
        self.assertEqual(parse_markdown(md_content), expected_output)

    def test_preformatted_html(self):
        md_content = "```Preformatted text **He He**```"
        expected_output = "<pre></pre>\n"
        self.assertEqual(parse_markdown(md_content), expected_output)

    def test_bold_ansi(self):
        md_content = "This is **bold** text."
        expected_output = "This is \033[1mbold\033[0m text.\n"
        self.assertEqual(parse_markdown_to_ansi(md_content), expected_output)

    def test_italic_ansi(self):
        md_content = "This is _italic_ text."
        expected_output = "This is \033[3mitalic\033[0m text.\n"
        self.assertEqual(parse_markdown_to_ansi(md_content), expected_output)

    def test_monospaced_ansi(self):
        md_content = "This is `monospaced` text."
        expected_output = "This is \033[3mmonospaced\033[0m text.\n"
        self.assertEqual(parse_markdown_to_ansi(md_content), expected_output)

    def test_preformatted_ansi(self):
        md_content = "```Preformatted text **He He**```"
        expected_output = "\033[3m\033[0m\n"
        self.assertEqual(parse_markdown_to_ansi(md_content), expected_output)

if __name__ == '__main__':
    unittest.main()


