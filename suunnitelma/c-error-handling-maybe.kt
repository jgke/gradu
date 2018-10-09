dev_priv->perf.metrics_kobj ?: {
    DRM_DEBUG("OA metrics weren't advertised via sysfs\n")
    return -EINVAL
}

props->sample_flags & SAMPLE_OA_REPORT ?: {
    DRM_DEBUG("Only OA report sampling supported\n")
    return -EINVAL
}

dev_priv->perf.oa.ops.init_oa_buffer ?: {
    DRM_DEBUG("OA unit not supported\n")
    return -ENODEV
}

/* ... */

stream->ctx?.let { oa_get_render_ctx_id(stream) } ?: {
    DRM_DEBUG("Invalid context id to filter with\n")
    return it
}

get_oa_config(dev_priv, props->metrics_set, &stream->oa_config)?.let {
    ret = it
    DRM_DEBUG("Invalid OA config id=%i\n", props->metrics_set)
    goto err_config
}

/* ... */

err_config:
stream->ctx?.let { oa_put_render_ctx_id(stream) }

return ret

