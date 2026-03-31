# LinDelInt ArgDigest Configuration

ARGUMENT_DIGESTERS = {
    "points": {
        "kind": "std",
        "rules": ["is_ndarray", "is_float"],
    },
    "properties": {
        "kind": "std",
        "rules": ["is_ndarray"],
    },
}
