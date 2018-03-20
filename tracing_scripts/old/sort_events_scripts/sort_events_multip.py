#!/usr/bin/python3
import babeltrace
import babeltrace.reader as btr
import babeltrace.writer as btw
import sys
# from tracing_events_classes import event_classes
from collections import defaultdict
import time
import os
from collections import defaultdict
import threading
import copy
# from multiprocessing import Process, Manager
# from pathos.multiprocessing import Process, Manager
# from pathos.multiprocessing import ProcessingPool as Pool
from multiprocess import Process, Queue, Manager

# *************************

# Create field declarations
# Field declarations
uint64_fd = btw.IntegerFieldDeclaration(64)
uint64_fd.signed = False

int64_fd = btw.IntegerFieldDeclaration(64)
int64_fd.signed = True

uint32_fd = btw.IntegerFieldDeclaration(32)
uint32_fd.signed = False

int32_fd = btw.IntegerFieldDeclaration(32)
int32_fd.signed = True

float_fd = btw.FloatingPointFieldDeclaration()

huint64_fd = btw.IntegerFieldDeclaration(64)
huint64_fd.base = babeltrace.writer.IntegerBase.HEX
huint64_fd.signed = False

string_fd = btw.StringFieldDeclaration()

dim_array_fd = btw.ArrayFieldDeclaration(uint32_fd, 3)
# Create event classes
event_classes = {}

# hsaTracer
event_classes['hsaTracer:function_entry'] = btw.EventClass('hsaTracer:function_entry')
event_classes['hsaTracer:function_entry'].add_field(string_fd, 'cat')
event_classes['hsaTracer:function_entry'].add_field(string_fd, 'name')
event_classes['hsaTracer:function_exit'] = btw.EventClass('hsaTracer:function_exit')
event_classes['hsaTracer:function_exit'].add_field(string_fd, 'cat')
event_classes['hsaTracer:function_exit'].add_field(string_fd, 'name')

# hipTracer
event_classes['hipTracer:function_entry'] = btw.EventClass('hipTracer:function_entry')
event_classes['hipTracer:function_entry'].add_field(string_fd, 'cat')
event_classes['hipTracer:function_entry'].add_field(string_fd, 'name')
event_classes['hipTracer:function_exit'] = btw.EventClass('hipTracer:function_exit')
event_classes['hipTracer:function_exit'].add_field(string_fd, 'cat')
event_classes['hipTracer:function_exit'].add_field(string_fd, 'name')

# grpcTracer
event_classes['grpcTracer:receive_request'] = btw.EventClass('grpcTracer:receive_request')
event_classes['grpcTracer:receive_request'].add_field(string_fd, 'name')
event_classes['grpcTracer:send_request'] = btw.EventClass('grpcTracer:send_request')
event_classes['grpcTracer:send_request'].add_field(string_fd, 'name')

event_classes['grpcTracer:receive_RecvTensor_request'] = btw.EventClass('grpcTracer:receive_RecvTensor_request')
event_classes['grpcTracer:receive_RecvTensor_request'].add_field(string_fd, 'cat')
event_classes['grpcTracer:receive_RecvTensor_request'].add_field(string_fd, 'name')
event_classes['grpcTracer:receive_RecvTensor_request'].add_field(string_fd, 'rendezvous_key')
event_classes['grpcTracer:receive_RecvTensor_request'].add_field(uint64_fd, 'step_id')
event_classes['grpcTracer:receive_RecvTensor_request'].add_field(uint32_fd, 'bus_id')
event_classes['grpcTracer:send_RecvTensor_request'] = btw.EventClass('grpcTracer:send_RecvTensor_request')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'cat')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'name')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'rendezvous_key')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'tensor')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'src_device')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'dst_device')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'request')
event_classes['grpcTracer:send_RecvTensor_request'].add_field(string_fd, 'response')



