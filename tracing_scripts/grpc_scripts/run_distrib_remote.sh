sh ~/trace_tensorflow_grpc.sh
cd /home/pierre/Dropbox/dev/distributed/in_model_parallelism/
set -x HIP_PROFILE_API 2
set -x HCC_PROFILE 2
python3 mlp_master.py w
sudo lttng destroy
sudo chown -R pierre:pierre ~/lttng-traces
python3 ~/sort_events_second.py
python3 ~/vtid_second.py
scp -r ~/remote_traces 132.207.72.22:~/
scp -r ~/lttng-traces/$(ls -t ~/lttng-traces/ | head -n1) 132.207.72.22:~/
