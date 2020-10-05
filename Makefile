
all: lint_markdown lint_python check_data check_source_exist

setup: setup_npm_module


setup_node_module:
	npm install markdownlint-cli

lint_markdown:
	find . -maxdepth 1| grep '\.md$$' \
		| xargs npx markdownlint --config ./.markdownlint.json

setup_pip:
	pip install -r requirements.txt $(PIP_OPTION)

lint_python: mypy autopep8 flake8 isort yamllint jsonlint
mypy:
	find scripts | grep py$$ | xargs mypy --python-version 3.7 \
              --show-column-numbers --show-error-codes \
              --check-untyped-defs --ignore-missing-imports \
              --follow-imports skip --strict-equality

autopep8:
	find scripts | grep py$$ | xargs autopep8 -d | diff /dev/null -

flake8:
	find scripts | grep py$$ | xargs flake8

isort:
	find scripts | grep py$$ | xargs isort --diff | diff /dev/null -

yamllint:
	yamllint --no-warnings ./.circleci/config.yml

jsonlint:
	python3 -c "import sys,json;print(json.dumps(\
	    json.loads(sys.stdin.read()),\
	    indent=4,ensure_ascii=False,sort_keys=True))" \
	< .markdownlint.json  | diff -q - .markdownlint.json


check_data:
	find . -name '*.tsv' | xargs python3 scripts/check_data.py

check_source_exist:
	python3 scripts/check_source_exist.py \
	    --source data/rte.lrec2020_sem_short.tsv \
	    --data data/rte.lrec2020_mlm.tsv \
	    --op data/operation.rte.lrec2020_mlm.tsv

.PHONY: all setup setup_node_module \
    lint_markdown setup_pip \
    lint_python mypy autopep8 flake8 isort yamllint jsonlint\
    check_data check_source_exist

.DELETE_ON_ERROR:
