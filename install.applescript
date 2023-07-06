on run argv
    set argumentCount to count of argv
    if argumentCount > 0 then
        set firstArgument to item 1 of argv
    end if

    if firstArgument = "pip3"
        do shell script "pip3 install -r requirements.txt"
    else
        do shell script "pip install -r requirements.txt"
    end if
end run

do shell script "python -m venv env"
do shell script "source env/bin/activate"
do shell script "pip install -r requirements.txt"
do shell script "deactivate"

do shell script "chmod +x run.sh"