sudo lttng create tensorflow
sudo lttng enable-event --userspace "hsaTracer:*"
sudo lttng enable-event --userspace "hccTracer:*"
sudo lttng enable-event --userspace "hipTracer:*"
sudo lttng enable-event --userspace "tensorflowTracer:*"
sudo lttng enable-event --userspace "streamTracer:*"
sudo lttng enable-event --python my-begin-logger
sudo lttng enable-event --python my-end-logger
sudo lttng add-context -u -t vtid
sudo lttng start
