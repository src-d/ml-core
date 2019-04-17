current_dir = $(shell pwd)

.PHONY: check
check:
	! (grep -R /tmp ml_core/tests)
	flake8 --count
	pylint ml_core

.PHONY: test
test:
	python3 -m unittest discover

.PHONY: docs
docs:
	cd docs && python3 -msphinx -M html . build

.PHONY: docker-build
docker-build:
	docker build -t srcd/m_corel .

.PHONY: docker-test
docker-test: docker-build
	docker ps | grep bblfshd  # bblfsh server should be running
	docker run --rm -it --network host --entrypoint python3 -w /ml_core \
		-v $(current_dir)/.git:/ml_core/.git \
		srcd/ml_core -m unittest discover
