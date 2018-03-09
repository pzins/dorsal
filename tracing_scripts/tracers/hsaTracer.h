#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER hsaTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./hsaTracer.h"

#if !defined(_hsaTRACER_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _hsaTRACER_H

#include <lttng/tracepoint.h>
TRACEPOINT_EVENT(
	hsaTracer,
	function_entry,
	TP_ARGS(
		const char*, cat_arg,
		char*, name
	),
	TP_FIELDS(
		ctf_string(cat, cat_arg)
		ctf_string(name, name)
	)
)

TRACEPOINT_EVENT(
    hsaTracer,
	function_exit,
	TP_ARGS(
		const char*, cat_arg,
		char*, name
	),
	TP_FIELDS(
		ctf_string(cat, cat_arg)
		ctf_string(name, name)
	)
)

TRACEPOINT_EVENT(
	hsaTracer,
	pool_memory_allocate,
	TP_ARGS(
		uint64_t, handle_arg,
		uint64_t, ptr_arg,
		uint64_t, size_arg
	),
	TP_FIELDS(
		ctf_integer(uint64_t, handle, handle_arg)
		ctf_integer(uint64_t, ptr, ptr_arg)
		ctf_integer(uint64_t, size, size_arg)
	)
)

TRACEPOINT_EVENT(
	hsaTracer,
	pool_memory_free,
	TP_ARGS(
		uint64_t, handle_arg,
		uint64_t, ptr_arg,
		uint64_t, size_arg
	),
	TP_FIELDS(
		ctf_integer(uint64_t, handle, handle_arg)
		ctf_integer(uint64_t, ptr, ptr_arg)
		ctf_integer(uint64_t, size, size_arg)
	)
)

#endif

#include <lttng/tracepoint-event.h>
