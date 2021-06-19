IMAGE_NAME=felipemocruha/sistemas-distribuidos-antifraud
IMAGE_VERSION=aula-1


docker:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) -f Dockerfile .

push:
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)
