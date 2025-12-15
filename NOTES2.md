# vbox setup
- name: newpushlab
- iso: netinst
- ram: 10240 MB
- cpu: 8
- disk: 80 GB
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
git clone -b keycloak-wip https://github.com/Barni112/newpush-labs.git
cd newpush-labs
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r provisioning/ansible/requirements.txt
ansible-galaxy install -r provisioning/ansible/requirements.yaml
cp provisioning/ansible/group_vars/lab.yaml.example provisioning/ansible/group_vars/lab.yaml
```

# install & test
```bash
sudo bash -c "source .venv/bin/activate && make setup HOSTS_FILE=./provisioning/ansible/inventory/hosts"
sudo bash -c "source .venv/bin/activate && make test"
```

# user password
- docker inspect casdoor -> Mounts -> casdoor.db
- docker run -it --rm -v /opt/student-lab/services/casdoor:/db alpine sh
  - apk add sqlite
  - sqlite3 /db/casdoor.db
    - .tables
    - SELECT * from user;
