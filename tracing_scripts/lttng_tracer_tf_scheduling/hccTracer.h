#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER hccTracer

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./hccTracer.h"

#if !defined(_hccTRACER_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _hccTRACER_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    hccTracer,
    kernel_begin,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    kernel_end,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)


TRACEPOINT_EVENT(
    hccTracer,
    async_memcpy_begin,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    async_memcpy_end,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)

TRACEPOINT_EVENT(
    hccTracer,
    barrier_begin,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    barrier_end,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, my_string_arg)
    )
)

TRACEPOINT_EVENT(
	hccTracer,
	aql_packet_submitted,
	TP_ARGS(
		uint64_t, packet_id,
		const char*, packet_type,
		uint64_t, agent_handle,
		uint64_t, queue_id
	),
	TP_FIELDS(
		ctf_integer(uint64_t, packet_id, packet_id)
		ctf_string(packet_type, packet_type)
		ctf_integer_hex(uint64_t, agent_handle, agent_handle)
		ctf_integer(uint64_t, queue_id, queue_id)
	)
)



TRACEPOINT_EVENT(
	hccTracer,
	aql_kernel_dispatch_packet_submitted,
	TP_ARGS(
		uint64_t, packet_id,
		uint64_t, agent_handle,
		uint64_t, queue_id,
		uint64_t, kernel_object,
		const char*, kernel_name
	),
	TP_FIELDS(
		ctf_integer(uint64_t, packet_id, packet_id)
		ctf_integer_hex(uint64_t, agent_handle, agent_handle)
		ctf_integer(uint64_t, queue_id, queue_id)
		ctf_integer_hex(uint64_t, kernel_object, kernel_object)
		ctf_string(kernel_name, kernel_name)
	)
)

#endif

#include <lttng/tracepoint-event.h>
