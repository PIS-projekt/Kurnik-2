# Kurnik-2

* [Jira](https://michluszcz.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog)

## Korzystanie z Ansible

### Instalacja
Ansible instaluje się na maszynie programisty.
Ansible łączy się z maszynami zdalnymi za pomocą SSH.

```shell
python3 -m venv .venv
source ./.venv/bin/activate
pip install ansible
```

### Konfiguracja ci-cd-vm
* Instalacja dockera
* Utworzenie użytkowników
* Instalacja Nexusa i uruchomienie

```shell
ansible-playbook -u azureuser -i deployment/inventory.ini deployment/install-docker.yaml
ansible-playbook -u azureuser -i deployment/inventory.ini deployment/users.yaml
ansible-playbook -u azureuser -i deployment/inventory.ini deployment/nginx.yaml
ansible-playbook -i deployment/inventory.ini deployment/nexus.yaml
```

## Korzystanie z Nexus
* Jest utworzony jeden użytkownik - admin
  * hasło na Discordzie
* Jest utworzone jedno repozytorium typu raw (hosted)
  * test-repository
  * na zwykłe pliki

### Upload pliku do Nexusa

```shell
curl -u "admin:password" --upload-file ./index.html https://nexus.mgarbowski.pl/repository/test-repository/website/index.html
```

### Pobranie pliku z Nexusa

```shell
curl -u "admin:password" https://nexus.mgarbowski.pl/repository/test-repository/website/index.html -o index.html
```

### Upload docker image do Nexusa

```shell
# Zbudowanie obrazu
docker build --tag pis-frontend:latest frontend/

# Nadanie tagu obrazowi
docker tag pis-frontend:latest nexus.mgarbowski.pl/docker-images/pis-frontend:latest

# Logowanie do Nexusa
docker login nexus.mgarbowski.pl

# Wysłanie obrazu do Nexusa
docker push nexus.mgarbowski.pl/docker-images/pis-frontend:latest

# Pobranie obrazu z Nexusa
docker pull nexus.mgarbowski.pl/docker-images/pis-frontend:latest
```

## Nginx
* Volume `certs` musi zawierać pliki wygenerowane przez letsencrypt - nie mogą się znajdować w repozytorium
  * Pytania -> Mikołaj Garbowski