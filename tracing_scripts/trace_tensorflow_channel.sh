lttng create tensorflow
lttng enable-channel -u mychannel --num-subbuf=100 --subbuf-size=16384
lttng enable-event --userspace "hsaTracer:*" --channel=mychannel
lttng enable-event --userspace "hccTracer:*" --channel=mychannel
lttng enable-event --userspace "hipTracer:*" --channel=mychannel
lttng enable-event --userspace "cuptiTracer:*" --channel=mychannel
lttng enable-event --userspace "tensorflowTracer:*" --channel=mychannel
lttng add-context -u -t vtid
lttng start

