import docker


def run_container(app):
    client = docker.from_env()
    container = client.containers.run(
        image=app.image, command=app.command, environment=app.envs, detach=True
    )
    return container.id


def stop_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
