from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd, env

computer_1_ip = "192.168.1.3"
computer_1_ip = "132.207.72.22"
computer_2_ip = "192.168.1.5"
computer_2_ip = "132.207.72.31"
tf_program_name = "cnn_distributed"

_HOSTS = [ computer_1_ip, computer_2_ip ] 
env.hosts = computer_1_ip
env.shell = "/usr/bin/fish -l -i -c"

@task
def startTracing():
    run("sh ~/trace_tensorflow_grpc.sh")

@task
@parallel
def runProgramTF():
    path_to_tf_script = "/home/pierre/Dropbox/dev/distributed/in_model_parallelism/"
    with cd(path_to_tf_script):
        if env.host == computer_1_ip:
            with settings(hide('warnings'), warn_only=True):
                run("set -x HIP_PROFILE_API 2; set -x HCC_PROFILE 2; python3 " + tf_program_name + ".py w > /dev/null 2>&1")
        else:
            run("set -x HIP_PROFILE_API 2; set -x HCC_PROFILE 2; python3 " + tf_program_name + ".py m  > /dev/null 2>&1")
            with settings(host_string=computer_2_ip):
                run("kill -SIGKILL (ps -aux | grep " + tf_program_name + " | grep -v grep | awk '{print $2}')")

@task
@parallel
def stopTracing():
    if env.host == computer_2_ip:
        run("sudo lttng destroy; sudo chown -R pierre:pierre ~/lttng-traces/")
        run("python3 ~/sort_events.py")
        run("python3 ~/vtid.py")
    elif env.host == computer_1_ip:
        run("sudo lttng destroy; sudo chown -R pierre:pierre ~/lttng-traces/")
        run("python3 ~/sort_events_second.py")
        run("python3 ~/vtid_second.py")
        run("scp -r ~/remote_traces " + computer_1_ip + ":~/")
        run("scp -r ~/lttng-traces/(ls -t lttng-traces/ | head -n1) " + computer_1_ip + ":~/")

@task
def main():
    with settings(password="pierreol"):
        results = execute(startTracing, hosts=_HOSTS)
        results = execute(runProgramTF, hosts=_HOSTS)
        results = execute(stopTracing, hosts=_HOSTS)


