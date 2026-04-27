<p align="center">
  <img src="./img/logo.png" style="width: 140px; height: 140px; box-shadow: none; -webkit-box-shadow: none" alt="Field"/>
</p>

<div align="center" markdown="1">

### [English](./index.md) \| [Deutsch](./manual.de.md)

</div>

<br>

## Was ist Field Connect?

*Field Connect* ist ein Plugin für [QGIS](https://qgis.org), das eine Verbindung mit [Field Desktop](https://field.idai.world/download) herstellt, einer Software zur archäologischen Grabungsdokumentation und Funderfassung, die in einer Kooperation zwischen dem Deutschen Archäologischen Institut ([DAI](https://www.dainst.org)) und der Verbundzentrale des Gemeinsamen Bibliotheksverbundes ([VZG](https://www.gbv.de)) entwickelt wird.

Das Plugin ermöglicht den Austausch von Daten zwischen einem QGIS-Projekt und einer auf demselben Computer ausgeführten Installation von Field Desktop. In diesem Zusammenhang kann es außerdem dazu verwendet werden, [GeoPackage](https://www.geopackage.org)-Dateien aus den in Field Desktop aufgenommenen Daten zu erstellen.

Die Benutzeroberfläche von Field Connect ist in den Sprachen Deutsch und Englisch verfügbar.

## Voraussetzungen

* QGIS 3.40 oder aktueller
* Field Desktop 3.7 oder aktueller

## Installation

Field Connect kann aus dem offiziellen QGIS-Erweiterungsrepositorium installiert werden (Menü "Erweiterungen" ➝ "Erweiterungen verwalten und installieren..."). Sollte das Plugin noch nicht in der Liste auftauchen, rufen Sie im Fenster "Erweiterungen" bitte die Funktion "Einstellungen" ➝ "Repositorium neu laden" für das offizielle QGIS-Erweiterungsrepositorium auf.

## Erste Schritte

Rufen Sie Field Desktop auf und öffnen Sie das Projekt, mit dem Sie in QGIS arbeiten möchten. **Wichtig**: Alle Funktionen von Field Connect arbeiten immer mit dem aktuell in Field Desktop geöffneten Projekt.

Nach der Installation des Plugins erscheint in der Erweiterungwerkzeugleiste in QGIS ein neuer Button mit dem Field-Logo (Tooltip: "Mit Field Desktop verbinden"), der das *Field Connect*-Menü öffnet.

Geben Sie nun in das Eingabefeld "Field-Passwort" das Synchronisationspasswort Ihrer *Field Desktop*-Installation ein. Sie finden das Passwort, indem Sie in Field Desktop das Menü "Werkzeuge" ➝ "Einstellungen" (unter macOS: "Field Desktop" ➝ "Einstellungen") aufrufen. Im Abschnitt "Synchronisation" können Sie das Passwort unter "Eigenes Passwort" auslesen und ändern.

Über den Button "Verbinden" können Sie nun eine Verbindung mit dem in Field Desktop geöffneten Projekt herstellen. Bei bestehender Verbindung können über die Tabs "Import" und "Export" im *Field Connect*-Menü Daten zwischen QGIS und Field Desktop ausgetauscht werden.

## Import

### Einstellungen

#### Kategorien

Dieses Auswahlmenü enthält alle Kategorien, die für das Projekt, mit dem Sie sich verbunden haben, konfiguriert sind. Wählen Sie eine oder mehrere Kategorien aus, deren Ressourcen in das aktuell geöffnete QGIS-Projekt importiert werden sollen. Mit der Option "Alle auswählen" können Sie sämtliche Ressourcen des Projekts importieren.

#### CRS

Wählen Sie hier das Koordinatenreferenzsystem aus, in dem die Geometriedaten gespeichert werden sollen. Standardmäßig ausgewählt ist das Koordinatenreferenzsystem, das über das Feld "EPSG-Code" in den Projekteigenschaften des Field-Projekts festgelegt wurde (Menü "Projekt" ➝ "Eigenschaften").

#### Format

Wählen Sie das Zielformat aus, in dem die Daten gespeichert werden sollen. Die unterstützten Formate sind:

* *GeoPackage*: Es wird eine GeoPackage-Datei angelegt, in der die importierten Daten gespeichert werden. Beim Start des Imports erscheint ein Dateiauswahlfenster, in dem Sie den gewünschten Speicherort festlegen können.
* *Temporär*: Es werden temporäre Layer im aktuell geöffneten QGIS-Projekt angelegt.

#### Zeitzone

Wählen Sie hier die Zeitzone aus, in der Datumsangaben in der Attributtabelle gespeichert werden sollen. Alle im Field-Projekt ausgefüllten Felder des Eingabetyps "Datum" werden in die entsprechende Zeitzone umgerechnet. Standardmäßig ist die System-Zeitzone des Computers ausgewählt, auf dem QGIS ausgeführt wird. Mit dem Button "Auf System-Zeitzone zurücksetzen" können Sie die Standardeinstellung wiederherstellen.

#### Optionen

##### Layer für alle konfigurierten Geometrietypen anlegen

Wenn diese Option aktiviert ist, wird pro Kategorie jeweils ein Layer für jeden in Field Desktop für diese Kategorie konfigurierten Geometrietyp angelegt, unanbhängig davon ob im Field-Projekt entsprechende Daten vorhanden sind. Andernfalls werden nur Layer angelegt, für die Daten vorhanden sind (siehe Unterkapitel "Ergebnis des Imports").

##### Hierarchische Relationen zusammenfassen

Wenn diese Option aktiviert ist, werden die hierarchischen Relationen "Aufgenommen in" und "Liegt in" zur vereinfachten Relation "Übergeordnete Ressource" zusammengefasst. Diese Option sollte in der Regel aktiviert bleiben.

### Import starten

Starten Sie den Import über den Button "Import". Der Fortschritt des Importvorgangs wird durch einen Balken in QGIS angezeigt. Die Benutzeroberfläche von Field Desktop ist währenddessen blockiert.

### Ergebnis des Imports

Field Connect legt im aktuell geöffneten QGIS-Projekt eine neue Gruppe mit dem Namen des Field-Projekts an, die alle Layer mit den importierten Daten enthält. Die Layer sind jeweils nach dem Schema "Projektkennung_Kategoriebezeichner_Geometrietyp" benannt (z. B. "test_Fund_Point"). Für Ressourcen ohne Geometrien wird jeweils ein Layer mit Geometrietyp "NoGeometry" angelegt.

Ist die Option "Layer für alle konfigurierten Geometrietypen anlegen" deaktiviert, werden ausschließlich Layer für Kategorien und Geometrietypen angelegt, für die entsprechende Daten im Field-Projekt existieren.

Ist die Option hingegen aktiviert, wird die Projektkonfiguration des Field-Projekts ausgelesen: In Field Desktop können im Menü "Werkzeuge" ➝ "Projektkonfiguration" für das Geometriefeld einer Kategorie die erlaubten Geometrietypen ausgewählt werden. Mögliche Geometrietypen sind: "Polygon", "Multipolygon", "Polyline", "Multipolyline", "Punkt" und "Multipunkt". Für jeden der erlaubten Geometrietypen wird ein entsprechender Layer angelegt. Ausnahme: Ist ein Multi-Geometrietyp erlaubt, wird für diese Kategorie kein Layer für den entsprechenden Einzel-Geometrietyp angelegt (z. B. werden Polygone und Multipolygone gemeinsam in einem Layer "test_Schnitt_MultiPolygon" gespeichert).

In den Benutzereigenschaften jedes Layers wird in der Variable "field_category" der Kategoriebezeichner gespeichert. Diese Variable sollte **nicht gelöscht werden**, da sie beim Export des Layers zurück nach Field Desktop sowie beim Aktualisieren einer bestehenden GeoPackage-Datei benötigt wird.

Field Connect liest beim Import darüber hinaus Wertelisten, Feld- und Wertebezeichnungen sowie Beschreibungstexte aus der Field-Projektkonfiguration aus und speichert diese in einem eigenen Layer mit dem Benennungsschema "Projektkennung_lookup" (z. B. "test_lookup"). Dieser Layer ist erforderlich für die Funktionalität des Plugins und sollte **nicht gelöscht werden**.

Nähere Angaben zum Aufbau der Attributtabelle eines importierten Layers finden Sie im Kapitel "Die Attributtabelle".

### Aktualisierung von GeoPackage-Dateien

Wenn Sie eine bereits existierende GeoPackage-Datei als Ziel des Imports auswählen, so werden die entsprechenden Layer im GeoPackage aktualisiert. Wird für ein Objekt eine Ressource mit dem gleichen Bezeichner in den aus Field Desktop importierten Daten gefunden, gilt:
* In allen Feldern werden die Feldinhalte der Importdaten eingetragen, falls die entsprechenden Felder dort vorhanden sind.
* Felder, die in den Importdaten nicht vorhanden sind, bleiben mit ihren bisherigen Inhalten erhalten.

Objekte, für die keine Ressource in den aus Field Desktop importierten Daten gefunden wird, bleiben unverändert erhalten.

**Wichtig**: Objekte in Geometrie-Layern, die über keine Geometrie verfügen, werden beim Aktualisieren des GeoPackages automatisch in den entsprechenden "NoGeometry"-Layer verschoben. Gibt es noch keinen solchen Layer, so wird er angelegt.

## Export

### Einstellungen

#### Layer-Gruppe

Wählen Sie hier die Gruppe aus, deren Daten Sie nach Field Desktop exportieren möchten.

#### Modus

Wählen Sie hier den Export-Modus aus, der bestimmt, welche Daten übertragen werden.
    
* *Gruppe*: Alle Daten der ausgewählten Gruppe werden exportiert.
* *Ausgewähle(r) Layer*: Ausschließlich die Daten der aktuell selektierten Layer innerhalb der Gruppe werden exportiert.

#### Ziel-CRS

Wählen Sie hier das Koordinatenreferenzsystem aus, in dem die Geometriedaten im Field-Projekt gespeichert werden sollen.

#### Zeitzone

Wählen Sie hier die Zeitzone aus, in der Datumsangaben in der Attributtabelle angegeben sind. Standardmäßig ist die System-Zeitzone des Computers ausgewählt, auf dem QGIS ausgeführt wird. Mit dem Button "Auf System-Zeitzone zurücksetzen" können Sie die Standardeinstellung wiederherstellen.

#### Optionen

##### Nur ungespeicherte Objekte exportieren

Wenn diese Option aktiviert ist, werden ausschließlich neu hinzugefügte oder bearbeitete Objekte exportiert. Dazu müssen sich die entsprechenden Layer im Editierungsmodus befinden und die Änderungen noch nicht gespeichert worden sein. Diese Option kann nützlich sein, um die Exportdauer bei großen Projekten zu verkürzen, wenn lediglich wenige Änderungen in ein bestehendes Field-Projekt übertragen werden sollen.

##### Ungespeicherte Änderungen speichern

Wenn diese Option aktiviert ist, werden die entsprechenden Layer beim Export gespeichert. Diese Option kann insbesondere in Kombination mit der Option "Nur ungespeicherte Objekte exportieren" nützlich sein.

##### Nicht konfigurierte Felder ignorieren

Standardmäßig wird der Exportprozess abgebrochen, sobald Felder gefunden werden, die im Field-Projekt nicht konfiguriert sind. Wenn diese Option aktiviert ist, wird der Export stattdessen vollständig durchgeführt, wobei Daten in unkonfigurierten Feldern ignoriert werden.

##### Löschen von Feldern erlauben

Wenn diese Option aktiviert ist, können Felder nicht nur bearbeitet, sondern auch gelöscht werden. Gelöscht werden alle Felder (inklusive Relationen), für die das entsprechende Feld in der Attributtabelle leer ist. Nicht in der Attributtabelle gelistete Felder bleiben unverändert.

### Export starten

Starten Sie den Export über den Button "Export". Der Fortschritt des Exportvorgangs wird durch einen Balken in QGIS angezeigt. Die Benutzeroberfläche von Field Desktop ist währenddessen blockiert.

### Ergebnis des Exports

In QGIS neu hinzugefügte Objekte werden in Field Desktop als neue Ressourcen ergänzt. Bereits existierende Ressourcen werden aktualisiert, falls sich Daten in der Attributtabelle oder die Geometrie geändert haben.

Beim Export werden die Daten der Attributtabelle durch Field Desktop geprüft. Werden dabei fehlerhafte Daten gefunden, wird der Export abgebrochen und eine entsprechende Fehlermeldung in QGIS angezeigt.

**Wichtig**: Die Aktualisierung von Ressourcen, für die in Field Desktop Warnungen vorliegen, ist durch den QGIS-Export nur dann möglich, wenn die entsprechenden Warnungen durch den Export behoben werden (etwa durch Änderungen in der Attributtabelle).

### Hinweise

#### Aufbau der Attributtabelle

Empfohlen wird, dass beim Export Layer verwendet werden, die über die Importfunktion von Field Connect erstellt wurden. Möchten Sie Daten aus QGIS heraus in ein noch leeres Field-Projekt übertragen, so führen Sie zunächst einen Import mit der Option "Layer für alle konfigurierten Geometrietypen anlegen" durch, um leere Layer für alle Kategorien mit den dazugehörigen Attributtabellen zu erzeugen. Tragen Sie Ihre Daten nach Möglichkeit in diese Layer ein.

Selbst angelegte Layer müssen im Aufbau und Benennungsschema der Attributtabelle den durch Field Connect erzeugten Layern entsprechen (es müssen allerdings nicht sämtliche Spalten enthalten sein, und es können zusätzliche Spalten für weitere Einträge in Listenfeldern enthalten sein). Darüber hinaus muss in den Benutzereigenschaften des Layers die Variable "field_category" angelegt und der Kategoriebezeichner eingetragen werden, damit beim Export die korrekte Kategorie gesetzt werden kann.

#### Problemlösung bei Fehlermeldungen

Schlägt der Export fehl, dann liegt die Ursache in der Regel darin, dass Eingaben in der Attributtabelle nicht zu den entsprechenden Eingabetypen in der Field-Projektkonfiguration passen. Die Fehlermeldung weist darauf hin, an welcher Stelle das Problem liegt.

In manchen Fällen kann der Export allerdings aufgrund von Datenproblemen scheitern, die anhand der Attributtabelle nicht unmittelbar nachvollziehbar sind. Prüfen Sie in diesem Fall, ob in dem Projekt bereits Warnungen vorliegen und lösen Sie diese über die Werkzeuge des Warnungsmenüs, das Sie über das Warnungs-Icon rechts oben in der Navigationsleiste von Field Desktop erreichen. Je nach Warnungstyp lassen sich die Warnungen möglicherweise auch über Änderungen in der QGIS-Attributtabelle und einen anschließenden Export nach Field Desktop beheben.

Beachten Sie außerdem, dass standardmäßig keine Felddaten, auch nicht in Unterfeldern (z. B. von Feldern der Eingabetypen "Datierung" oder "Längenangabe") gelöscht werden. Wenn ein Feld in der Attributtabelle leer ist, bedeutet dies also nicht automatisch, dass es beim Export in Field Desktop gelöscht wird. Stellen Sie in diesen Fällen sicher, dass die Option "Löschen von Feldern erlauben" aktiviert ist – insbesondere wenn Sie einzelne Unterfelder löschen möchten, da es andernfalls zu Fehlern kommen kann.

## Die Attributtabelle

Die Attributtabelle eines importierten Layers enthält sämtliche Felder, die auch im Ressourceneditor von Field Desktop ausgefüllt werden können. Aufgrund des tabellarischen Datenformats gibt es allerdings Unterschiede bei der Dateneingabe: Abhängig vom Eingabetyp kann etwa mehr als eine Spalte nötig sein, um ein Feld zu beschreiben. Weitere Informationen dazu finden Sie in den folgenden Abschnitten.

Ist für das Feld in der Field-Projektkonfiguration ein Beschreibungstext in der in QGIS eingestellten Sprache hinterlegt, so wird dieser im Tooltip des Feldes in der QGIS-Attributtabelle angezeigt.

Die im folgenden genannten Feldbezeichnungen beziehen sich jeweils auf den Alias, der standardmäßig in der Attributtabelle eines durch Field Connect angelegten Layers gesetzt ist. Die eigentlichen Feldnamen entsprechen den Spaltennamen, die in den von Field Desktop erstellten CSV-Dateien verwendet werden. Sie können sich dabei am Unterkapitel "CSV" des Kapitels "Import und Export" des Handbuchs von Field Desktop orientieren.

### Der Bezeichner

Das Feld "Bezeichner" muss immer ausgefüllt sein. **Wichtig**: Der Bezeichner dient zur Zuordnung des Objekts zur entsprechenden Ressource in Field Desktop. Importieren Sie eine Ressource aus Field Desktop nach QGIS, ändern den Bezeichner und exportieren es anschließend zurück nach Field Desktop, so wird **nicht** die bestehende Ressource aktualisiert, sondern eine zusätzliche Ressource mit dem neuen Bezeichner angelegt.

Bitte beachten Sie, dass ausschließlich der Bezeichner zur eindeutigen Referenzierung eines Objekts verwendet werden sollte. Das Feld "fid", das beim Erstellen von GeoPackage-Dateien angelegt wird, ist dazu nicht geeignet, da sich die hier gesetzten Werte bei späteren Importen aus Field Desktop ändern können.

### Wertelistenfelder

Bei Feldern, die eine Auswahl aus einer Werteliste erlauben, können Sie den entsprechenden Wert aus einem Dropdownmenü bzw. aus einer Checkbox-Liste auswählen (abhängig vom Eingabetyp des Feldes). 

### Ja/Nein-Felder

Für Felder des Eingabetyps "Ja / Nein" können die Werte "Ja" und "Nein" aus einem Dropdownmenü ausgewählt werden.

### Mehrsprachige Felder

Können in ein Feld Werte in verschiedenen Sprachen eingetragen werden, so wird in der Attributtabelle für jede Sprache eine eigene Spalte angelegt. Der Spaltenkopf enthält hinter dem Anzeigenamen des Feldes jeweils den Namen der Sprache (z. B. "Beschreibung Englisch").

In Projekten, die mit älteren Versionen von Field Desktop erstellt wurden, sowie durch Änderungen an der Projektkonfiguration kann es vorkommen, dass in einem mehrsprachigen Feld ein Wert ohne Sprachangabe eingetragen ist. In diesen Fällen wird im Spaltenkopf anstelle des Sprachkürzels der Text "Ohne Sprachangabe" angefügt.

### Dropdown-Listen (Bereich)

Felder des Eingabetyps "Dropdown-Liste (Bereich)" bestehen aus bis zu zwei Unterfeldern, für die jeweils eine eigene Spalte angelegt wird:

* *Wert*: Der Bezeichner des ausgewählten Wertes; bei zwei ausgewählten Werten der erste der beiden Werte.
* *Endwert*: Der Bezeichner des zweiten ausgewählten Wertes, falls zwei Werte ausgewählt sind.

### Datumsfelder

Felder des Eingabetyps "Datum" bestehen aus bis zu drei Unterfeldern, für die jeweils eine eigene Spalte angelegt wird:

* *Wert*: Die Datumsangabe bei einem Einzeldatum; das Startdatum bei einem Datumsbereich
* *Endwert*: Das Enddatum bei einem Datumsbereich
* *Bereich?*: Gibt an ob es sich um einen Datumsbereich handelt. Mögliche Werte sind: "Ja" (Datumsbereich), "Nein" (Einzeldatum).

Die Datumsangaben werden jeweils im Format "Tag.Monat.Jahr" (TT.MM.JJJJ) eingetragen. Die Angaben für Tag und Monat sind optional, sodass auch lediglich ein bestimmter Monat eines Jahres bzw. ein bestimmtes Jahr angegeben werden kann.

Darüber hinaus kann (durch ein Leerzeichen getrennt) optional eine Uhrzeit im Format "Stunden:Minuten" eingetragen werden, sofern die Angabe einer Uhrzeit für das entsprechende Feld in der Projektkonfiguration zugelassen ist.

**Wichtig**: Bei importierten Daten aus Field Desktop sind die Datumsangaben in derjenigen Zeitzone angegeben, die beim Import ausgewählt wurde. Achten Sie beim Export nach Field Desktop darauf, die korrekte Zeitzone auszuwählen. 

### Listenfelder

Bei Feldern des Eingabetyps "Checkboxen" wird für das Feld nur eine einzige Spalte angelegt. Die Feldwerte können durch Checkboxen ausgewählt werden.

Bei Feldern der Eingabetypen "Datierungsangabe", "Längenangabe", "Gewichtsangabe", "Volumenangabe", "Literaturangabe", "Kompositfeld" und "Einzeiliger Text (Liste)" werden **für jeden Listeneintrag** die entsprechenden Spalten für die jeweiligen Unterfelder bzw. Sprachen angelegt. Hinter den Feldnamen wird dabei (beginnend bei 0) eine Nummer zur Identifikation des jeweiligen Eintrags angefügt.

### Relationen

Der Name des Spaltenkopfes beginnt jeweils mit "Relation", gefolgt vom Anzeigenamen der Relation. Eingetragen werden die Bezeichner der Zielressourcen, getrennt durch ein Semikolon.

Zusätzlich zu den Relationen, die in der Projektkonfiguration im Formular der jeweiligen Kategorie aufgeführt sind, können die folgenden Relationen verwendet werden:

* *Übergeordnete Ressource*: Gibt die unmittelbar übergeordnete Ressource in der Hierarchie an; bleibt bei Ressourcen auf oberster Ebene leer.
* *Zeigt* (nur bei Bildressourcen): Verknüpft das Bild mit einer oder mehreren Ressourcen.
* *Wird gezeigt in* (nicht bei Bildressourcen): Verknüpft die Ressource mit einem oder mehreren Bildern.
* *Kartenhintergrund von* (nur bei Bildressourcen): Fügt das Bild als Kartenhintergrund im Kontext der als Ziel angegebenen Ressource hinzu.
* *Hat Kartenhintergrund* (nicht bei Bildressourcen): Fügt im Kontext dieser Ressource eines oder mehrere Bilder als Kartenhintergrund hinzu.
* *Hat Standard-Kartenhintergrund* (nicht bei Bildressourcen): Gibt an, welche Kartenhintergünde bei der Anzeige in Field Desktop standardmäßig aktiviert sein sollen.

Um Bilder mit dem Projekt zu verknüpfen oder auf Projektebene als Kartenhintergrund einzurichten, tragen Sie in der Spalte *Relation Zeigt* bzw. *Relation Kartenhintergrund von* die Projektkennung ein.

### QR-Codes

In der Spalte "QR-Code" kann eine Zeichenkette eingetragen werden, mit der die Ressource eindeutig identifiziert werden kann und die als QR-Code in Field Desktop angezeigt werden soll. Diese Spalte wird nur angelegt, wenn QR-Codes für die entsprechende Kategorie zuvor im Konfigurationseditor aktiviert worden sind.

### Datierungsangaben

Felder des Eingabetyps "Datierungsangabe" sind Listenfelder, die jeweils mehrere Datierungen enthalten können. Eine Datierung besteht aus folgenden Unterfeldern, für die jeweils pro Datierung eine eigene Spalte angelegt wird:

* *Typ*: Der Datierungstyp. Mögliche Werte sind: "Zeitraum", "Einzelnes Jahr", "Vor", "Nach", "Naturwissenschaftlich".
* *Start*: Jahresangabe, die beim Datierungstyp "Nach" sowie für das Anfangsdatum beim Datierungstyp "Zeitraum" gesetzt wird.
* *Ende*: Jahresangabe, die bei den Datierungstypen "Einzelnes Jahr", "Vor", "Naturwissenschaftlich" sowie für das Enddatum beim Datierungstyp "Zeitraum" gesetzt wird.
* *Toleranzspanne*: Toleranzspanne in Jahren beim Datierungstyp "Naturwissenschaftlich".
* *Grundlage*: Grundlage der Datierung, mehrsprachiges Textfeld (eine Spalte pro Sprache).
* *Ungenau?*: Kann beim Datierungstyp "Naturwissenschaftlich" nicht gesetzt werden. Mögliche Werte sind: "Ja", "Nein".
* *Unsicher?*: Kann beim Datierungstyp "Naturwissenschaftlich" nicht gesetzt werden. Mögliche Werte sind: "Ja", "Nein".

Die Jahresangaben "Start" und "Ende" bestehen wiederum aus zwei Unterfeldern:

* *Zeitrechnung*: Mögliche Werte sind "v. Chr.", "n. Chr." und "BP".
* *Jahr*: Die Jahreszahl.

### Längen-, Gewichts- und Volumenangaben

Felder der Eingabetypen "Längenangabe", "Gewichtsangabe" und "Volumenangabe" sind Listenfelder, die jeweils mehrere Einträge enthalten können. Ein Eintrag besteht aus folgenden Unterfeldern, für die jeweils pro Eintrag eine eigene Spalte angelegt wird:

* *Wert*: Der gemessene Zahlenwert.
* *Endwert*: Der zweite gemessene Zahlenwert, falls es sich um einen Bereich handelt.
* *Maßeinheit*: Mögliche Werte sind "mm", "cm", "m" (Längenangabe) / "mg", "g", "kg" (Gewichtsangabe) / "ml", "l" (Volumenangabe).
* *Gemessen an* (Längenangabe) / *Messgerät* (Gewichtsangabe) / *Messverfahren* (Volumenangabe): Es kann jeweils optional ein Wert aus der für das Feld konfigurierten Werteliste ausgewählt werden.
* *Kommentar*: Mehrsprachiges Textfeld (eine Spalte pro Sprache).
* *Ungenau?*: Mögliche Werte sind "Ja", "Nein"

### Literaturangaben

Felder des Eingabetyps "Literaturangabe" sind Listenfelder, die jeweils mehrere Literaturangaben enthalten können. Eine Literaturangabe besteht aus folgenden Unterfeldern, für die jeweils pro Literaturangabe eine eigene Spalte (Texteingabe) angelegt wird:

* *Literaturzitat*
* *Zenon-ID*
* *DOI*
* *Seite*
* *Abbildung*

### Kompositfelder

Felder des Eingabetyps "Kompositfeld" sind Listenfelder, die jeweils mehrere Einträge enthalten können. Für jedes konfigurierte Unterfeld wird pro Eintrag eine Spalte angelegt (bei mehrsprachigen Textfeldern entsprechend eine Spalte für jede Sprache). Im Spaltenkopf wird jeweils der Anzeigename des Unterfelds angegeben.

## Einschränkungen

Mithilfe von Field Connect können Ressourcen der Kategorie "Bild" (sowie der entsprechenden Unterkategorien) importiert und exportiert werden. Es können allerdings über den Export keine neuen Ressourcen dieser Kategorien angelegt werden, da diese zwingend eine dazugehörige Bilddatei voraussetzen, um von Field Desktop akzeptiert zu werden. Der Import und Export von Bilddateien ist kein Bestandteil der vorliegenden Version von Field Connect.

---

<br>

<p align="center">
  <a href="https://www.gbv.de"><img src="./img/gbv_vzg.png" style="width: 294px; height: 70px; box-shadow: none; -webkit-box-shadow: none" alt="VZG"/></a>
</p>
