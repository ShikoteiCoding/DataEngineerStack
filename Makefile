# useless for now as no dockerfile
build_broker:
	cd devops/kafka/ && \
	docker-compose build zookeeper kafka

build_generator:
	cd microservices && \
	docker build --tag 'generator' generator/.

start_broker:
	cd devops/kafka/ && \
	docker-compose up zookeeper kafka

start_generator:
	cd microservices && \
	docker-compose up generator

start_network:
	docker network rm cluster && \
	docker network create cluster && \
	docker network connect cluster kafka && \
	docker network connect cluster zookeeper && \
	docker network connect cluster generator