# hccTracer
event_classes['hccTracer:kernel_begin'] = btw.EventClass('hccTracer:kernel_begin')
event_classes['hccTracer:kernel_begin'].add_field(string_fd, 'cat')
event_classes['hccTracer:kernel_begin'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:kernel_begin'].add_field(string_fd, 'name')
event_classes['hccTracer:kernel_begin'].add_field(string_fd, 'long_name')
event_classes['hccTracer:kernel_begin'].add_field(dim_array_fd, 'workgroup_size')
event_classes['hccTracer:kernel_begin'].add_field(dim_array_fd, 'grid_size')
event_classes['hccTracer:kernel_begin'].add_field(uint32_fd, 'static_group_segment_size')
event_classes['hccTracer:kernel_begin'].add_field(uint32_fd, 'private_segment_size')
event_classes['hccTracer:kernel_begin'].add_field(uint32_fd, 'workitem_vgpr_count')

event_classes['hccTracer:kernel_end'] = btw.EventClass('hccTracer:kernel_end')
event_classes['hccTracer:kernel_end'].add_field(string_fd, 'cat')
event_classes['hccTracer:kernel_end'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:kernel_end'].add_field(string_fd, 'name')
event_classes['hccTracer:kernel_end'].add_field(string_fd, 'long_name')
event_classes['hccTracer:kernel_end'].add_field(dim_array_fd, 'workgroup_size')
event_classes['hccTracer:kernel_end'].add_field(dim_array_fd, 'grid_size')
event_classes['hccTracer:kernel_end'].add_field(uint32_fd, 'static_group_segment_size')
event_classes['hccTracer:kernel_end'].add_field(uint32_fd, 'private_segment_size')
event_classes['hccTracer:kernel_end'].add_field(uint32_fd, 'workitem_vgpr_count')

event_classes['hccTracer:unpinned_memory_engine_copy_entry'] = btw.EventClass('hccTracer:unpinned_memory_engine_copy_entry')
event_classes['hccTracer:unpinned_memory_engine_copy_entry'].add_field(string_fd, 'cat')
event_classes['hccTracer:unpinned_memory_engine_copy_entry'].add_field(string_fd, 'name')
event_classes['hccTracer:unpinned_memory_engine_copy_entry'].add_field(int64_fd, 'size_bytes')
event_classes['hccTracer:unpinned_memory_engine_copy_exit'] = btw.EventClass('hccTracer:unpinned_memory_engine_copy_exit')
event_classes['hccTracer:unpinned_memory_engine_copy_exit'].add_field(string_fd, 'cat')
event_classes['hccTracer:unpinned_memory_engine_copy_exit'].add_field(string_fd, 'name')
event_classes['hccTracer:unpinned_memory_engine_copy_exit'].add_field(int64_fd, 'size_bytes')

event_classes['hccTracer:async_memcpy_begin'] = btw.EventClass('hccTracer:async_memcpy_begin')
event_classes['hccTracer:async_memcpy_begin'].add_field(string_fd, 'cat')
event_classes['hccTracer:async_memcpy_begin'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:async_memcpy_begin'].add_field(string_fd, 'name')
event_classes['hccTracer:async_memcpy_begin'].add_field(int64_fd, 'size_bytes')
event_classes['hccTracer:async_memcpy_begin'].add_field(float_fd, 'size_megabytes')
event_classes['hccTracer:async_memcpy_begin'].add_field(float_fd, 'throughput')
event_classes['hccTracer:async_memcpy_begin'].add_field(uint32_fd, 'isAsync')
event_classes['hccTracer:async_memcpy_begin'].add_field(uint32_fd, 'isSingleStepCopy')
event_classes['hccTracer:async_memcpy_begin'].add_field(uint32_fd, 'isPeerToPeer')
event_classes['hccTracer:async_memcpy_begin'].add_field(uint32_fd, 'isActiveWait')

event_classes['hccTracer:async_memcpy_end'] = btw.EventClass('hccTracer:async_memcpy_end')
event_classes['hccTracer:async_memcpy_end'].add_field(string_fd, 'cat')
event_classes['hccTracer:async_memcpy_end'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:async_memcpy_end'].add_field(string_fd, 'name')
event_classes['hccTracer:async_memcpy_end'].add_field(int64_fd, 'size_bytes')
event_classes['hccTracer:async_memcpy_end'].add_field(float_fd, 'size_megabytes')
event_classes['hccTracer:async_memcpy_end'].add_field(float_fd, 'throughput')
event_classes['hccTracer:async_memcpy_end'].add_field(uint32_fd, 'isAsync')
event_classes['hccTracer:async_memcpy_end'].add_field(uint32_fd, 'isSingleStepCopy')
event_classes['hccTracer:async_memcpy_end'].add_field(uint32_fd, 'isPeerToPeer')
event_classes['hccTracer:async_memcpy_end'].add_field(uint32_fd, 'isActiveWait')

event_classes['hccTracer:async_memcpyslo_begin'] = btw.EventClass('hccTracer:async_memcpy_begin')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(string_fd, 'cat')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(string_fd, 'name')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(int64_fd, 'size_bytes')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(float_fd, 'size_megabytes')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(float_fd, 'throughput')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(uint32_fd, 'isAsync')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(uint32_fd, 'isSingleStepCopy')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(uint32_fd, 'isPeerToPeer')
event_classes['hccTracer:async_memcpyslo_begin'].add_field(uint32_fd, 'isActiveWait')

event_classes['hccTracer:async_memcpyslo_end'] = btw.EventClass('hccTracer:async_memcpy_end')
event_classes['hccTracer:async_memcpyslo_end'].add_field(string_fd, 'cat')
event_classes['hccTracer:async_memcpyslo_end'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:async_memcpyslo_end'].add_field(string_fd, 'name')
event_classes['hccTracer:async_memcpyslo_end'].add_field(int64_fd, 'size_bytes')
event_classes['hccTracer:async_memcpyslo_end'].add_field(float_fd, 'size_megabytes')
event_classes['hccTracer:async_memcpyslo_end'].add_field(float_fd, 'throughput')
event_classes['hccTracer:async_memcpyslo_end'].add_field(uint32_fd, 'isAsync')
event_classes['hccTracer:async_memcpyslo_end'].add_field(uint32_fd, 'isSingleStepCopy')
event_classes['hccTracer:async_memcpyslo_end'].add_field(uint32_fd, 'isPeerToPeer')
event_classes['hccTracer:async_memcpyslo_end'].add_field(uint32_fd, 'isActiveWait')


event_classes['hccTracer:barrier_begin'] = btw.EventClass('hccTracer:barrier_begin')
event_classes['hccTracer:barrier_begin'].add_field(string_fd, 'cat')
event_classes['hccTracer:barrier_begin'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:barrier_begin'].add_field(string_fd, 'name')
event_classes['hccTracer:barrier_begin'].add_field(uint32_fd, 'dep_count')
event_classes['hccTracer:barrier_begin'].add_field(uint32_fd, 'acquire')
event_classes['hccTracer:barrier_begin'].add_field(uint32_fd, 'release')

event_classes['hccTracer:barrier_end'] = btw.EventClass('hccTracer:barrier_end')
event_classes['hccTracer:barrier_end'].add_field(string_fd, 'cat')
event_classes['hccTracer:barrier_end'].add_field(string_fd, 'name')
event_classes['hccTracer:barrier_end'].add_field(uint64_fd, 'timestamp')
event_classes['hccTracer:barrier_end'].add_field(uint32_fd, 'dep_count')
event_classes['hccTracer:barrier_end'].add_field(uint32_fd, 'acquire')
event_classes['hccTracer:barrier_end'].add_field(uint32_fd, 'release')

# event_classes['hccTracer:aql_packet_submitted'] = btw.EventClass('hccTracer:aql_packet_submitted')
# event_classes['hccTracer:aql_packet_submitted'].add_field(uint64_fd, 'packet_id')
# event_classes['hccTracer:aql_packet_submitted'].add_field(string_fd, 'packet_type')
# event_classes['hccTracer:aql_packet_submitted'].add_field(uint64_fd, 'agent_handle')
# event_classes['hccTracer:aql_packet_submitted'].add_field(uint64_fd, 'queue_id')
#
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'] = btw.EventClass('hccTracer:aql_packet_submitted')
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'].add_field(uint64_fd, 'packet_id')
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'].add_field(uint64_fd, 'agent_handle')
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'].add_field(uint64_fd, 'queue_id')
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'].add_field(uint64_fd, 'kernel_object')
# event_classes['hccTracer:aql_kernel_dispatch_packet_submitted'].add_field(string_fd, 'kernel_name')



# tensorflowTracer

# Tracepoints : entry / exit
event_classes['tensorflowTracer:process_entry'] = btw.EventClass('tensorflowTracer:process_entry')
event_classes['tensorflowTracer:process_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:process_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:process_entry'].add_field(uint64_fd, 'schedule')
event_classes['tensorflowTracer:process_exit'] = btw.EventClass('tensorflowTracer:process_exit')
event_classes['tensorflowTracer:process_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:process_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:process_exit'].add_field(uint64_fd, 'schedule')

event_classes['tensorflowTracer:inline_ready_entry'] = btw.EventClass('tensorflowTracer:inline_ready_entry')
event_classes['tensorflowTracer:inline_ready_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:inline_ready_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:inline_ready_exit'] = btw.EventClass('tensorflowTracer:inline_ready_exit')
event_classes['tensorflowTracer:inline_ready_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:inline_ready_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:push_succ_entry'] = btw.EventClass('tensorflowTracer:push_succ_entry')
event_classes['tensorflowTracer:push_succ_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:push_succ_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:push_succ_exit'] = btw.EventClass('tensorflowTracer:push_succ_exit')
event_classes['tensorflowTracer:push_succ_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:push_succ_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:push_succ_exit'].add_field(uint32_fd, 'is_ready')

event_classes['tensorflowTracer:allocate_chunk_entry'] = btw.EventClass('tensorflowTracer:allocate_chunk_entry')
event_classes['tensorflowTracer:allocate_chunk_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:allocate_chunk_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:allocate_chunk_exit'] = btw.EventClass('tensorflowTracer:allocate_chunk_exit')
event_classes['tensorflowTracer:allocate_chunk_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:allocate_chunk_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:allocate_raw_internal_entry'] = btw.EventClass('tensorflowTracer:allocate_raw_internal_entry')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(string_fd, 'ptr')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(uint32_fd, 'num_bytes')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(uint32_fd, 'rounded_bytes')
event_classes['tensorflowTracer:allocate_raw_internal_entry'].add_field(uint32_fd, 'bin_num')
event_classes['tensorflowTracer:allocate_raw_internal_exit'] = btw.EventClass('tensorflowTracer:allocate_raw_internal_exit')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(string_fd, 'ptr')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(uint32_fd, 'num_bytes')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(uint32_fd, 'rounded_bytes')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(uint32_fd, 'bin_num')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(uint32_fd, 'need_extend')
event_classes['tensorflowTracer:allocate_raw_internal_exit'].add_field(uint32_fd, 'success')

event_classes['tensorflowTracer:deallocate_raw_internal_entry'] = btw.EventClass('tensorflowTracer:deallocate_raw_internal_entry')
event_classes['tensorflowTracer:deallocate_raw_internal_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:deallocate_raw_internal_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:deallocate_raw_internal_entry'].add_field(string_fd, 'ptr')
event_classes['tensorflowTracer:deallocate_raw_internal_entry'].add_field(int32_fd, 'num_bytes')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'] = btw.EventClass('tensorflowTracer:deallocate_raw_internal_exit')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'].add_field(string_fd, 'ptr')
event_classes['tensorflowTracer:deallocate_raw_internal_exit'].add_field(int32_fd, 'num_bytes')

event_classes['tensorflowTracer:do_create_entry'] = btw.EventClass('tensorflowTracer:do_create_entry')
event_classes['tensorflowTracer:do_create_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:do_create_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:do_create_entry'].add_field(string_fd, 'container')
event_classes['tensorflowTracer:do_create_exit'] = btw.EventClass('tensorflowTracer:do_create_exit')
event_classes['tensorflowTracer:do_create_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:do_create_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:do_create_exit'].add_field(string_fd, 'container')
event_classes['tensorflowTracer:do_create_exit'].add_field(uint32_fd, 'success')

event_classes['tensorflowTracer:cleanup_entry'] = btw.EventClass('tensorflowTracer:cleanup_entry')
event_classes['tensorflowTracer:cleanup_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:cleanup_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:cleanup_exit'] = btw.EventClass('tensorflowTracer:cleanup_exit')
event_classes['tensorflowTracer:cleanup_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:cleanup_exit'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:gpu_bfc_alloc_entry'] = btw.EventClass('tensorflowTracer:gpu_bfc_alloc_entry')
event_classes['tensorflowTracer:gpu_bfc_alloc_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:gpu_bfc_alloc_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_bfc_alloc_entry'].add_field(uint32_fd, 'num_bytes')
event_classes['tensorflowTracer:gpu_bfc_alloc_entry'].add_field(uint32_fd, 'alignment')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'] = btw.EventClass('tensorflowTracer:gpu_bfc_alloc_exit')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'].add_field(uint32_fd, 'num_bytes')
event_classes['tensorflowTracer:gpu_bfc_alloc_exit'].add_field(uint32_fd, 'alignment')

event_classes['tensorflowTracer:gpu_bfc_free_entry'] = btw.EventClass('tensorflowTracer:gpu_bfc_free_entry')
event_classes['tensorflowTracer:gpu_bfc_free_entry'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:gpu_bfc_free_entry'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_bfc_free_entry'].add_field(int32_fd, 'num_bytes')
event_classes['tensorflowTracer:gpu_bfc_free_exit'] = btw.EventClass('tensorflowTracer:gpu_bfc_free_exit')
event_classes['tensorflowTracer:gpu_bfc_free_exit'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:gpu_bfc_free_exit'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:gpu_bfc_free_exit'].add_field(int32_fd, 'num_bytes')


# Tracepoints : start / end
event_classes['tensorflowTracer:session_start'] = btw.EventClass('tensorflowTracer:session_start')
event_classes['tensorflowTracer:session_start'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:session_start'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:session_start'].add_field(uint32_fd, 'count')
event_classes['tensorflowTracer:session_end'] = btw.EventClass('tensorflowTracer:session_end')
event_classes['tensorflowTracer:session_end'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:session_end'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:session_end'].add_field(uint32_fd, 'count')

event_classes['tensorflowTracer:operation_start'] = btw.EventClass('tensorflowTracer:operation_start')
event_classes['tensorflowTracer:operation_start'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:operation_start'].add_field(string_fd, 'placement')
event_classes['tensorflowTracer:operation_start'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:operation_end'] = btw.EventClass('tensorflowTracer:operation_end')
event_classes['tensorflowTracer:operation_end'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:operation_end'].add_field(string_fd, 'placement')
event_classes['tensorflowTracer:operation_end'].add_field(string_fd, 'name')

event_classes['tensorflowTracer:async_operation_start'] = btw.EventClass('tensorflowTracer:async_operation_start')
event_classes['tensorflowTracer:async_operation_start'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:async_operation_start'].add_field(string_fd, 'placement')
event_classes['tensorflowTracer:async_operation_start'].add_field(string_fd, 'name')
event_classes['tensorflowTracer:async_operation_end'] = btw.EventClass('tensorflowTracer:async_operation_end')
event_classes['tensorflowTracer:async_operation_end'].add_field(string_fd, 'placement')
event_classes['tensorflowTracer:async_operation_end'].add_field(string_fd, 'cat')
event_classes['tensorflowTracer:async_operation_end'].add_field(string_fd, 'name')


# Tracepoints : XY Charts
event_classes['tensorflowTracer:bfc_allocator_stats'] = btw.EventClass('tensorflowTracer:bfc_allocator_stats')
event_classes['tensorflowTracer:bfc_allocator_stats'].add_field(string_fd, 'allocator_name')
event_classes['tensorflowTracer:bfc_allocator_stats'].add_field(uint64_fd, 'num_allocs')
event_classes['tensorflowTracer:bfc_allocator_stats'].add_field(uint64_fd, 'bytes_in_use')
event_classes['tensorflowTracer:bfc_allocator_stats'].add_field(uint64_fd, 'max_bytes_in_use')
event_classes['tensorflowTracer:bfc_allocator_stats'].add_field(uint64_fd, 'max_alloc_size')

event_classes['tensorflowTracer:gpu_bfc_chunks_stats'] = btw.EventClass('tensorflowTracer:gpu_bfc_chunks_stats')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(string_fd, 'allocator_name')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_bytes_in_use')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_requested_bytes_in_use')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_wasted_bytes_in_use')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_bytes')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_requested_bytes')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_wasted_bytes')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'chunks')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'in_use_chunks')
event_classes['tensorflowTracer:gpu_bfc_chunks_stats'].add_field(uint64_fd, 'free_chunks')

event_classes['tensorflowTracer:cpu_bfc_chunks_stats'] = btw.EventClass('tensorflowTracer:cpu_bfc_chunks_stats')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(string_fd, 'allocator_name')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_bytes_in_use')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_requested_bytes_in_use')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_wasted_bytes_in_use')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_bytes')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_requested_bytes')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'total_wasted_bytes')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'chunks')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'in_use_chunks')
event_classes['tensorflowTracer:cpu_bfc_chunks_stats'].add_field(uint64_fd, 'free_chunks')

event_classes['tensorflowTracer:gpu_bfc_bins_stats'] = btw.EventClass('tensorflowTracer:gpu_bfc_bins_stats')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(string_fd, 'allocator_name')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'bin_numero')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'total_chunks_in_bin')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'total_chunks_in_use')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'total_bytes_in_bin')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'total_bytes_in_use')
event_classes['tensorflowTracer:gpu_bfc_bins_stats'].add_field(uint64_fd, 'total_requested_bytes_in_use')

