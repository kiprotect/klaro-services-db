from helpers import serialize_text, deserialize_text, translate, hash
import yaml
import sys
import os
import re

class DB:

    def __init__(self, path):
        self.path = path
        self.db = {}

    def load(self):
        if os.path.exists(self.path):
            with open(self.path) as input_file:
                self.db = yaml.load(input_file.read(), Loader=yaml.BaseLoader)

    def get(self, language, key):
        return self.db.get(language, {}).get(key)

    def set(self, language, key, hv):
        if not language in self.db:
            self.db[language] = {}
        self.db[language][key] = hv
        # we immediately write the DB to disk
        self.write()

    def write(self):
        with open(self.path, "wb") as output_file:
            output_file.write(yaml.dump(self.db, encoding='utf-8', allow_unicode=True, indent=2, sort_keys=True))

def deserialize_struct(struct, translated=False):
    for k, v in struct.items():
        if isinstance(v, str):
            if not translated:
                # we make a roundtrip to remove translation markup...
                struct[k] = deserialize_text(serialize_text(v))
            #  if there are <tr-snip> tags, we only return the text within them.
            if re.match(r".*<tr-snip>", v):
                snippets = []
                for m in re.finditer(r"<tr-snip>([^<]+?)</tr-snip>", v):
                    snippets.append(m.group(1).strip())
                struct[k] = " ".join(snippets)
        else:
            deserialize_struct(v, translated=translated)
    return process_filters(struct)

filtermap = {
    'capitalize' : lambda v : " ".join([vv.capitalize() if i == 0 else vv for (i, vv) in enumerate(v.split(" ")) ]),
}

def process_filters(struct):
    filtered_struct = {}
    for k, v in struct.items():
        kp = k.split("|")
        kr = kp[0]
        filters = kp[1:]
        if isinstance(v, str):
            for filter in filters:
                if not filter in filtermap:
                    sys.stderr.write(f"Unknown filter: {filter}\n")
                    continue
                v = filtermap[filter](v)
            filtered_struct[kr] = v
        else:
            filtered_struct[k] = process_filters(v)
    return filtered_struct

def translate_struct(ref_lang, target_lang, translations, db, token):
    if not target_lang in translations:
        translations[target_lang] = {}
    for k, v in translations.get('$'+ref_lang, {}).items():
        kp = k.split("|")
        kr = kp[0]
        kh = hash(v)
        rh = db.get(target_lang, kr)
        if rh == kh:
            continue #translation is still good
        print(f"Translating {kr} from {ref_lang} to {target_lang}...")
        try:
            if target_lang == ref_lang:
                translation = deserialize_text(serialize_text(v))
            else:
                translation = deserialize_text(translate(serialize_text(v), ref_lang, target_lang, token))
        except KeyboardInterrupt:
            raise
        except:
            continue
        translations[target_lang][kr] = translation
        db.set(target_lang, kr, kh)
    return translations

def update_translations(services_path, ref_lang, token):
    """
    - We load the reference English translations from {ref_lang}.ref.yml
    - We load the translation cache from src/translations/{ref_lang}.trans
    - We generate translations for all target languages based on the keys in
      the reference language translations file.
    - We post-process and store the translations.
    - We also post-process the reference translations and store them.
    """
    for file in os.listdir(services_path):
        if file.endswith('.trans') or not file.endswith('.yml'):
            continue
        with open(os.path.join(services_path, file)) as service_file:
            service_config = yaml.load(service_file.read(), Loader=yaml.FullLoader)
            if not service_config:
                continue
        # we load the translations cache for the given service
        db_path = os.path.join(services_path, file+".trans")
        db = DB(db_path)
        db.load()
        for target_lang in TARGET_LANGS:
            service_config['translations'] = translate_struct(ref_lang, target_lang, service_config.get('translations', {}), db, token)
            with open(os.path.join(services_path, file), "wb") as service_file:
                service_file.write(yaml.dump(service_config, encoding='utf-8', allow_unicode=True, indent=2, sort_keys=True))

SERVICES_PATH = os.environ.get('SERVICES') or os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')))
TOKEN = os.environ.get('TOKEN')
REF_LANG = "en"
TARGET_LANGS = ["es", "de", "fr", "pt", "it", "nl", "pl", "zh", "en"]
#TARGET_LANGS = ["de", "fr"]
if __name__ == '__main__':
    if len(sys.argv) > 1:
        TARGET_LANGS = sys.argv[1].split(",")
    if not TOKEN:
        sys.stderr.write(f"Please provide a DeepL token in the 'TOKEN' environment variable.\n")
        sys.exit(-1)
    update_translations(SERVICES_PATH, REF_LANG, TOKEN)
