from fabric.api import run, sudo, cd, lcd, local, put, prompt

def deploy_worker(repo=""):
    if repo == "":
        repo = prompt("worker repository?: ")
    
    cd('~')
    run("git clone %s" % repo)

def start_worker():
    cd('~')
    run("celery")


def deploy_sshkey(ssh_key=""):
    if ssh_key == "":
        ssh_key = prompt("Specify ssh public key file:" )
    
    put(ssh_key, '~/.ssh/id_rsa.pub')
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
    run('chmod 600 ~/.ssh/authorized_keys')
    




