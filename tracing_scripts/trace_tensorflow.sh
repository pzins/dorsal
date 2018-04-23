lttng create tensorflow
lttng enable-channel -u mychannel --num-subbuf=1000 --subbuf-size=131072
lttng enable-event --userspace "hsa_runtime:*" --channel=mychannel
lttng enable-event --userspace "hsaTracer:*" --channel=mychannel
lttng enable-event --userspace "hcTracer:*" --channel=mychannel
lttng enable-event --userspace "hipTracer:*" --channel=mychannel
lttng enable-event --userspace "tensorflowTracer:*" --channel=mychannel
lttng enable-event --userspace "streamTracer:*" --channel=mychannel
lttng add-context -u -t vtid
lttng start


# sudo lttng create tensorflow
# sudo lttng enable-event -k -a
# sudo lttng enable-event --userspace "hsa_runtime:*"
# sudo lttng enable-event --userspace "hsaTracer:*"
# sudo lttng enable-event --userspace "hcTracer:*"
# sudo lttng enable-event --userspace "hipTracer:*"
# sudo lttng enable-event --userspace "tensorflowTracer:*"
# sudo lttng enable-event --userspace "streamTracer:*"
# sudo lttng add-context -u -t vtid
# sudo lttng start
