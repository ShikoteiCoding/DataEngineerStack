# useless for now as no dockerfile
build_broker:
	cd devops/kafka/ && \
	docker-compose build zookeeper kafka

start_broker:
	cd devops/kafka/ && \
	docker-compose up zookeeper kafka

build_generator:
	cd microservices/generator && \
	docker build .