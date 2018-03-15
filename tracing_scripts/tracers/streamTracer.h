#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER streamTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./streamTracer.h"

#if !defined(_streamTracer_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _streamTracer_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    streamTracer,
    test_start_ThenMemcpy_host_to_device,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)
TRACEPOINT_EVENT(
    streamTracer,
    test_end_ThenMemcpy_host_to_device,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)
TRACEPOINT_EVENT(
    streamTracer,
    test_start_ThenMemcpy_device_to_host,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)
TRACEPOINT_EVENT(
    streamTracer,
    test_end_ThenMemcpy_device_to_host,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)

TRACEPOINT_EVENT(
    streamTracer,
    test_start_ThenMemcpy_device_to_device,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)
TRACEPOINT_EVENT(
    streamTracer,
    test_end_ThenMemcpy_device_to_device,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)


/*
GetStatusAsync
RegisterGraphAsync
DeregisterGraphAsync
RunGraphAsync
CleanupGraphAsync
CleanupAllAsync
RecvTensorAsync
LoggingAsync
TracingAsync


GetStatusHandler
CleanupAllHandler
RegisterGraphHandler
DeregisterGraphHandler
RunGraphHandler
RecvTensorHandlerRaw
CleanupGraphHandler
LoggingHandler
TracingHandler
*/




#endif

#include <lttng/tracepoint-event.h>
