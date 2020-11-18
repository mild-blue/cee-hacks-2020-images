.PHONY: help

.DEFAULT: help
help:
	@echo "TODO"

build_and_push_worker:
	. ./devops/build_and_push_to_dockerhub.sh && build_and_push_worker

build_and_push_backend:
	. ./devops/build_and_push_to_dockerhub.sh && build_and_push_backend

redeploy_staging:
	. ./devops/redeploy_staging.sh