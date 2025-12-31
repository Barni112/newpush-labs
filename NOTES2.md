# vbox setup

- name: newpushlab
- iso: netinst
- ram: 6144 MB
- cpu: 8
- disk: 60 GB
- network: bridge

# install debian

- lang: english
- location: hungary
- locale: us
- keyboard: hungarian
- hostname: newpushlab
- root pw: labuser
- user: Lab User, labuser, labuser
- standard system utilities, ssh server

# setup

```bash
apt install sudo vim git ansible python3.13-venv make
usermod -aG sudo labuser
git clone -b customized https://github.com/Barni112/newpush-labs.git
cd newpush-labs
python3 -m venv .venv
bash -c "source .venv/bin/activate && pip3 install -r provisioning/ansible/requirements.txt"
ansible-galaxy install -r provisioning/ansible/requirements.yaml
cp provisioning/ansible/group_vars/lab.yaml.example provisioning/ansible/group_vars/lab.yaml
echo "fill in <PRIVATE_IP_OF_VM> in provisioning/ansible/group_vars/lab.yaml"
echo "generate key and self-signed cert, and put them in services/traefik/certs"
```

# install & test

```bash
sudo bash -c "source .venv/bin/activate && make setup HOSTS_FILE=./provisioning/ansible/inventory/hosts"
sudo bash -c "source .venv/bin/activate && make test"
```

# quick up down

```bash
docker compose -f /opt/student-lab/services/docker-compose.yaml -p lab-core up -d
docker compose -f /opt/student-lab/services/docker-compose.yaml -p lab-core stop
docker compose -f /opt/student-lab/services/docker-compose.yaml -p lab-core down
docker container ls --format '{{.Names}}\t enabled:{{.Label "sablier.enable"}}'| grep enabled:true | awk '{print $1}' | xargs -r docker container stop
```

# get user password from casdoor db

- docker inspect casdoor -> Mounts -> casdoor.db
- docker run -it --rm -v /opt/student-lab/services/casdoor:/db alpine sh
    - apk add sqlite
    - sqlite3 /db/casdoor.db
        - .tables
        - SELECT * from user;

# generate key and self-signed cert

```bash
openssl req -x509 -noenc -days 3650 -newkey rsa:4096 -keyout self_signed.key -out self_signed.crt -subj "/CN=192.168.0.133.traefik.me" -addext "subjectAltName = DNS:192.168.0.133.traefik.me,DNS:*.192.168.0.133.traefik.me" -sha256
```
