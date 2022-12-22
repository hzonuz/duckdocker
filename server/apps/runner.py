import docker


def run_container(image, command, envs):
    client = docker.from_env()
    container = client.containers.run(
        image=image, command=command, environment=envs, detach=True
    )
    return container


def stop_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
