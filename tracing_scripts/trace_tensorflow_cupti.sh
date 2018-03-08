lttng create tensorflow
lttng enable-event --userspace "hsaTracer:*"
lttng enable-event --userspace "hccTracer:*"
lttng enable-event --userspace "hipTracer:*"
lttng enable-event --userspace "tensorflowTracer:*"
lttng enable-event --userspace "cuptiTracer:*"
lttng add-context -u -t vtid
lttng start
