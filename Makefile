# Microservices
build_generator:
	cd microservices/generator && docker build --tag generator .

start_generator:
	kubectl apply -f k8s-local/generator/namespace.yaml
	kubectl apply -f k8s-local/generator/ --validate=false

stop_generator:
	kubectl delete --ignore-not-found -f k8s-local/generator/