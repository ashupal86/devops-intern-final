job "hello" {
  datacenters = ["dc1"]
  type        = "service"

  group "hello-group" {
    count = 1

    task "hello-task" {
      driver = "docker"

      config {
        image = "ashu111/devops-hello:latest"
        force_pull = false   # 👈 prevents Nomad from trying to pull from DockerHub
      }

      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
