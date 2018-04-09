lttng create tensorflow
lttng enable-channel -u mychannel --num-subbuf=1000 --subbuf-size=131072
lttng enable-event --userspace "hsaTracer:*" --channel=mychannel
lttng enable-event --userspace "hccTracer:*" --channel=mychannel
lttng enable-event --userspace "hipTracer:*" --channel=mychannel
# lttng enable-event --userspace "tensorflowTracer:operation_start" --channel=mychannel
# lttng enable-event --userspace "tensorflowTracer:operation_end" --channel=mychannel
# lttng enable-event --userspace "tensorflowTracer:session*" --channel=mychannel
lttng enable-event --userspace "tensorflowTracer:*" --channel=mychannel
lttng enable-event --userspace "cuptiTracer:*" --channel=mychannel
lttng enable-event --userspace "streamTracer:*" --channel=mychannel
lttng add-context -u -t vtid
lttng start
#

# sudo lttng create tensorflow
# sudo lttng enable-channel -u mychannel --num-subbuf=1000 --subbuf-size=131072
# sudo lttng enable-event -k -a
# sudo lttng enable-event --userspace "hsaTracer:*" --channel=mychannel
# sudo lttng enable-event --userspace "hccTracer:*" --channel=mychannel
# sudo lttng enable-event --userspace "hipTracer:*" --channel=mychannel
# sudo lttng enable-event --userspace "tensorflowTracer:operation_start" --channel=mychannel
# sudo lttng enable-event --userspace "tensorflowTracer:operation_end" --channel=mychannel
# sudo lttng enable-event --userspace "tensorflowTracer:session*" --channel=mychannel
# sudo lttng enable-event --userspace "cuptiTracer:*" --channel=mychannel
# sudo lttng enable-event --userspace "streamTracer:*" --channel=mychannel
# sudo lttng add-context -u -t vtid
# sudo lttng start
