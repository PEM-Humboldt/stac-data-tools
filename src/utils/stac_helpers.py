from pystac.extensions.raster import DataType


def map_dtype_to_pystac_datatype(dtype_str: str) -> DataType | None:
    """Map a raster dtype string (e.g., 'uint16', 'float32') to a PySTAC DataType."""
    d = (dtype_str or "").lower()
    if d in ("uint8", "ubyte"):
        return DataType.UINT8
    if d in ("uint16",):
        return DataType.UINT16
    if d in ("uint32",):
        return DataType.UINT32
    if d in ("int16",):
        return DataType.INT16
    if d in ("int32",):
        return DataType.INT32
    if d in ("float32", "float"):
        return DataType.FLOAT32
    if d in ("float64", "double"):
        return DataType.FLOAT64
    return None
