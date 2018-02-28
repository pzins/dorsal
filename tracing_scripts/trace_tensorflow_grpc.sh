sudo lttng create tensorflow
sudo lttng enable-event --userspace "hsaTracer:*"
sudo lttng enable-event --userspace "hccTracer:*"
sudo lttng enable-event --userspace "hipTracer:*"
sudo lttng enable-event --userspace "tensorflowTracer:*"
sudo lttng enable-event --userspace "grpcTracer:*"
sudo lttng enable-event -k net_dev_queue
sudo lttng enable-event -k net_if_receive_skb
sudo lttng add-context -u -t vtid
sudo lttng start
