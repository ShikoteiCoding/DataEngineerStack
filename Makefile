# useless for now as no dockerfile
build_broker:
	cd devops/kafka/ && \
	docker-compose build zookeeper kafka

build_generator:
	cd microservices && \
	docker build --tag 'generator' generator/.

init:
	docker network create cluster

start_broker:
	cd devops/kafka/ && \
	docker-compose up zookeeper kafka && \
	docker network connect cluster zookeeper && \
	docker network connect cluster kafka

start_generator:
	docker-compose --file microservices/docker-compose.yaml up generator && \
	docker network connect cluster generator

make clear:
	docker network rm cluster