import os
from tempfile import TemporaryDirectory
from subprocess import check_call, CalledProcessError, STDOUT
from logging import basicConfig, INFO
from rasterio import open
from requests import post, put
from shapely import geometry
from azure import storage
from dotenv import load_dotenv


def run_command(command, work_dir):
    """
    A simple utility to execute a subprocess command.
    """
    try:
        check_call(command, stderr=STDOUT, cwd=work_dir)
    except CalledProcessError as e:
        raise RuntimeError(
            "command '{}' return with error (code {}): {}".format(
                e.cmd, e.returncode, e.output
            )
        )


def check_dir(fname):
    """
    To check if the directory exists
    """
    file_name = fname.split("/")
    rel_path = os.path.join(*file_name[-2:])
    return rel_path


def get_filename(fname, outdir):
    """
    To create a temporary filename to add overviews and convert to COG
    and create a file name just as source but without '.TIF' extension
    """
    rel_path = check_dir(fname)
    out_fname = os.path.join(outdir, rel_path)

    if not os.path.exists(os.path.dirname(out_fname)):
        os.makedirs(os.path.dirname(out_fname))
    return out_fname


def _write_cogtiff(fname, out_fname, outdir):
    """
    Convert the Geotiff to COG using gdal commands
    Blocksize is 512
    TILED <boolean>: Switch to tiled format
    COPY_SRC_OVERVIEWS <boolean>: Force copy of overviews of source dataset
    COMPRESS=[NONE/DEFLATE]: Set the compression to use.
    DEFLATE is only available if NetCDF has been compiled with
              NetCDF-4 support.
              NC4C format is the default if DEFLATE compression is used.
    ZLEVEL=[1-9]: Set the level of compression when using DEFLATE compression.
    A value of 9 is best, and 1 is least compression. The default is 1,
    which offers the best time/compression ratio.
    BLOCKXSIZE <int>: Tile Width
    BLOCKYSIZE <int>: Tile/Strip Height
    PREDICTOR <int>: Predictor Type (1=default, 2=horizontal differencing,
    3=floating point prediction)
    PROFILE <string-select>: possible values: GDALGeoTIFF,GeoTIFF,BASELINE,
    """
    with TemporaryDirectory() as tmpdir:
        temp_fname = os.path.join(tmpdir, os.path.basename(fname))

        env = [
            "GDAL_DISABLE_READDIR_ON_OPEN=YES",
            "CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.tif",
        ]
        check_call(env, shell=True)

        # copy to a tempfolder
        to_cogtif = ["gdal_translate", fname, temp_fname]
        run_command(to_cogtif, tmpdir)

        # Add Overviews
        # gdaladdo - Builds or rebuilds overview images.
        # 2,4,8,16,32 are levels for list of integral overview levels to build.
        add_ovr = [
            "gdaladdo",
            "-r",
            "average",
            "--config",
            "GDAL_TIFF_OVR_BLOCKSIZE",
            "512",
            temp_fname,
            "2",
            "4",
            "8",
            "16",
            "32",
        ]
        run_command(add_ovr, tmpdir)

        # Convert to COG
        cogtif = [
            "gdal_translate",
            "-co",
            "TILED=YES",
            "-co",
            "COPY_SRC_OVERVIEWS=YES",
            "-co",
            "COMPRESS=DEFLATE",
            "-co",
            "ZLEVEL=9",
            "--config",
            "GDAL_TIFF_OVR_BLOCKSIZE",
            "512",
            "-co",
            "BLOCKXSIZE=512",
            "-co",
            "BLOCKYSIZE=512",
            "-co",
            "PREDICTOR=1",
            "-co",
            "PROFILE=GeoTIFF",
            temp_fname,
            out_fname,
        ]
        run_command(cogtif, outdir)


def tif_to_cog(tif_fle, output_file, output_dir):
    """
    Read and convert a TIF file to a COG file
    """
    basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", level=INFO
    )
    output_dir = os.path.abspath(output_dir)
    f_name = os.path.join(os.getcwd(), tif_fle)
    filename = get_filename(output_file, output_dir)
    _write_cogtiff(f_name, filename, output_dir)


def post_or_put(url: str, data: dict):
    """
    Post or put data to url.
    """
    r = post(url, json=data)
    if r.status_code == 409:
        # Exists, so update
        r = put(url, json=data)
        # Unchanged may throw a 404
        if not r.status_code == 404:
            r.raise_for_status()
    else:
        r.raise_for_status()


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


def up_to_blobstorage(file_name, local_folder_path):
    """
    Upload a file to Azure Blob Storage
    """
    load_dotenv()

    # Set the connection string to your Azure Blob Storage account
    connection_string = os.getenv("ABS_STRING")

    # Set the name of the container where you want to upload the files
    container_name = "cog-test"

    # Create a BlobServiceClient object
    blob_client = storage.blob.BlobServiceClient.from_connection_string(
        connection_string
    )

    # Create a ContainerClient object
    container_client = blob_client.get_container_client(container_name)

    local_file_path = os.path.join(local_folder_path, file_name)
    blob_name = os.path.relpath(local_file_path, local_folder_path).replace(
        "\\", "/"
    )

    # Create a BlobClient object for the file
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the file to Azure Blob Storage
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
