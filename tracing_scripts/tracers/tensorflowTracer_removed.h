TRACEPOINT_EVENT(
    tensorflowTracer,
    allocate_chunk_entry,
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
    tensorflowTracer,
    allocate_chunk_exit,
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
    tensorflowTracer,
    allocate_raw_internal,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        const char*, alloc_name_arg,
        const char*, ptr_arg,
        int, num_bytes_arg,
        int, rounded_bytes_arg,
        int, bin_num_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_string(alloc_name, alloc_name_arg)
        ctf_string(ptr, ptr_arg)
        ctf_integer(int, num_bytes, num_bytes_arg)
        ctf_integer(int, rounded_bytes, rounded_bytes_arg)
        ctf_integer(int, bin_num, bin_num_arg)
    )
)

TRACEPOINT_EVENT(
    tensorflowTracer,
    deallocate_raw_internal,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        const char*, alloc_name_arg,
        const char*, ptr_arg,
        int, num_bytes_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_string(alloc_name, alloc_name_arg)
        ctf_string(ptr, ptr_arg)
        ctf_integer(int, num_bytes, num_bytes_arg)
    )
)


TRACEPOINT_EVENT(
    tensorflowTracer,
    do_create_entry,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        const char*, container_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_string(container, container_arg)
    )
)
TRACEPOINT_EVENT(
    tensorflowTracer,
    do_create_exit,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        const char*, container_arg,
        int, success_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_string(container, container_arg)
        ctf_integer(int, success, success_arg)
    )
)

TRACEPOINT_EVENT(
    tensorflowTracer,
    cleanup_entry,
    TP_ARGS(
        const char*, cat_arg,
        const char*, container_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, container_arg)
    )
)
TRACEPOINT_EVENT(
    tensorflowTracer,
    cleanup_exit,
    TP_ARGS(
        const char*, cat_arg,
        const char*, container_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, container_arg)
    )
)

TRACEPOINT_EVENT(
    tensorflowTracer,
    gpu_bfc_alloc_entry,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        uint64_t, num_bytes_arg,
        int, alignment_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, num_bytes, num_bytes_arg)
        ctf_integer(int, alignment, alignment_arg)
    )
)
TRACEPOINT_EVENT(
    tensorflowTracer,
    gpu_bfc_alloc_exit,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        uint64_t, num_bytes_arg,
        int, alignment_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_integer(uint64_t, num_bytes, num_bytes_arg)
        ctf_integer(int, alignment, alignment_arg)
    )
)

TRACEPOINT_EVENT(
    tensorflowTracer,
    gpu_bfc_free_entry,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        uint64_t, num_bytes_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_integer(int64_t, num_bytes, num_bytes_arg)
    )
)
TRACEPOINT_EVENT(
    tensorflowTracer,
    gpu_bfc_free_exit,
    TP_ARGS(
        const char*, cat_arg,
        const char*, name_arg,
        uint64_t, num_bytes_arg
    ),
    TP_FIELDS(
        ctf_string(cat, cat_arg)
        ctf_string(name, name_arg)
        ctf_integer(int64_t, num_bytes, num_bytes_arg)
    )
)