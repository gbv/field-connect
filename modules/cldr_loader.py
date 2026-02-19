import json
from pathlib import Path


class CLDRLoader:
    def __init__(self, plugin_base_path):
        # path to data/cldr-localenames-full/main/
        self.base = Path(plugin_base_path) / "data" / "cldr-localenames-full" / "main"

    def _wrap_labels(self, lang_dict):
        """Convert { "de": "Deutsch" } to { "de": { "label": "Deutsch" } }"""
        return {code: {"label": name} for code, name in lang_dict.items()}

    def load_all_languages(self):
        """Return dict of: {ui_lang: {code: { "label": translated_name }}}"""
        result = {}

        if not self.base.exists():
            return result

        for folder in sorted(self.base.iterdir()):
            if not folder.is_dir():
                continue

            ui_lang = folder.name
            lang_file = folder / "languages.json"

            try:
                if lang_file.exists():
                    with lang_file.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                        raw = (
                            data["main"]
                            .get(ui_lang, {})
                            .get("localeDisplayNames", {})
                            .get("languages", {})
                        )

                        result[ui_lang] = self._wrap_labels(raw)

                else:
                    result[ui_lang] = {}

            except Exception:
                result[ui_lang] = {}

        return result

    def load_language_for(self, ui_lang):
        """Return wrapped dict: {code: { "label": translated_name }}"""
        folder = self.base / ui_lang
        file = folder / "languages.json"

        if not file.exists():
            return {}

        try:
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            raw = data["main"].get(ui_lang, {}).get("localeDisplayNames", {}).get("languages", {})

            return self._wrap_labels(raw)

        except Exception:
            return {}
