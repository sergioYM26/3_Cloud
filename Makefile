SHELL=/bin/bash
CDK_DIR=src/
COMPOSE_RUN = docker compose run --rm cdk-base

_prep-cache: #This resolves Error: EACCES: permission denied, open 'cdk.out/tree.json'
	mkdir -p ${CDK_DIR}cdk.out/

container-build: pre-reqs
	docker-compose build

container-info:
	${COMPOSE_RUN} make _container-info

_container-info:
	./containerInfo.sh

clear-cache:
	${COMPOSE_RUN} rm -rf ${CDK_DIR}cdk.out && rm -rf ${CDK_DIR}node_modules

cli: _prep-cache
	docker-compose run cdk-base /bin/bash

pip-install: _prep-cache
	${COMPOSE_RUN} make _pip-install

_pip-install:
	python3 -m venv .venv && source .venv/bin/activate && pip install poetry && poetry install

synth: _prep-cache
	${COMPOSE_RUN} make _synth

_synth: _pip-install
	source .venv/bin/activate && cd ${CDK_DIR} && cdk synth --no-staging ${PROFILE}

bootstrap: _prep-cache
	${COMPOSE_RUN} make _bootstrap

_bootstrap:
	source .venv/bin/activate && cd ${CDK_DIR} && cdk bootstrap ${PROFILE}

deploy: _prep-cache
	${COMPOSE_RUN} make _deploy

_deploy: _pip-install
	source .venv/bin/activate && cd ${CDK_DIR} && cdk deploy --require-approval never ${PROFILE}

destroy: _prep-cache
	${COMPOSE_RUN} make _destroy

_destroy: _pip-install
	source .venv/bin/activate && cd ${CDK_DIR} && cdk destroy --force ${PROFILE}

diff: _prep-cache
	${COMPOSE_RUN} make _diff

_diff: _pip-install
	source .venv/bin/activate && cd ${CDK_DIR} && cdk diff ${PROFILE}

test: _prep-cache
	${COMPOSE_RUN} make _test

_test: _pip-install
	source .venv/bin/activate && cd ${CDK_DIR} && pytest run


