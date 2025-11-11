from qgis.core import QgsWkbTypes


GEOJSON_TO_QGIS = {
    "Point": QgsWkbTypes.PointZ,
    "MultiPoint": QgsWkbTypes.MultiPointZ,
    "LineString": QgsWkbTypes.LineStringZ,
    "MultiLineString": QgsWkbTypes.MultiLineStringZ,
    "Polygon": QgsWkbTypes.PolygonZ,
    "MultiPolygon": QgsWkbTypes.MultiPolygonZ,
    "NoGeometry": QgsWkbTypes.NoGeometry
}