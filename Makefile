current_dir = $(shell pwd)

PROJECT = ml_core

DOCKERFILES = Dockerfile:$(PROJECT)
DOCKER_ORG = "srcd"

# Including ci Makefile
CI_REPOSITORY ?= https://github.com/src-d/ci.git
CI_BRANCH ?= v1
CI_PATH ?= .ci
MAKEFILE := $(CI_PATH)/Makefile.main
$(MAKEFILE):
	git clone --quiet --depth 1 -b $(CI_BRANCH) $(CI_REPOSITORY) $(CI_PATH);
-include $(MAKEFILE)

.PHONY: check
check:
	! (grep -R /tmp sourced/ml/core/tests)
	flake8 --count
	pylint sourced

.PHONY: test
test:
	python3 -m unittest discover

.PHONY: docker-test
docker-test:
	docker ps | grep bblfshd  # bblfsh server should be run. Try `make bblfsh-start` command.
	docker run --rm -it --network host --entrypoint python3 -w /ml_core \
		-e SKIP_BBLFSH_UTILS_TESTS=1 \
		srcd/ml_core:$(VERSION) -m unittest discover

.PHONY: bblfsh-start
bblfsh-start:
	! docker ps | grep bblfshd # bblfsh server should not be running already
	docker run -d --name ml_core_bblfshd --privileged -p 9432\:9432 bblfsh/bblfshd\:v2.12.1
	docker exec -it ml_core_bblfshd bblfshctl driver install python bblfsh/python-driver\:v2.9.0
