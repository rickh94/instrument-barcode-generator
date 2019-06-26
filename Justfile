clean:
    rm -f codes/*.png
    rm -f labels/*.png
    rm -f pages/*.png
generate:
    pipenv run python generate.py
combine:
    pipenv run python combine.py
