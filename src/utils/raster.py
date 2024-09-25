import rasterio
import os
from shapely.geometry import Polygon, mapping
from osgeo import gdal



def get_tif_metadata(file_name):
    """
    Extract TIF metadata such as bbox, footprint, crs, pixel_size_x and dtype
    """
    with rasterio.open(file_name) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon(
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
            mapping(footprint),
            crs,
            pixel_size_x,
            r.meta["dtype"],
        )


def tif_to_cog(input_file, input_dir, output_dir):
    """
    Convert layer from TIF to COG format
    """
    cog_options = [
        "COMPRESS=DEFLATE",
        "BLOCKSIZE=512",
        "OVERVIEWS=IGNORE_EXISTING",
    ]

    layer = gdal.Open("{}/{}".format(input_dir, input_file), gdal.GA_ReadOnly)
    output_path = "{}/{}".format(output_dir, input_file)

    if not layer:
        raise RuntimeError("Error al leer el archivo: {}".format(input_file))

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        gdal.Translate(
            output_path, layer, format="COG", creationOptions=cog_options
        )

        # This check exists because if the conversion fails no error is shown.
        if not os.path.exists(output_path):
            raise RuntimeError(
                "No fue posible convertir el archivo a formato COG."
            )

        return output_path
    except Exception as e:
        raise RuntimeError(
            "Error al convertir el archivo: {}. Detalle: {}".format(
                input_file, e
            )
        )
