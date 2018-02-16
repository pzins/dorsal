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
        uint64_t, timestamp_arg,
        const char*, name_arg,
        const char*, long_name_arg,
        int, static_group_segment_size_arg,
        int, private_segment_size_arg,
        int, workitem_vgpr_count_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_string(long_name, long_name_arg)
        ctf_integer(int, static_group_segment_size, static_group_segment_size_arg)
        ctf_integer(int, private_segment_size, private_segment_size_arg)
        ctf_integer(int, workitem_vgpr_count, workitem_vgpr_count_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    kernel_end,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        const char*, long_name_arg,
        int, static_group_segment_size_arg,
        int, private_segment_size_arg,
        int, workitem_vgpr_count_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_string(long_name, long_name_arg)
        ctf_integer(int, static_group_segment_size, static_group_segment_size_arg)
        ctf_integer(int, private_segment_size, private_segment_size_arg)
        ctf_integer(int, workitem_vgpr_count, workitem_vgpr_count_arg)
    )
)


TRACEPOINT_EVENT(
    hccTracer,
    async_memcpy_begin,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        int64_t, size_bytes_arg,
        float, size_megabytes_arg,
        float, throughput_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_integer(int64_t, size_bytes, size_bytes_arg)
        ctf_float(float, size_megabytes, size_megabytes_arg)
        ctf_float(double, throughput, throughput_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    async_memcpy_end,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        int64_t, size_bytes_arg,
        float, size_megabytes_arg,
        float, throughput_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_integer(int64_t, size_bytes, size_bytes_arg)
        ctf_float(float, size_megabytes, size_megabytes_arg)
        ctf_float(double, throughput, throughput_arg)
    )
)

TRACEPOINT_EVENT(
    hccTracer,
    async_memcpyslo_begin,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        int, size_bytes_arg,
        float, size_megabytes_arg,
        float, throughput_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_integer(int, size_bytes, size_bytes_arg)
        ctf_float(float, size_megabytes, size_megabytes_arg)
        ctf_float(double, throughput, throughput_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    async_memcpyslo_end,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        int, size_bytes_arg,
        float, size_megabytes_arg,
        float, throughput_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_integer(int, size_bytes, size_bytes_arg)
        ctf_float(float, size_megabytes, size_megabytes_arg)
        ctf_float(double, throughput, throughput_arg)
    )
)


TRACEPOINT_EVENT(
    hccTracer,
    barrier_begin,
    TP_ARGS(
        uint64_t, timestamp_arg,
        const char*, name_arg,
        int, dep_count_arg,
        int, acquire_arg,
        int, release_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp_arg)
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, dep_count, dep_count_arg)
        ctf_integer(uint64_t, acquire, acquire_arg)
        ctf_integer(uint64_t, release, release_arg)
    )
)

TRACEPOINT_EVENT(
    hccTracer,
    barrier_end,
    TP_ARGS(
        uint64_t, timestamp,
        const char*, name_arg,
        int, dep_count_arg,
        int, acquire_arg,
        int, release_arg
    ),
    TP_FIELDS(
        ctf_integer(uint64_t, timestamp, timestamp)
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, dep_count, dep_count_arg)
        ctf_integer(uint64_t, acquire, acquire_arg)
        ctf_integer(uint64_t, release, release_arg)
    )
)

TRACEPOINT_EVENT(
    hccTracer,
    unpinned_memory_engine_copy_entry,
    TP_ARGS(
        const char*, name_arg,
        uint64_t, size_bytes_arg
    ),
    TP_FIELDS(
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, size_bytes, size_bytes_arg)
    )
)
TRACEPOINT_EVENT(
    hccTracer,
    unpinned_memory_engine_copy_exit,
    TP_ARGS(
        const char*, name_arg,
        uint64_t, size_bytes_arg
    ),
    TP_FIELDS(
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, size_bytes, size_bytes_arg)
    )
)



// no more used, because profiling methods crash
// TRACEPOINT_EVENT(
// 	hccTracer,
// 	aql_packet_submitted,
// 	TP_ARGS(
// 		uint64_t, packet_id,
// 		const char*, packet_type,
// 		uint64_t, agent_handle,
// 		uint64_t, queue_id
// 	),
// 	TP_FIELDS(
// 		ctf_integer(uint64_t, packet_id, packet_id)
// 		ctf_string(packet_type, packet_type)
// 		ctf_integer_hex(uint64_t, agent_handle, agent_handle)
// 		ctf_integer(uint64_t, queue_id, queue_id)
// 	)
// )
// 
// 
// 
// TRACEPOINT_EVENT(
// 	hccTracer,
// 	aql_kernel_dispatch_packet_submitted,
// 	TP_ARGS(
// 		uint64_t, packet_id,
// 		uint64_t, agent_handle,
// 		uint64_t, queue_id,
// 		uint64_t, kernel_object,
// 		const char*, kernel_name
// 	),
// 	TP_FIELDS(
// 		ctf_integer(uint64_t, packet_id, packet_id)
// 		ctf_integer_hex(uint64_t, agent_handle, agent_handle)
// 		ctf_integer(uint64_t, queue_id, queue_id)
// 		ctf_integer_hex(uint64_t, kernel_object, kernel_object)
// 		ctf_string(kernel_name, kernel_name)
// 	)
// )



#endif

#include <lttng/tracepoint-event.h>
