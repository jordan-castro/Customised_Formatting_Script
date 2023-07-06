# Instructions
## Installing
Open a terminal window at the location of the unziped folder. and run
```
chmod +x run.sh
```

Once chmod, it can now be executed easily by writing 
```
./run.sh
```
Into the terminal window.

## How to use
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
    custom_format.py -i <-input> [-c]
    <!-- custom_format.py -h | --help -->
    <!-- custom_format.py --version -->

Options:
    -h --help       Show this screen
    --version       Show version
    -i <-input>      The file to be formatted
    -c              Convert the file from docx to HTML and back to docx   
