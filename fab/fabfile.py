from fabric.api import run, sudo, cd, lcd, local, put, prompt
from fabric.contrib import files

def setup_worker_node():
    pass

def setup_worker_proxy():


def setup_worker_pyenv():
    sudo("apt-get install git")
    sudo("apt-get install build-essential")
    sudo("apt-get install libsqlite3-dev")
    sudo("apt-get install sqlite3")
    sudo("apt-get install bzip2 libbz2-dev")
    sudo("apt-get install libssl-dev openssl")
    sudo("apt-get install libreadline6 libreadline6-dev")
    cd('~')
    run("git clone https://github.com/yyuu/pyenv.git .pyenv")
    run("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.bashrc")
    run("echo 'export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.bashrc")
    run("echo 'eval \"$(pyenv init -)\"' >> ~/.bash_profile")
    run("exec $SHELL")


def setup_worker_install_pyenv_python(version="2.7.9"):
    run("pyenv install %s" % version)
    run("pyenv rehash")
    run("pyenv global %s" % version)


def deploy_mbs(repo=""):
    if repo == "":
        repo = prompt("MBS repository?: ")
        
    cd('~')
    run("git clone %s message_simulator" % repo)

def deploy_worker(repo=""):
    if repo == "":
        repo = prompt("worker repository?: ")
    
    cd('~')
    run("git clone %s message_simulator_gui" % repo)

def start_worker():
    cd('~/message_simulator_gui')
    run("celery -A sim_dashboard worker -l info")


def deploy_sshkey(ssh_key=""):
    if ssh_key == "":
        ssh_key = prompt("Specify ssh public key file:" )
    
    if files.exists('~/.ssh/id_rsa.pub'):
        
    put(ssh_key, '~/.ssh/id_rsa.pub')
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
    run('chmod 600 ~/.ssh/authorized_keys')
    




