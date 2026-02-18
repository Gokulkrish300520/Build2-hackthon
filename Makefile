# Makefile for building and running Docker containers for Vercel

.PHONY: build-admin build-backend run-admin run-backend push-admin push-backend

ADMIN_PATH=Admin\ UI
BACKEND_PATH=backend
ADMIN_IMAGE=admin-ui:latest
BACKEND_IMAGE=backend-api:latest

build-admin:
	docker build -t $(ADMIN_IMAGE) "$(ADMIN_PATH)"

build-backend:
	docker build -t $(BACKEND_IMAGE) $(BACKEND_PATH)

run-admin:
	docker run -p 3000:3000 $(ADMIN_IMAGE)

run-backend:
	docker run -p 8000:8000 $(BACKEND_IMAGE)

push-admin:
	docker tag $(ADMIN_IMAGE) <your-registry>/$(ADMIN_IMAGE)
	docker push <your-registry>/$(ADMIN_IMAGE)

push-backend:
	docker tag $(BACKEND_IMAGE) <your-registry>/$(BACKEND_IMAGE)
	docker push <your-registry>/$(BACKEND_IMAGE)
