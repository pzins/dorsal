filename=$(basename "$1")
extension="${filename##*.}"
filename="${filename%.*}"
if [ "$1" != "" ]; then
    if [ "$filename" = "$extension" ]; then
        python3 -m "py_compile" $1.py
        cp __pycache__/$filename.cpython-35.pyc .   
        chmod +x $filename.cpython-35.pyc
    else
        python3 -m "py_compile" $1
        cp __pycache__/$filename.cpython-35.pyc .   
        chmod +x $filename.cpython-35.pyc
    fi
else
    python3 -m "py_compile" *.py
    cp __pycache__/*.cpython-35.pyc .   
    chmod +x *.cpython-35.pyc
fi
