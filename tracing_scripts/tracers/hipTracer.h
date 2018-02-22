#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER hipTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./hipTracer.h"

#if !defined(_hipTracer_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _hipTracer_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    hipTracer,
    function_entry,
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
    hipTracer,
    function_exit,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
    )
)





#endif

#include <lttng/tracepoint-event.h>
