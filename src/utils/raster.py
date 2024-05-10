from rasterio import open
from shapely import geometry


def get_tif_metadata(file_name):
    """
    Extract TIF metadata such as bbox, footprint, crs, pixel_size_x and dtype
    """
    with open(file_name) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = geometry.Polygon(
            [
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.top],
                [bounds.right, bounds.bottom],
            ]
        )

        if r.meta["crs"].to_epsg() is None:
            crs = r.meta["crs"].to_string()
        else:
            crs = r.meta["crs"].to_epsg()

        pixel_size_x, _ = r.res
        return (
            bbox,
            geometry.mapping(footprint),
            crs,
            pixel_size_x,
            r.meta["dtype"],
        )
