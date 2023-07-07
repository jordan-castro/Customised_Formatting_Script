"""
Custom Format script.
This script works as such:
    Run the script with the given arguments, options would be running 
    the script using the default which is with conversion being applied 
    in the script. The second option would be handling the conversion
    manually using 'https://cloudconvert.com'.

    The conversion is done from docx to HTML. Conversion is done to HTML
    because the docx is only modifiable from Word.

    Formatting begins by searching all bolded words. The script does not 
    know when a specific vocab word starts or beings. It can only know 
    by the lenght of the bolded text. I.e. if you have a sentance with 
    "My name is John" and you want to use "My name" as the vocab translation.
    Then you have to bold "My name" together, and not "My" and then "name" as 
    2 seperate bolded objects. If the goal is to have "My" and "name" as two 
    different vocabulary words then each word has to be bolded seperately.
    
    To recap, each object that is bolded regardless of amount of words will
    be used as the translation origin.

    After the formatting is finished, the file is then reconverted from HTML 
    to docx. Keeping the format as close as possible.

Usage: 
    custom_format.py -i <input> [-c]
    custom_format.py -h | --help
    custom_format.py --version

Options:
    -h --help       Show this screen
    --version       Show version
    -i <input>      The file to be formatted
    -c              Convert the file from docx to HTML and back to docx   
"""

from bs4 import BeautifulSoup
from googletrans import Translator
import convert
import args
import os

TRANS_MARKER = "****"

def translate(string):
    translator = Translator()
    try:    
        trans_word = translator.translate(string, src='it', dest='en')
        return trans_word.text
    except Exception as e:
        print(e)
        print(
            'SDADSA'
        )
        return None
    

def master_translation(words):
    string_ = TRANS_MARKER.join(words)
    result = translate(string_)
    return result.split(TRANS_MARKER)


def lfl(word):
    """it
    Lowercase the first letter of the word.
    """
    if word:
        return word[0].lower() + word[1:]
    else:
        return ""
    

def add_vocabulary(vocab, start):
    """
    Return a HTML soup element with the vocab words passed in.
    """
    vocab_html = ""
    for data in vocab:
        space = ""
        # Check to add a extra space
        if data[0] < 10:
            space = "&nbsp;&nbsp;"
        vocab_html += f"""
        {data[0]}&emsp;&emsp;<b class="hide">{space}{data[1]}&emsp;&emsp;</b> {data[2]}
        <br />
        """

    raw_html = f"""
    <p class="MsoNormal" style="text-align: left; font-size: 14pt;"><strong><em>Vocabulary</em></strong>
        <br />
        {vocab_html}
    </p>
    <br clear="all" style="page-break-before:always" />
    """

    vocabulary_table = soup.new_tag("class")
    vocabulary_table.append(BeautifulSoup(raw_html, 'html.parser'))
    return vocabulary_table


def add_number(text_element, number):
    """
    Add the number to the bold text
    """
    number_html = f"<sup>{number}</sup>"
    text_element.append(BeautifulSoup(number_html, 'html.parser'))


def clean_bold_elements(elements):
    """
    This will remove any empty text elements.
    """
    nes = []
    for el in elements:
        if el.text.strip() == "":
            # Don't add to list
            continue
        nes.append(el)
    return nes


def delete_temp_files():
    files = os.listdir()
    for file in files:
        if "_temp" in file:
            os.remove(file)


def save_soup(file_name, soup):
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(str(soup))


# Command line arguments
args_ = [
    {
        "name": "input",
        "short": "-i",
        "long": "--input",
        "required": True
    },
    {
        "name": "convert",
        "short": "-c",
        "long": "--convert",
        "required": False,
        "default": "1"
    }
]
arg_parser = args.Args(args_, __doc__, '0.0.1', "custom_format.py")
# Read arguments
options = arg_parser.parse()
input_file = options.input
convert_files = options.convert

# Convert files if neccesarry
if convert_files.strip() == "1": # This is the argument from above ^
    file_name = f'{input_file.split(".")[0]}_temp.html'
    if convert.convert_file(input_file, file_name):
        input_file = file_name
    else:
        print(f"""Error converting file {input_file}. Try manual conversion 
              using https://cloudconvert.com and then run again using the '-c 0' argument""")
        exit(1)


# Setup soup object
soup = None
with open(input_file, encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), 'html.parser')

