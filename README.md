# Field Connect

Field Connect is a [QGIS](https://qgis.org) plugin that connects QGIS with [Field](https://github.com/dainst/idai-field), a documentation software for archaeological field and find recording developed as a cooperation between the German Archaeological Institute ([DAI](https://www.dainst.org)) and the Head Office of the GBV Common Library Network ([GBV](https://en.gbv.de/)).

The plugin allows importing and exporting data between a [Field Desktop](https://field.idai.world/download) application running on the same computer and a QGIS project. It can also be used to create [GeoPackage](https://www.geopackage.org) files from data recorded in Field Desktop.

*Please note that Field Connect is currently in development and has not yet been released.*

## Features

### Import
* Import data from the project currently open in Field Desktop into a QGIS project either as temporary layers or by saving it as a GeoPackage file.
* Labels for fields and valuelists defined in the project configuration can be optionally added as a layer style definition.

### Export 
* Export data from QGIS layers into the project currently open in Field Desktop.
