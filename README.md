# Kurnik-2


## Linki
* [Jira](https://michluszcz.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog)
* [Nexus](https://nexus.mgarbowski.pl)

## DNS
* ci-cd-vm.mgarbowski.pl
  * 51.136.34.212
  * nexus.mgarbowski.pl
* deployment-vm.mgarbowski.pl
  * 104.40.144.201

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
* Jest utworzone jedno repozytorium typu docker (hosted)
  * docker-images
  * na obrazy dockerowe

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

## Backup serwera CI/CD
* Wszystkie dane, które mają być przechowywane w sposób trwały, muszą być zapisane w docker volume.

### Wykonanie i pobranie backupu
```shell
./deployment/backup-ci-cd-vm.sh
```

## Jenkins
Playbook `jenkins-docker.yaml` instaluje Jenkinsa w wraz z agentem w kontenerze.
Konfiguracaj samego Jenkinsa nie jest robiona automatycznie i musi być wykonana ręcznie w nastepujących krokach:
- Przejście przez proces aktywacji Jenkinsa
- Dodanie credentiaili:
  - Prywatny klucz SSH wygenerowany na maszynie `ci-cd-vm` w `/home/azureuser/.ssh/id_rsa`
  - Github Classic Token - do automatycznego ustawiania webhooków przez Jenkinsa
- Dodanie agenta w Jenkinsie (`Manage Jenkins` -> `Manage Nodes and Clouds` -> `New Node`)
- Utworzenie multibranch pipeline dla projektu i odpowiednie skonfigurowanie `Sources` w tymże pipelinie
