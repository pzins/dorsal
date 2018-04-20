sudo lttng create tensorflow
sudo lttng enable-channel -u mychannel --num-subbuf=1000 --subbuf-size=131072
sudo lttng enable-event -k -a --channel=mychannel
sudo lttng track --kernel --pid=6629

# sudo lttng enable-event --userspace "hsa_runtime:*" --channel=mychannel
# sudo lttng enable-event --userspace "hsaTracer:*" --channel=mychannel
sudo lttng enable-event --userspace "hccTracer:*" --channel=mychannel
sudo lttng enable-event --userspace "hipTracer:*" --channel=mychannel
sudo lttng enable-event --userspace "tensorflowTracer:*" --channel=mychannel
# sudo lttng enable-event --userspace "streamTracer:*" --channel=mychannel
sudo lttng add-context -u -t vtid
sudo lttng start
