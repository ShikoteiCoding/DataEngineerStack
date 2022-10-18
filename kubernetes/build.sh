#!/usr/bin/env bash

echo "Installing k3s package ..."
curl -L https://get.k3s.io > $HOME/k3s-install.sh
sudo sh $HOME/k3s-install.sh

sudo sh $HOME/setup-config.sh

echo "Setting spark permissions..."
sudo cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: spark-operator
---
apiVersion: v1
kind: Namespace
metadata:
  name: spark-apps
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: spark-apps
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-operator-role
  namespace: spark-apps
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
  - kind: ServiceAccount
    name: spark
    namespace: spark-apps
EOF

echo "Installing Helm package..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

echo "Install spark operator..."
while [ helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator | grep -q "has been added to your repositories" ];
do
    echo "Trying to add the spark-operator repo to k3s..."
    sleep 10;
done

sleep 2
helm upgrade --install spark-operator spark-operator/spark-operator \
        --set image.tag=v1beta2-1.3.7-3.1.1 \
        --namespace spark-operator \
        --set enableWebhook=true \
        --set sparkJobNamespace=spark-apps \
        --set-string enableMetrics=true \
        --set webhook.enable=true \
        --create-namespace
sleep 2
helm status --namespace spark-operator spark-operator