from fabric.api import run, sudo, cd, lcd, local, put, prompt, env
from fabric.contrib import files

def setup_worker_node():
    pass

def setup_worker_01_fnet_ubuntu(apt_proxy_file="", env_proxy_file="", resolvconf=""):
    put(apt_proxy_file, '/etc/apt/apt.conf', use_sudo=True)
    put(env_proxy_file, '/etc/profile.d/fnet.sh', use_sudo=True)
    put(resolvconf, '/etc/resolvconf/resolv.conf.d/base', use_sudo=True)
    sudo("service resolvconf restart")

def setup_worker_01_fnet_centos():
    pass

def setup_worker_02_install_required_apt():
    ## for mbs
    sudo("apt-get -y install redis-server")
    
    ## for pyenv
    sudo("apt-get -y install git")
    sudo("apt-get -y install build-essential")
    sudo("apt-get -y install libsqlite3-dev")
    sudo("apt-get -y install sqlite3")
    sudo("apt-get -y install bzip2 libbz2-dev")
    sudo("apt-get -y install libssl-dev openssl")
    sudo("apt-get -y install libreadline6 libreadline6-dev")

    ## for scipy
    sudo("apt-get -y install libblas-dev gfortran liblapack-dev")

    ## for matplotlib
    sudo("apt-get -y install libpng12-0 libpng12-dev")
    sudo("apt-get -y install libfreetype6 libfreetype6-dev")
    

def setup_worker_02_install_required_yum():
    sudo("yum install readline readline-devel")
    sudo("yum install gcc gcc-c++ make git openssl-devel")
    sudo("yum install bzip2-devel zlib-devel")
    sudo("yum install sqlite-devel")
    sudo("yum install readline readline-devel")

def setup_worker_03_pyenv():
    cd('~')
    run("git clone https://github.com/yyuu/pyenv.git .pyenv")
    run("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.bash_profile")
    run("echo 'export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.bash_profile")
    run("echo 'eval \"$(pyenv init -)\"' >> ~/.bash_profile")


def setup_worker_04_install_pyenv_python(version="2.7.9"):
    run("pyenv install %s" % version)
    run("pyenv rehash")
    run("pyenv global %s" % version)
    run("pyenv rehash")


def setup_worker_05_pythonlib():
    run("pip install numpy")
    run("pip install pymongo")
    run("pip install redis")
    run("pip install PyYAML")
    run("pip install python-mysql")
    run("pip install django")
    run("pip install celery")
    run("pip install django-celery")

    ## needs additional libraries
    run("pip install scipy")

    run("pip install pandas")

    ## needs additional libraries
    run("pip install matplotlib")



def setup_worker_06_mbs(repo="", branch=""):
    if repo == "":
        repo = prompt("MBS repository?: ")
        
    cd('~')
    run("git clone %s message_simulator" % repo)
    if not branch == "":
        cd("message_simulator")
        run("git checkout %s" % branch)
    

def setup_worker_07_worker(repo="", branch=""):
    if repo == "":
        repo = prompt("worker repository?: ")
    
    cd('~')
    run("git clone %s message_simulator_gui" % repo)
    if not branch == "":
        cd("message_simulator_gui")
        run("git checkout %s" % branch)

def setup_worker_10_update_worker(repo_dir=""):
    if repo_dir == "":
        repo_dir = prompt("local repository directory?: ")

    cd(repo_dir)
    run("git pull origin master")

def setup_worker_08_configure_worker(broker_url=""):
    pass

def start_worker():
    cd('~/message_simulator_gui')
    run("celery -A sim_dashboard worker -c 1 -l info")


def deploy_sshkey(ssh_key=""):
    if ssh_key == "":
        ssh_key = prompt("Specify ssh public key file:" )
    
    if files.exists('~/.ssh/id_rsa.pub'):
        return

    put(ssh_key, '~/.ssh/id_rsa.pub')
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
    run('chmod 600 ~/.ssh/authorized_keys')
    

    


