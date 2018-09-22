if (!dev_priv->perf.metrics_kobj) {
    DRM_DEBUG("OA metrics weren't advertised via sysfs\n");
    return -EINVAL;
}

if (!(props->sample_flags & SAMPLE_OA_REPORT)) {
    DRM_DEBUG("Only OA report sampling supported\n");
    return -EINVAL;
}

if (!dev_priv->perf.oa.ops.init_oa_buffer) {
    DRM_DEBUG("OA unit not supported\n");
    return -ENODEV;
}

/* ... */

if (stream->ctx) {
    ret = oa_get_render_ctx_id(stream);
    if (ret) {
        DRM_DEBUG("Invalid context id to filter with\n");
        return ret;
    }
}

ret = get_oa_config(dev_priv, props->metrics_set, &stream->oa_config);
if (ret) {
    DRM_DEBUG("Invalid OA config id=%i\n", props->metrics_set);
    goto err_config;
}

/* ... */

err_config:
if (stream->ctx)
    oa_put_render_ctx_id(stream);

return ret;
