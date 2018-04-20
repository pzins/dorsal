from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd, env

_HOSTS = [ "192.168.1.5", "192.168.1.3" ] 
env.hosts = "192.168.1.5"
env.shell = "/usr/bin/fish -l -i -c"

@task
def startTracing():
    run("sh ~/trace_tensorflow_grpc.sh")

@task
@parallel
def runProgramTF():
    path_to_tf_script = "/home/pierre/Dropbox/dev/distributed/in_model_parallelism/"
    with cd(path_to_tf_script):
        if env.host == "192.168.1.5":
            with settings(hide('warnings'), warn_only=True):
                run("set -x HIP_PROFILE_API 2; set -x HCC_PROFILE 2; python3 cnn_distributed.py w > /dev/null 2>&1")
        else:
            run("set -x HIP_PROFILE_API 2; set -x HCC_PROFILE 2; python3 cnn_distributed.py m  > /dev/null 2>&1")
            with settings(host_string='192.168.1.5'):
                prog_name=  "cnn_distributed"
                run("kill -SIGKILL (ps -aux | grep " + prog_name + " | grep -v grep | awk '{print $2}')")

@task
@parallel
def stopTracing():
    if env.host == "192.168.1.3":
        run("sudo lttng destroy; sudo chown -R pierre:pierre ~/lttng-traces/")
        run("python3 ~/sort_events.py")
        run("python3 ~/vtid.py")
    elif env.host == "192.168.1.5":
        run("sudo lttng destroy; sudo chown -R pierre:pierre ~/lttng-traces/")
        run("python3 ~/sort_events_second.py")
        run("python3 ~/vtid_second.py")
        run("scp -r ~/remote_traces 192.168.1.3:~/")
        run("scp -r ~/lttng-traces/(ls -t lttng-traces/ | head -n1) 192.168.1.3:~/")

@task
def main():
    with settings(password="pierreol"):
        results = execute(startTracing, hosts=_HOSTS)
        results = execute(runProgramTF, hosts=_HOSTS)
        results = execute(stopTracing, hosts=_HOSTS)


