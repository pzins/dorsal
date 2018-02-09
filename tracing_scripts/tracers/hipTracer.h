#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER hipTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./hipTracer.h"

#if !defined(_hipTracer_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _hipTracer_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    hipTracer,
    begin,
    TP_ARGS(
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_string(name, my_string_arg)
    )
)
TRACEPOINT_EVENT(
    hipTracer,
    end,
    TP_ARGS(
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_string(name, my_string_arg)
    )
)





#endif

#include <lttng/tracepoint-event.h>
