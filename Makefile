

all:lint

lint:lint_markdown lint_python check_data check_source_exist

lint_markdown:
	find *.md data/ docs/ | grep '\.md$$' \
		| xargs npx markdownlint --config ./.markdownlint.json

POETRY_NO_ROOT:= --no-root
setup_python:
	poetry install $(POETRY_OPTION)

lint_python: pyright black flake8 isort yamllint jsonlint pydocstyle

pyright:
	npx pyright

black:
	find ./scripts | grep py$$ | xargs black --diff | diff /dev/null -

flake8:
	find ./scripts | grep py$$ | xargs flake8

isort:
	find ./scripts | grep py$$ | xargs isort --diff | diff /dev/null -

yamllint:
	find . -name '*.yml' -type f | grep -v node_modules | xargs yamllint --no-warnings

jsonlint:
	python3 -c "import sys,json;print(json.dumps(\
	    json.loads(sys.stdin.read()),\
	    indent=4,ensure_ascii=False,sort_keys=True))" \
	< ./.markdownlint.json  | diff -q - ./.markdownlint.json

pydocstyle:
	pydocstyle ./scripts --ignore=D100,D101,D102,D103,D104,D105,D107,D203,D212,D400,D415

check_data:
	find . -name '*.tsv' | xargs python3 scripts/check_data.py

check_source_exist:
	python3 scripts/check_source_exist.py \
	    --source data/rte.lrec2020_sem_short.tsv \
	    --data data/rte.lrec2020_mlm.tsv \
	    --op data/operation.rte.lrec2020_mlm.tsv

