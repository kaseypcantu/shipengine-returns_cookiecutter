SHELL:=bash

BAKE_OPTIONS:=--no-input

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


demo_bake: ## Make a demo project using the defaults
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

watch: demo_bake ## Make a project using defaults and watch for changes
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.directory_name}}/

replay: BAKE_OPTIONS=--replay
replay: demo_bake  ## Make a replay of the last cookiecutter generated
replay: watch ## Make a replay of last cookiecutter generated and watch for changes