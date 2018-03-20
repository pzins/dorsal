# script to run on the first computer
# and run
# ssh -A 132.207.72.31 sh run_distrib_remote.sh
# simultaneoulsy in another terminal

sh ~/trace_tensorflow_grpc.sh
cd /home/pierre/Dropbox/dev/distributed/in_model_parallelism/
set -x HIP_PROFILE_API 2
set -x HCC_PROFILE 2
python3 mlp_master.py m
ssh -A 132.207.72.31 "kill -9 (ps -aux | grep mlp_master | grep -v grep | awk '{print \$2}' | head -n1)"
sudo lttng destroy
sudo chown -R pierre:pierre ~/lttng-traces/
python3 ~/sort_events.py
python3 ~/vtid.py
