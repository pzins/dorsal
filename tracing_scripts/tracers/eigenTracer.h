#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER eigenTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./eigenTracer.h"

#if !defined(_EIGENTRACER_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _EIGENTRACER_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    eigenTracer,
    schedule_entry,
    TP_ARGS(
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_string(name, my_string_arg)
    )
)
TRACEPOINT_EVENT(
    eigenTracer,
    schedule_exit,
    TP_ARGS(
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_string(name, my_string_arg)
    )
)





#endif

#include <lttng/tracepoint-event.h>
