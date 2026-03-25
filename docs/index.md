<p align="center">
  <img src="./img/logo.png" style="width: 120px; height: 120px; box-shadow: none; -webkit-box-shadow: none" alt="Field"/>
</p>


<div align="center" markdown="1">

### [English](./index.md) \| [Deutsch](./manual.de.md)

</div>

## What is Field Connect?

*Field Connect* is a plugin for [QGIS](https://qgis.org) that establishes a connection with [Field](https://field.idai.world), a documentation software for archaeological field and find recording developed as a cooperation between the German Archaeological Institute ([DAI](https://www.dainst.org)) and the Head Office of the GBV Common Library Network ([VZG](https://www.gbv.de)).

The plugin enables the exchange of data between a [Field Desktop](https://field.idai.world/download) application running on the same computer and a QGIS project. It can also be used to create [GeoPackage](https://www.geopackage.org) files from the data of a Field project.

The user interface of Field Connect is available in German and English.

## Requirements

* QGIS 3.44 or later
* Field Desktop 3.7.0 or later

## How to start

Launch Field Desktop and open the project you wish to work on in QGIS. **Important**: All functionality of Field Connect always works with the project currently open in Field Desktop.

Once the plugin has been installed, you can open the *Field Connect* menu via a new button showing the Field logo ("Connect to Field Desktop") which will appear in the plugins toolbar.

Now enter the synchronization password for your *Field Desktop* installation in the input field *Field Password*. You can find the password by opening the menu "Tools" ➝ "Settings" in Field Desktop (on macOS: "Field Desktop" ➝ "Settings"). In the section "Synchronization", you can view and change the password under "Your password".

You can now establish a connection with the project open in Field Desktop by clicking the button "Connect". Once connected, data can be exchanged between QGIS and Field Desktop via the "Import" and "Export" tabs in the *Field Connect* menu.

## Import

### Settings

* *Categories*: This dropdown menu contains all the categories configured for the project that you are currently connected to. Select one or more categories whose resources you wish to import into the currently open QGIS project. Use the option "Select all" to import all of the resources recorded in the project.
* *CRS*: Select the coordinate reference system in which the geometry data is to be stored. By default, the coordinate reference system specified via the field "EPSG Code" in the project properties of the Field project is selected (menu "Project" ➝ "Properties").
* *Format*: Select the target format in which the data should be saved. The supported formats are:
    * *GeoPackage*: A GeoPackage file is created in which the imported data is saved. When the import starts, a file selection window appears in which you can specify the desired file location.
    * *Temporary*: Temporary layers are created in the currently open QGIS project.
* *Timezone*: Select the timezone in which date information is to be stored in the attribute table. All fields of input type "Date"  that are present in the Field project will be converted to the corresponding timezone. By default, the system timezone of the computer on which QGIS is running is selected. You can restore the default setting using the button *Reset to system timezone* .
* *Options*:
    * *Create layers for all configured geometry types*: If this option is enabled, one layer is created per category for each geometry type configured in Field Desktop for that category, regardless of whether corresponding data is present in the Field project. Otherwise, only layers that contain data are created (see subchapter "Import results").
    * *Combine hierarchical relations*: If this option is enabled, the hierarchical relations "Is recorded in" and "Lies within" are combined into the simplified relation "Is child of". This option should normally remain enabled.

### Start import

Start the import by clicking the button "Import". The progress of the import process is shown by a progress bar in QGIS. The Field Desktop interface is blocked whilst this is taking place.

### Import results

Field Connect creates a new group in the currently open QGIS project with the same name as the Field project, which contains all layers with the imported data. The layers are named according to the scheme "Project identifier_Category identifier_Geometry type" (e.g. "test_Find_Point").

If the option *Create layers for all configured geometry types* is disabled, layers are created only for categories and geometry types for which corresponding data exists in the Field project.

If, however, the option is enabled, the project configuration of the Field project is considered: In Field Desktop, you can select the permitted geometry types for a category’s geometry field via the menu "Tools" ➝ "Project Configuration". Possible geometry types are: "Polygon", "Multipolygon", "Polyline", "Multipolyline", "Point" and "Multipoint". A corresponding layer is created for each of the permitted geometry types. Exception: If a multi-geometry type is permitted, no layer is created for the corresponding single geometry type within this category (e.g. polygons and multipolygons are stored together in a layer named "test_Trench_MultiPolygon").

The category identifier is stored in the variable "field_category" within the user properties of each layer. This variable should **not be deleted**, as it is needed when the layer is exported back to Field Desktop.

During import, Field Connect also reads valuelists, field and value labels as well as description texts from the Field project configuration and saves these in a separate layer with the naming scheme "Project identifier_lookup" (e.g. "test_lookup") . This layer is required for the plugin to function and should **not be deleted**.

Further details on the structure of the attribute table of an imported layer can be found in the chapter "The attribute table".

## Export

### Settings

* *Layer group*: Select the group whose data you wish to export to Field Desktop.
* *Mode*: Select the export mode to determine which data is transferred.
    * *Group*: All data from the selected group will be exported.
    * *Selected Layer(s)*: Only the data from the currently selected layer(s) within the group will be exported.
* *Target CRS*: Select the coordinate reference system in which the geometry data is to be stored in the Field project.
* *Timezone*: Select the timezone in which date values are specified in the attribute table. By default, the system timezone of the computer on which QGIS is running is selected. You can restore the default setting using the button *Reset to system timezone*.
* *Options*:
    * *Export only unsaved features*: If this option is enabled, only newly added or edited features will be exported. For this to work, the relevant layers must be in edit mode and the changes must not yet have been saved. This option can be useful for reducing export time for large projects when only a few changes need to be transferred to an existing Field project.
    * *Save unsaved changes*: If this option is enabled, the relevant layers are saved during export. This option can be particularly useful in combination with the option *Export only unsaved features*.
    * *Ignore unconfigured fields**: If this option is enabled, the export process is not interrupted if fields are found that are not configured in the Field project. Instead, data in unconfigured fields is ignored.
    * *Permit field deletions*: When this option is enabled, fields can not only be edited but also deleted. All fields (including relations) for which the corresponding field in the attribute table is empty will be deleted. Fields not listed in the attribute table remain unchanged.

### Start export

Start the export by clicking the button "Export". The progress of the export process is shown by a progress bar in QGIS. The Field Desktop interface is blocked whilst this is taking place.

### Export results

Newly added features are added to Field Desktop as new resources. Existing resources are updated if data in the attribute table or the geometry has changed.

During export, Field Desktop validates the data in the attribute table. If any invalid data is found, the export is cancelled and a corresponding error message is displayed in QGIS.

**Important**: Resources for which warnings exist in Field Desktop can only be updated via the QGIS export if the export resolves these warnings (for example via changes in the attribute table).

### Notes

#### Structure of the attribute table

It is recommended that you use layers created via the import tool of Field Connect when exporting. If you wish to transfer data from QGIS into a Field project that is still empty, first perform an import using the option *Create layers for all configured geometry types* to generate empty layers for all categories with the corresponding attribute tables. Enter your data into these layers where possible.

Layers you have created yourself must correspond to the layers generated by Field Connect in terms of structure and naming convention of the attribute table (however, not all columns need to be included, and extra columns for further entries in list fields may be added). Furthermore, to ensure that the correct category can be set during export, the category identifier must be entered in a variable named "field_category" that must be created in the layer’s user properties.

#### Handling error messages

If the export fails, this is usually because entries in the attribute table do not match the corresponding data types in the Field project configuration. The error message indicates where the problem lies.

In some cases, however, the export may fail due to data issues that cannot be immediately identified in attribute table. In this case, check whether there are any existing warnings in the project and resolve them using the tools in the warnings menu, which you can access via the "Warnings" icon at the top right of the navigation bar in Field Desktop. Depending on the warning type, the warnings may also be resolved by making changes in the QGIS attribute table and then re-exporting to Field Desktop.

Please also note that, by default, no field data is deleted, not even in subfields (e.g. of fields of the input types "Dating" or "Dimension"). If a field in the attribute table is empty, this does not automatically mean that it will be deleted during export in Field Desktop. In such cases, ensure that the option *Permit field deletions* is enabled – particularly if you wish to delete individual subfields, as otherwise errors may occur.

## The attribute table

The attribute table of an imported layer contains all the fields that can also be filled in using the resource editor in Field Desktop. However, due to the table structure, there are differences in how data is entered: Depending on the input type, more than one column may be required to describe a field.

The field labels listed below refer to the alias set by default in the attribute table of a layer created by Field Connect. The actual field names correspond to the column names that are used in CSV files created by Field Desktop. You can refer to the subchapter "CSV" of the chapter "Import and Export" in the Field Desktop manual for guidance.

### The identifier

The field "Identifier" must always be filled in. **Important**: The identifier is used to assign the feature to the corresponding resource in Field Desktop. If you import a resource from Field Desktop, change the identifier and then export it back to Field Desktop, the existing resource will **not** be updated; instead, an additional resource with the new identifier will be created.

### Valuelist fields

For fields that allow you to select from a list of values, you can choose the relevant value from a dropdown menu or a list of checkboxes (depending on the input type of the field).

### Yes / No fields

For fields of the input type "Yes / No", the values "Yes" and "No" can be selected from a dropdown menu.

### Multilingual fields

If values in different languages can be entered in a field, a separate column is created in the attribute table for each language. The column header displays the name of the language after the field label (e.g. "Description English").

In projects created with older versions of Field Desktop, or as a result of changes to the project configuration, it may happen that a value without a language specification is entered in a multilingual field. In such cases, the text "Unspecified language" is added to the column header in place of the language code.

### Dropdown lists (range)

Fields of the input type "Dropdown list (range)" consist of up to two subfields, for each of which a separate column is created:

* *Value*: The identifier of the selected value; if two values are selected, the first of the two values.
* *End value*: The identifier of the second selected value if two values are selected.

### Date fields

Fields of the input type "Date" consist of up to three subfields, for each of which a separate column is created:

* *Value*: The date specification for a single date; the start date for a date range
* *End value*: The end date for a date range
* *Range?*: Indicates whether the date is a date range. Possible values are: "Yes" (date range), "No" (single date).

The dates are entered in the format "day.month.year" (DD.MM.YYYY). The entries for day and month are optional, so that it is possible to enter only a specific month of a year or a specific year.

In addition, a time specification in the format "hours:minutes" can be entered (separated by a space) if the entry of a time is permitted for the corresponding field in the project configuration.

**Important**: For data imported from Field Desktop, the dates are specified in the timezone selected during import. When exporting to Field Desktop, ensure you select the correct timezone.

### List fields

For fields of the input type "Checkboxes", only a single column is created for the field. The field values can be selected using checkboxes.

For fields of the input types "Dating", "Dimension", "Weight", "Volume", "Bibliographic reference", "Composite field" and "Single line text (List)", the corresponding columns for the respective subfields or languages are created **for each list entry**. A number (starting at 0) is inserted after the field label to identify the respective entry.

### Relations

Each column header begins with "Relation", followed by the label of the relation. The identifiers of the target resources are entered, separated by a semicolon.

In addition to the relations listed in the project configuration in the form of the respective category, the following relations can be used:

* *Parent resource*: Specifies the direct parent resource in the hierarchy; remains empty for top-level resources.
* *Depicts* (image resources only): Links the image to one or more resources.
* *Depicted in* (not for image resources): Links the resource to one or more images.
* *Is map layer of* (only for image resources): Adds the image as a map layer in the context of the resource specified as the target.
* *Has map layer* (not for image resources): Adds one or more images as a map layer in the context of this resource.

To link images to the project or set them up as map layers at project level, enter the project identifier in the column *Relation Depicts* or *Relation Is map layer of*.

### QR codes

In the column "QR code", you can enter a string of characters that uniquely identifies the resource and is to be displayed as a QR code in Field Desktop. This column is only created if QR codes have previously been enabled for the relevant category in the configuration editor.

### Datings

Fields of the input type "Dating" are list fields, each of which can contain several dating entries. A dating consists of the following subfields, for which a separate column is created for each dating:

* *Type*: The dating type. Possible values are: "Period", "Single Year", "Before", "After", "Scientific".
* *Start*: Year specification that is set for the dating type "After" and as the start date for the dating type "Period".
* *End*: Year specification that is set for the dating types "Single Year", "Before", "Scientific", as the end date for the dating type "Period".
* *Margin*: Tolerance margin in years for the dating type "Scientific".
* *Source*: Source of the dating, multilingual text field (one column per language).
* *Is imprecise?*: Cannot be set for the dating type "Scientific". Possible values are: "Yes", "No".
* *Is uncertain?*: Cannot be set for the dating type "Scientific". Possible values are: "Yes", "No".

The year specifications "Start" and "End" consist of two subfields:

* *Dating system*: Possible values are "BCE", "BP" and "CE".
* *Year*: The year.

### Dimensions, weights and volumes

Fields of the input types "Dimension", "Weight" and "Volume" are list fields, each of which can contain several entries. An entry consists of the following subfields, for which a separate column is created for each entry:

* *Value*: The measured numerical value.
* *End value*: The second measured numerical value, if it is a range.
* *Unit*: Possible values are "mm", "cm", "m" (Dimension) / "mg", "g", "kg" (Weight) / "ml", "l" (Volume).
* *As measured by* (Dimension) / *Measurement device* (Weight) / *Measurement technique* (Volume): In each case, a value can optionally be selected from the valuelist configured for the field.
* *Comment*: Multilingual text field (one column per language).
* *Is imprecise?*: Possible values are "Yes", "No"

### Bibliographic references

Fields of the input type "Bibliographic reference" are list fields, each of which can contain several reference entries. An entry consists of the following subfields, for which a separate column (text input) is created for each bibliographic entry:

* *Literature quotation*
* *Zenon ID*
* *DOI*
* *Page*
* *Figure*

### Composite fields

Fields of the input type "Composite field" are list fields, each of which can contain several entries. One column is created per entry for each configured subfield (for multilingual text fields, one column for each language). The display name of the subfield is shown in the column header.

## Limitations

Field Connect allows resources of the category "Image" (and its subcategories) to be imported and exported. However, new resources in these categories cannot be created via the export tool, as they must have an associated image file to be accepted by Field Desktop. The import and export of image files is not included in this version of Field Connect.
