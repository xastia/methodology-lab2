import argparse
import sys
import re

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def write_file(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def parse_markdown(md_content):
    html_content = ""
    
    # Regex patterns for basic markdown elements
    patterns = {
        'bold': re.compile(r'\*\*(.*?)\*\*'),
        'italic': re.compile(r'_(.*?)_'),
        'monospaced': re.compile(r'`(.*?)`'),
        'preformatted': re.compile(r'```(.*?)```', re.DOTALL)
    }

    in_preformatted_block = False
    preformatted_content = ""

    lines = md_content.split('\n')
    for line in lines:
        if line.strip().startswith("```"):
            if in_preformatted_block:
                in_preformatted_block = False
                html_content += f"<pre>{preformatted_content.strip()}</pre>\n"
            else:
                in_preformatted_block = True
                preformatted_content = ""
            continue

        if in_preformatted_block:
            preformatted_content += line + '\n'
            continue

        # Bold
        line = patterns['bold'].sub(r'<b>\1</b>', line)
        
        # Italic
        line = patterns['italic'].sub(r'<i>\1</i>', line)
        
        # Monospaced
        line = patterns['monospaced'].sub(r'<tt>\1</tt>', line)
        
        # Paragraphs
        if line.strip():
            html_content += f"{line}\n"
        else:
            html_content += "</p>\n<p>"
    
    if in_preformatted_block:
        html_content += f"<pre>{preformatted_content.strip()}</pre>\n"
    
    # Wrapping content in paragraph tags if necessary
    if not in_preformatted_block:
        html_content = "<p>" + html_content.strip() + "</p>"
        html_content = html_content.replace("<p></p>", "")

    return html_content

def parse_markdown_to_ansi(md_content):
    ansi_content = ""

    # Regex patterns for basic markdown elements
    patterns = {
        'bold': re.compile(r'\*\*(.*?)\*\*'),
        'italic': re.compile(r'_(.*?)_'),
        'monospaced': re.compile(r'`(.*?)`'),
        'preformatted': re.compile(r'```(.*?)```', re.DOTALL)
    }

    in_preformatted_block = False
    preformatted_content = ""

    lines = md_content.split('\n')
    for line in lines:
        if line.strip().startswith("```"):
            if in_preformatted_block:
                in_preformatted_block = False
                ansi_content += f"\033[3m{preformatted_content.strip()}\033[0m\n"
            else:
                in_preformatted_block = True
                preformatted_content = ""
            continue

        if in_preformatted_block:
            preformatted_content += line + '\n'
            continue

        # Bold
        line = patterns['bold'].sub(r'\033[1m\1\033[0m', line)
        
        # Italic
        line = patterns['italic'].sub(r'\033[3m\1\033[0m', line)
        
        # Monospaced
        line = patterns['monospaced'].sub(r'\033[3m\1\033[0m', line)
        
        ansi_content += line + '\n'

    if in_preformatted_block:
        ansi_content += f"\033[3m{preformatted_content.strip()}\033[0m\n"
    
    return ansi_content.strip() + '\n'



def main():
    parser = argparse.ArgumentParser(description='Convert Markdown file to formatted output.')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('--out', dest='output_file', help='Path to the output file')
    parser.add_argument('--format', dest='format', choices=['html', 'ansi'], help='Output format: html or ansi', default=None)
    
    args = parser.parse_args()
    
    md_content = read_file(args.input_file)
    
    if args.output_file:
        output_format = args.format if args.format else 'html'
    else:
        output_format = args.format if args.format else 'ansi'
    
    if output_format == 'html':
        output_content = parse_markdown(md_content)
    else:
        output_content = parse_markdown_to_ansi(md_content)
    
    if args.output_file:
        write_file(output_content, args.output_file)
    else:
        print(output_content)

if __name__ == '__main__':
    main()


