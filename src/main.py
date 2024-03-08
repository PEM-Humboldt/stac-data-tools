import pystac
import json
import argparse
import os
import utils
from datetime import datetime, timedelta
from urllib import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--app_host",
        dest="app_host",
        help="STAC server host",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--catalog_folder",
        dest="catalog_folder",
        help="Catalog Folder",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--catalog_file",
        dest="catalog_file",
        help="Catalog File",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--collection_name",
        dest="collection_name",
        help="Collection Name",
        required=True,
    )

    args = parser.parse_args()

    items, dates, longs, lats, extra_fields = load_layers(args)
    lp_collection = create_collection(args, dates, longs, lats, extra_fields)
    create_items(args, items, lp_collection)


def load_layers(args):
    """
    Read a json file with information about a collection an features
    Convert TIF files to COG and upload them to Azure Blob Storage
    Extract information to create STAC collection an items
    """
    catalog_folder = "input/" + args.catalog_folder
    catalog_file = args.catalog_file
    cog_folder = "output/cog"

    items = []
    dates = []
    longs = []
    lats = []
    extra_fields = []

    if os.path.exists(catalog_folder) and catalog_file in os.listdir(
        catalog_folder
    ):
        catalog_data = json.load(
            open(os.path.join(catalog_folder, catalog_file))
        )

        for (
            feature_key,
            feature_value,
        ) in catalog_data["features"].items():
            item_data = {}
            item_data["id"] = feature_value["id"]

            if "assets" in feature_value:
                for (
                    asset_key,
                    asset_value,
                ) in feature_value["assets"].items():
                    if "href" in asset_value:
                        item_data["full_filename"] = asset_value["href"]
                        # Convertir de tif a cog
                        utils.tif_to_cog(
                            os.path.join(
                                catalog_folder,
                                item_data["full_filename"],
                            ),
                            item_data["full_filename"],
                            cog_folder,
                        )
                        # Cargar a azure
                        item_data["hrefFull"] = utils.up_to_blobstorage(
                            item_data["full_filename"],
                            os.path.join(
                                catalog_folder,
                                cog_folder,
                            ),
                        )

                        # Extraer metadatos del item
                        (
                            item_data["bbox"],
                            item_data["footprint"],
                            item_data["crs"],
                            item_data["resolution"],
                            item_data["dtype"],
                        ) = utils.get_tif_metadata(
                            os.path.join(
                                catalog_folder,
                                cog_folder,
                                item_data["full_filename"],
                            )
                        )
                        item_data["years"] = asset_value["classes"][
                            "period_layer"
                        ][0]
                        item_data["description"] = (
                            "Forest cover for Colombia for year(s) "
                            + asset_value["classes"]["period_layer"][0]
                        )

                        item_dates = asset_value["classes"]["period_layer"][
                            0
                        ].split("-")
                        item_data["datetime"] = datetime(
                            int(item_dates[1]) + 1,
                            1,
                            1,
                        ) - timedelta(days=1)
                        items.append(item_data)

                        extra_fields = asset_value["classes"]
                        dates.append(item_dates[0])
                        dates.append(item_dates[1])
                        longs.append(item_data["bbox"][0])
                        longs.append(item_data["bbox"][2])
                        lats.append(item_data["bbox"][1])
                        lats.append(item_data["bbox"][3])
                    else:
                        print("la capa no contiene el atributo href.")
    return items, dates, longs, lats, extra_fields


def create_collection(args, dates, longs, lats, extra_fields):
    """
    Set the parameters and create an initial collection
    """
    collection_name = args.collection_name

    bboxes = [
        min(longs),
        min(lats),
        max(longs),
        max(lats),
    ]
    spatial_extent = pystac.SpatialExtent(bboxes=[bboxes])
    temporal_extent = pystac.TemporalExtent(
        intervals=[
            [
                datetime(int(min(dates)), 1, 1),
                datetime(int(max(dates)) + 1, 1, 1) - timedelta(days=1),
            ]
        ]
    )

    lp_collection = pystac.Collection(
        id=collection_name,
        title="Time series of the binary presence of forests in Colombia",
        description="Time series of the presence of forests in Colombia",
        extent=pystac.Extent(
            spatial=spatial_extent,
            temporal=temporal_extent,
        ),
        license="CC-BY-SA-4.0",
        href=collection_name,
        extra_fields=extra_fields,
    )

    # Put collection in server
    utils.post_or_put(
        parse.urljoin(args.app_host, "/collections"),
        lp_collection.to_dict(),
    )

    return lp_collection


def create_items(args, items, lp_collection):
    """
    Create items an upload to collection
    """
    for item_data in items:
        item = pystac.Item(
            id=item_data["id"],
            geometry=item_data["footprint"],
            bbox=item_data["bbox"],
            datetime=item_data["datetime"],
            properties={
                "full_filename": item_data["full_filename"],
                "description": item_data["description"],
                "years": item_data["years"],
            },
            collection=lp_collection,
        )
        item.add_asset(
            key=item_data["id"],
            asset=pystac.Asset(
                href=item_data["hrefFull"],
                media_type=pystac.MediaType.COG,
            ),
        )
        item.set_self_href("./" + item_data["full_filename"])

        utils.post_or_put(
            f"{args.app_host}collections/{item.to_dict()['collection']}/items",
            item.to_dict(),
        )
    else:
        print("El directorio no existe o no contiene el archivo catalog.json.")


if __name__ == "__main__":
    main()
