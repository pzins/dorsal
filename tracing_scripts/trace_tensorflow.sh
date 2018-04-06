lttng create tensorflow
lttng enable-event --userspace "hsa_runtime:*"
lttng enable-event --userspace "hsaTracer:*"
# lttng enable-event --userspace "hccTracer:*"
lttng enable-event --userspace "hipTracer:*"
lttng enable-event --userspace "tensorflowTracer:*"
lttng enable-event --userspace "streamTracer:*"
lttng add-context -u -t vtid
lttng start


# sudo lttng create tensorflow
# sudo lttng enable-event -k -a
# sudo lttng enable-event --userspace "hsa_runtime:*"
# sudo lttng enable-event --userspace "hsaTracer:*"
# sudo lttng enable-event --userspace "hccTracer:*"
# sudo lttng enable-event --userspace "hipTracer:*"
# sudo lttng enable-event --userspace "tensorflowTracer:*"
# sudo lttng enable-event --userspace "streamTracer:*"
# sudo lttng add-context -u -t vtid
# sudo lttng start