# Add the vocabulary pages 
word_section = soup.body.find(class_='WordSection1')
# Add a 'page-break-before:always' to the style of the last paragraph
word_section.append(soup.new_tag('br', attrs={
    'style': 'page-break-before:always',
    'clear': 'all'
    }))

# Find the page breaks and check if there any of the 'bold' words on said page.
page_breaks = soup.find_all(lambda tag: tag.has_attr('style') and 'page-break-before:always' in tag['style'])
start = 1
last_bold_element = None
for element in page_breaks:
    # Find all previous bold elements
    bold_elements = []
    for p_element in element.find_all_previous('b'):
        if p_element == last_bold_element:
            # This also stops the vocabulary from repeating
            break
        if p_element.has_attr('class'):
            # Hide is because otherwise the vocabulary will repeat
            if "hide" in p_element['class']: 
                continue
        bold_elements.append(p_element)
    bold_elements.reverse()
    bold_elements = clean_bold_elements(bold_elements)
    last_bold_element = bold_elements[-1]
    # Grab bold text
    bold_text = [tag.text.strip() for tag in bold_elements]
    # Translate
    translation = master_translation(bold_text)
    # Add vocabulary
    vocabulary = []
    vocabulary = [(start+i, lfl(bold_text[i]), 
                   lfl(translation[i])) for i in range(len(translation))]
    element.append(add_vocabulary(vocabulary, start))
    # Number bold elements
    for el in bold_elements:
        add_number(el, start + bold_elements.index(el))
    start += len(bold_elements)


# Summary HTML
summary_html = f"""
<p class="MsoNormal">
    <strong style="text-align: left; font-size: 14pt;"><em>Riassunto della storia</em></strong>
    <br>
    <br>
    <em><strong>Summary in Italian</strong></em>
    <br>
    <br>
    <strong style="text-align: left; font-size: 14pt;"><em>Summary of the story</em></strong>
    <br>
    <br>
    <em>Summary in English</em>
</p>
<br clear="all" style="page-break-before:always" />
"""
summary_element = soup.new_tag("div")
summary_element.append(BeautifulSoup(summary_html, 'html.parser'))
word_section.append(summary_element)

# # Add questions
# questions_html = """
# <p class="MsoNormal" style="text-align: left; font-size: 14pt;"><b><em>Questions</em></b></p>

# <p class=MsoNormal style='margin-left:21.25pt;text-indent:-15.6pt'>1)<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>Question 1?</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>a.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>b.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>c.<span
# style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:21.25pt;text-indent:-15.6pt'>2)<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>Question 1?</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>a.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>b.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>c.<span
# style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:21.25pt;text-indent:-15.6pt'>3)<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>True or False?</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>a.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>b.<span
# style='font:7.0pt "Times New Roman"'>&nbsp; </span>…</p>

# <p class=MsoNormal style='margin-left:39.25pt;text-indent:-15.6pt'>c.<span
# style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp; </span>…</p>

# <p class="MsoNormal" style="text-align: left; font-size: 14pt;"><b><em>Answers</em></b></p>

# <p class="MsoNormal" style='margin:0in;line-height:normal;font-size:14pt'><b><em><b><em>1) C</em></b></h4>

# <p class="MsoNormal" style='margin:0in;line-height:normal;font-size:14pt'><b><em>2) A </em></b></h4>

# <p class="MsoNormal" style='margin:0in;line-height:normal;font-size:14pt'><b><em>3) A</em></b></h4>
# """
# questions_element = soup.new_tag('div')
# questions_element.append(BeautifulSoup(questions_html, 'html.parser'))
# word_section.append(questions_element)

# Add to the <style> tag
style = """
"""
soup.select_one('style').append(style)

# Write to file
save_soup("_temp.html", soup)

# Now convert "_temp.html" to options.input but add a Formatted at the begining
if options.convert == "1":
    format_name = f"FORMATTED_{options.input}"
    formatted_result = convert.convert_file("_temp.html", format_name)
    if formatted_result:
        print(f"Fomatting finished, file saves as {format_name}")
else:
    format_name = f"FORMATTED_{options.input.split('.')[0]}.html"
    save_soup(format_name, soup)
    print(f"""Formatting finished, file saves as {format_name}. 
Remember to convert file using https://cloudconvert.com""")

# Remove all temporary files
delete_temp_files()