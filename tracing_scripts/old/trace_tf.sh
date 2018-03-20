lttng create tensorflow
lttng enable-event -u "tensorflowTracer:*"
lttng enable-event  -u "eigenTracer:*"
lttng enable-event -k -a
lttng add-context -u -t vtid
#lttng start

