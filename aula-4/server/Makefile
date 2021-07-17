IMAGE_NAME=felipemocruha/sistemas-distribuidos-server
IMAGE_VERSION=aula-4


docker:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) -f Dockerfile .

push:
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)