event_classes['tensorflowTracer:cpu_bfc_bins_stats'] = btw.EventClass('tensorflowTracer:cpu_bfc_bins_stats')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(string_fd, 'allocator_name')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'bin_numero')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'total_chunks_in_bin')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'total_chunks_in_use')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'total_bytes_in_bin')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'total_bytes_in_use')
event_classes['tensorflowTracer:cpu_bfc_bins_stats'].add_field(uint64_fd, 'total_requested_bytes_in_use')

event_classes['lttng_python:event'] = btw.EventClass('lttng_python:event')
event_classes['lttng_python:event'].add_field(string_fd, 'asctime')
event_classes['lttng_python:event'].add_field(string_fd, 'msg')
event_classes['lttng_python:event'].add_field(string_fd, 'logger_name')
event_classes['lttng_python:event'].add_field(string_fd, 'funcName')
event_classes['lttng_python:event'].add_field(uint32_fd, 'lineno')
event_classes['lttng_python:event'].add_field(uint32_fd, 'int_loglevel')
event_classes['lttng_python:event'].add_field(uint64_fd, 'thread')
event_classes['lttng_python:event'].add_field(string_fd, 'threadName')


# cuptiTracer
event_classes['cuptiTracer:runtime_api_entry'] = btw.EventClass('cuptiTracer:runtime_api_entry')
event_classes['cuptiTracer:runtime_api_entry'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:runtime_api_entry'].add_field(string_fd, 'name')
event_classes['cuptiTracer:runtime_api_entry'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:runtime_api_exit'] = btw.EventClass('cuptiTracer:runtime_api_exit')
event_classes['cuptiTracer:runtime_api_exit'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:runtime_api_exit'].add_field(string_fd, 'name')
event_classes['cuptiTracer:runtime_api_exit'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:driver_api_entry'] = btw.EventClass('cuptiTracer:driver_api_entry')
event_classes['cuptiTracer:driver_api_entry'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:driver_api_entry'].add_field(string_fd, 'name')
event_classes['cuptiTracer:driver_api_entry'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:driver_api_exit'] = btw.EventClass('cuptiTracer:driver_api_exit')
event_classes['cuptiTracer:driver_api_exit'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:driver_api_exit'].add_field(string_fd, 'name')
event_classes['cuptiTracer:driver_api_exit'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:kernel_begin'] = btw.EventClass('cuptiTracer:kernel_begin')
event_classes['cuptiTracer:kernel_begin'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:kernel_begin'].add_field(string_fd, 'name')
event_classes['cuptiTracer:kernel_begin'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:kernel_end'] = btw.EventClass('cuptiTracer:kernel_end')
event_classes['cuptiTracer:kernel_end'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:kernel_end'].add_field(string_fd, 'name')
event_classes['cuptiTracer:kernel_end'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:memcpy_begin'] = btw.EventClass('cuptiTracer:memcpy_begin')
event_classes['cuptiTracer:memcpy_begin'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:memcpy_begin'].add_field(string_fd, 'name')
event_classes['cuptiTracer:memcpy_begin'].add_field(string_fd, 'details')
event_classes['cuptiTracer:memcpy_begin'].add_field(uint64_fd, 'timestamp')

event_classes['cuptiTracer:memcpy_end'] = btw.EventClass('cuptiTracer:memcpy_end')
event_classes['cuptiTracer:memcpy_end'].add_field(string_fd, 'cat')
event_classes['cuptiTracer:memcpy_end'].add_field(string_fd, 'name')
event_classes['cuptiTracer:memcpy_end'].add_field(string_fd, 'details')
event_classes['cuptiTracer:memcpy_end'].add_field(uint64_fd, 'timestamp')
#************************

# Add the input trace to the collection
collection = btr.TraceCollection()
directory = "/home/pierre/lttng-traces"
path = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
collection.add_trace(path + "/ust/uid/1000/64-bit", 'ctf')

# Set the output trace
out_path = "/home/pierre/out_traces"
writer = btw.Writer(out_path)

# Clock
clock = btw.Clock('monotonic')
clock.description = 'Monotonic clock from AMD RCP'
writer.add_clock(clock)

# Environment
writer.add_environment_field("hostname", "pierre-tensorflow")
writer.add_environment_field("domain", "ust")
writer.add_environment_field("tracer_name", "lttng-ust")
writer.add_environment_field("tracer_major", 2)
writer.add_environment_field("tracer_minor", 7)

# Create stream class
main_stream_class = btw.StreamClass('main_stream')
main_stream_class.clock = clock

# Create stream
for event_class in event_classes.values():
    main_stream_class.add_event_class(event_class)

start_time = time.time()

NB_THREADS = 4


# cntol = 0
events = [defaultdict(list) for i in range(NB_THREADS)]

# clock_offset = 1518196357777395130 # second computer
clock_offset = 1519939145097366944 # first computer
cnt_incoherent_barrier = 0

all_events = list(collection.events)
length_parts = int(len(all_events) / NB_THREADS)

# def worker1(begin, end, threadNB):
def mysubprocess(all_events_, threadNB, shared_events):
    print("worker", threadNB, "started")
    save_barrier_time = 0
    # for r_event in all_events[begin:end]:
    for r_event in all_events_:
        name = r_event.name
        event_time = r_event.timestamp
        w_event = btw.Event(event_classes[name])

        fields = r_event.field_list_with_scope(babeltrace.common.CTFScope.EVENT_FIELDS)
        w_event = btw.Event(event_classes[name])

        for f in fields:
            # print(name, f, r_event[f])
            # if hccTracer:kernel_* : fill the grid and groupworker arrays
            if f == "workgroup_size" or f == "grid_size":
                for i in range(3):
                    tmp = w_event.payload(f).field(i)
                    tmp.value = r_event[f][i]
                continue
                
            w_event.payload(f).value = r_event[f]

        if "hccTracer:kernel" in name or "hccTracer:async" in name or "hccTracer:barrier" in name:
            event_time = r_event["timestamp"] + clock_offset
            # for the first barrier of the trace, we initialize the varible save_barrier_time
            if save_barrier_time == 0:
                save_barrier_time = r_event["timestamp"]
            if "barrier" in name:
                # if time between last barrier and this barrier time (start or end) we skip it
                if abs(r_event["timestamp"] - save_barrier_time) > 1000000000 * 120:
                    print("barrier incoherent time")
                    cnt_incoherent_barrier += 1
                    continue
                save_barrier_time = r_event["timestamp"]

        # organize threads
        threadId = r_event.field_with_scope("vtid", babeltrace.common.CTFScope.STREAM_EVENT_CONTEXT)
        # if "RecvTensor" in name:
        #     threadId = 1111
        # elif "grpc" in name:
        #     continue
        # do not change vtid
        # events[event_time-1519157918746548549] = [w_event, threadId]

        # if event_time in events:
        #     print("timestamp already exists")
        #     cntol += 1
        
        events[threadNB][event_time].append([w_event, threadId])
        shared_events[event_time] = w_event
        # continue
    print("Worker",threadNB, "finished")

manager = Manager()
shared_events = manager.dict()
processes = []
for i in range(NB_THREADS):
    if i == NB_THREADS-1:
        tmp_events = copy.deepcopy(all_events[length_parts*i:])
        # tmp_events = all_events[length_parts*i:]
    else:
        tmp_events = copy.deepcopy(all_events[length_parts*i:length_parts*(i+1)])
        # tmp_events = all_events[length_parts*i:length_parts*(i+1)]
    p = Process(target=mysubprocess, args=(tmp_events, i, shared_events))
    processes.append(p)
    p.start()
    
for p in processes:
    p.join()
# print shared_dict
for i in events:
    print(len(i))

"""
threads1 = []
for i in range(NB_THREADS):
    if i == NB_THREADS-1:
        tmp_events = copy.deepcopy(all_events[length_parts*i:])
        # tmp_events = all_events[length_parts*i:]
    else:
        tmp_events = copy.deepcopy(all_events[length_parts*i:length_parts*(i+1)])
        # tmp_events = all_events[length_parts*i:length_parts*(i+1)]
    
    t = threading.Thread(target=worker1, args=(tmp_events, i))
    # t = threading.Thread(target=worker1, args=(length_parts*i,len(all_events), i))
    # t = threading.Thread(target=worker1, args=(length_parts*i,length_parts*(i+1), i))
    threads1.append(t)
    t.start()

for t in threads1:
    t.join()
"""
# exit(0)
print(time.time() - start_time)
# input
"""
    if "tensorflowTracer:session" in name or "tensorflowTracer:process" in name or "tensorflowTracer:inline_ready" in name or "tensorflowTracer:push_succ" in name:
        threadId = 1
    elif "operation" in name:
        if "gpu" in r_event["placement"]:
            if "async" not in name:
                threadId = 31
            else:
                threadId = 32
        else:
            if "async" not in name:
                threadId = 21
            else:
                threadId = 22
    elif "hsaTracer" in name:
        threadId = 4
    elif "hipTracer" in name:
        threadId = 5
    elif "hccTracer" in name:
        if "unpinned_memory_engine_copy" in name:
            threadId = 6
        else:
            threadId = 7
    elif "alloc" in name:
        threadId = 8
    elif "tensorflowTracer:do_create" in name or "tensorflowTracer:cleanup" in name:
        threadId = 9
    elif "grpcTracer" in name:
        if "RecvTensor" in name:
            threadId = 98
        elif "GetStatus" in r_event["name"]:
            threadId = 90
        elif "RegisterGraph" in r_event["name"]:
            threadId = 91
        elif "DeregisterGraph" in r_event["name"]:
            threadId = 92
        elif "RunGraph" in r_event["name"]:
            threadId = 93
        elif "CleanupGraph" in r_event["name"]:
            threadId = 94
        elif "CleanupAll" in r_event["name"]:
            threadId = 95
        elif "Logging" in r_event["name"]:
            threadId = 96
        elif "Tracing" in r_event["name"]:
            threadId = 97
        else:
            threadId = 99
    else:
        threadId = 99999

    events[event_time] = [w_event, threadId]
"""
"""
def worker(begin, end): 
    print('Worker')
    main_stream = writer.create_stream(main_stream_class)
    for timestamp in timestamps[begin:end]:
        clock.time = timestamp
        for i in range(len(merged_events[timestamp])):
            ev = merged_events[timestamp][i][0]
            ev.tid(merged_events[timestamp][i][1])
            # print(timestamp)
            main_stream.append_event(ev)
    main_stream.flush()

merged_events = defaultdict(list) 
for i in events:
    merged_events.update(i)
# Append events to the stream
timestamps = list(merged_events.keys())
timestamps.sort()
middle = int(len(timestamps)/NB_THREADS)


threads = []
for i in range(NB_THREADS):
    if i == NB_THREADS-1:
        t = threading.Thread(target=worker, args=(middle*i, len(timestamps)))
    else:
        t = threading.Thread(target=worker, args=(middle*i, middle*(i+1)))
    threads.append(t)
    t.start()

"""