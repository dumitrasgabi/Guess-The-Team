from database import load_teams
import re
import unicodedata


class Game:
    def __init__(self, correct_team = None):
        self.teams = load_teams()
        self.correct_team = correct_team
        self.attribute_mappings = {
            # Continents
            "europe": ("continent", "europe"),
            "uefa": ("continent", "europe"),
            "asia": ("continent", "asia"),
            "afc": ("continent", "asia"),
            "africa": ("continent", "africa"),
            "caf": ("continent", "africa"),
            "north america": ("continent", "north america"),
            "concacaf": ("continent", "north america"),
            "south america": ("continent", "south america"),
            "conmebol": ("continent", "south america"),
            "oceania": ("continent", "oceania"),
            "ofc": ("continent", "oceania"),

            # Zones
            "balkan": ("zone", "balkans"),
            "balkans": ("zone", "balkans"),
            "iberia": ("zone", "iberia"),
            "catalonia": ("zone", "catalonia"),
            "iberian peninsula": ("zone", "iberia"),
            "mediterranean": ("zone", "mediterranean"),
            "baltic": ("zone", "baltic"),
            "west": ("zone", "West"),
            "east": ("zone", "East"),
            "north": ("zone", "North"),
            "south": ("zone", "South"),
            "center": ("zone", "Center"),
            "central": ("zone", "Center"),
            "scandinavia": ("zone", "Scandinavia"),
            "saxon": ("zone", "Saxon"),
            "roman": ("zone", "Roman"),
            "latin": ("zone", "Roman"),
            "island": ("zone", "Island"),
            "slavic": ("zone", "Slavic"),
            "arab": ("zone", "Arab"),
            "british": ("zone", "British"),
            "middle east": ("zone", "Middle East"),

            # Countries
            "albania": ("country", "Albania"),
            "algeria": ("country", "Algeria"),
            "andorra": ("country", "Andorra"),
            "angola": ("country", "Angola"),
            "argentina": ("country", "Argentina"),
            "armenia": ("country", "Armenia"),
            "australia": ("country", "Australia"),
            "austria": ("country", "Austria"),
            "azerbaijan": ("country", "Azerbaijan"),
            "belarus": ("country", "Belarus"),
            "belgium": ("country", "Belgium"),
            "bolivia": ("country", "Bolivia"),
            "bosnia": ("country", "Bosnia"),
            "brazil": ("country", "Brazil"),
            "bulgaria": ("country", "Bulgaria"),
            "canada": ("country", "Canada"),
            "chile": ("country", "Chile"),
            "china": ("country", "China"),
            "colombia": ("country", "Colombia"),
            "costa rica": ("country", "Costa Rica"),
            "croatia": ("country", "Croatia"),
            "cyprus": ("country", "Cyprus"),
            "czech": ("country", "Czechia"),
            "denmark": ("country", "Denmark"),
            "dr congo": ("country", "DR Congo"),
            "ecuador": ("country", "Ecuador"),
            "egypt": ("country", "Egypt"),
            "england": ("country", "England"),
            "estonia": ("country", "Estonia"),
            "faroe": ("country", "Faroe"),
            "fiji": ("country", "Fiji"),
            "finland": ("country", "Finland"),
            "france": ("country", "France"),
            "georgia": ("country", "Georgia"),
            "germany": ("country", "Germany"),
            "gibraltar": ("country", "Gibraltar"),
            "greece": ("country", "Greece"),
            "guyana": ("country", "Guyana"),
            "hungary": ("country", "Hungary"),
            "iceland": ("country", "Iceland"),
            "iran": ("country", "Iran"),
            "ireland": ("country", "Ireland"),
            "israel": ("country", "Israel"),
            "italy": ("country", "Italy"),
            "ivory coast": ("country", "Ivory Coast"),
            "japan": ("country", "Japan"),
            "kazakhstan": ("country", "Kazakhstan"),
            "kosovo": ("country", "Kosovo"),
            "latvia": ("country", "Latvia"),
            "liechtenstein": ("country", "Liechtenstein"),
            "lithuania": ("country", "Lithuania"),
            "luxembourg": ("country", "Luxembourg"),
            "malta": ("country", "Malta"),
            "mexico": ("country", "Mexico"),
            "moldova": ("country", "Moldova"),
            "montenegro": ("country", "Montenegro"),
            "morocco": ("country", "Morocco"),
            "netherlands": ("country", "Netherlands"),
            "new zealand": ("country", "New Zealand"),
            "northern ireland": ("country", "Northern Ireland"),
            "north macedonia": ("country", "North Macedonia"),
            "norway": ("country", "Norway"),
            "paraguay": ("country", "Paraguay"),
            "poland": ("country", "Poland"),
            "portugal": ("country", "Portugal"),
            "qatar": ("country", "Qatar"),
            "romania": ("country", "Romania"),
            "russia": ("country", "Russia"),
            "san marino": ("country", "San Marino"),
            "saudi": ("country", "Saudi Arabia"),
            "scotland": ("country", "Scotland"),
            "serbia": ("country", "Serbia"),
            "slovakia": ("country", "Slovakia"),
            "slovenia": ("country", "Slovenia"),
            "south africa": ("country", "South Africa"),
            "spain": ("country", "Spain"),
            "sudan": ("country", "Sudan"),
            "sweden": ("country", "Sweden"),
            "switzerland": ("country", "Switzerland"),
            "tahiti": ("country", "Tahiti"),
            "tanzania": ("country", "Tanzania"),
            "thailand": ("country", "Thailand"),
            "tunisia": ("country", "Tunisia"),
            "turkey": ("country", "Turkey"),
            "uae": ("country", "UAE"),
            "ukraine": ("country", "Ukraine"),
            "uruguay": ("country", "Uruguay"),
            "usa": ("country", "USA"),
            "uzbekistan": ("country", "Uzbekistan"),
            "venezuela": ("country", "Venezuela"),
            "wales": ("country", "Wales"),

            # Popular Leagues
            "premier league": ("country", "England"),
            "la liga": ("country", "Spain"), 
            "laliga": ("country", "Spain"), 
            "bundesliga": ("country", "Germany"), 
            "serie a": ("country", "Italy"), 
            "ligue 1": ("country", "France"), 
            "eredivisie": ("country", "Netherlands"), 
            "jupiler pro league": ("country", "Belgium"), 
            "premiership": ("country", "Scotland"), 
            "super lig": ("country", "Turkey"),
            "mls": ("country", "USA"), 
            "liga mx": ("country", "Mexico"),

            # Kit colors (expanded)
            "black": ("kit_colors", "black"),
            "white": ("kit_colors", "white"),
            "red": ("kit_colors", "red"),
            "blue": ("kit_colors", "blue"),
            "green": ("kit_colors", "green"),
            "yellow": ("kit_colors", "yellow"),
            "orange": ("kit_colors", "orange"),
            "amber": ("kit_colors", "orange"),
            "pink": ("kit_colors", "pink"),
            "cyan": ("kit_colors", "cyan"),
            "maroon": ("kit_colors", "maroon"),
            "claret": ("kit_colors", "maroon"),
            "burgundy": ("kit_colors", "burgundy"),
            "gray": ("kit_colors", "gray"),
            "brown": ("kit_colors", "brown"),
            "purple": ("kit_colors", "purple"),
            "gold": ("kit_colors", "gold"),
            "silver": ("kit_colors", "silver"),
            "navy": ("kit_colors", "navy"),
            "lime": ("kit_colors", "lime"),
            "beige": ("kit_colors", "beige"),

            # Logo features (expanded animals and symbols)
            "animal": ("logo_features", "animal"),
            "wolf": ("logo_features", "wolf"),
            "dog": ("logo_features", "dog"),
            "fox": ("logo_features", "fox"),
            "lion": ("logo_features", "lion"),
            "tiger": ("logo_features", "tiger"),
            "bear": ("logo_features", "bear"),
            "eagle": ("logo_features", "eagle"),
            "falcon": ("logo_features", "falcon"),
            "hawk": ("logo_features", "hawk"),
            "dragon": ("logo_features", "dragon"),
            "horse": ("logo_features", "horse"),
            "bull": ("logo_features", "bull"),
            "bird": ("logo_features", "bird"),
            "fish": ("logo_features", "fish"),
            "dolphin": ("logo_features", "dolphin"),
            "mythologic": ("logo_features", "mythologic"),
            "mythology": ("logo_features", "mythologic"),
            "liver bird": ("logo_features", "liver bird"),
            "seagull": ("logo_features", "seagull"),
            "crocodile": ("logo_features", "crocodile"),
            "panther": ("logo_features", "panther"),
            "rhino": ("logo_features", "rhino"),
            "star": ("logo_features", "star"),
            "moon": ("logo_features", "moon"),
            "sun": ("logo_features", "sun"),
            "stripes": ("logo_features", "stripes"),
            "checkers": ("logo_features", "checkers"),
            "wings": ("logo_features", "wings"),
            "ball": ("logo_features", "ball"),
            "ship": ("logo_features", "ship"),
            "anchor": ("logo_features", "anchor"),
            "crown": ("logo_features", "crown"),
            "royal": ("logo_features", "crown"),
            "monogram": ("logo_features", "monogram"),
            "coat of arms": ("logo_features", "coat of arms"),
            "cross": ("logo_features", "cross"),
            "shield": ("logo_features", "shield"),
            "text": ("logo_features", "text"),
            "flag": ("logo_features", "flag"),
            "circle": ("logo_features", "circle"),
            "oval": ("logo_features", "oval"),
            "diamond": ("logo_features", "diamond"),
            "human": ("logo_features", "human"),
            "eiffel tower": ("logo_features", "eiffel tower"),
            "lily": ("logo_features", "lily"),
            "cannon": ("logo_features", "cannon"),
            "devil": ("logo_features", "devil"),
            "tree": ("logo_features", "tree"),
            "power plant": ("logo_features", "power plant"),
            "hammer": ("logo_features", "hammer"),
            "letter": ("logo_features", "letter"),
            "letters": ("logo_features", "letter"),
            "bee": ("logo_features", "bee"),
            "squirrel": ("logo_features", "squirrel"),
            "hand": ("logo_features", "hand"),
            "castle": ("logo_features", "castle"),
            "tower": ("logo_features", "castle"),
            "halo": ("logo_features", "halo"),
            "arrow": ("logo_features", "arrow"),
            "bat": ("logo_features", "bat"),
            "sword": ("logo_features", "sword"),
            "gryphon": ("logo_features", "gryphon"),
            "pine": ("logo_features", "pine"),
            "pinecone": ("logo_features", "pine"),
            "church": ("logo_features", "church"),
            "flower": ("logo_features", "flower"),
            "wheat": ("logo_features", "wheat"),
            "olive": ("logo_features", "olive"),
            "sheep": ("logo_features", "sheep"),
            "train": ("logo_features", "train"),
            "fountain": ("logo_features", "fountain"),
            "clover": ("logo_features", "clover"),
            "plant": ("logo_features", "plant"),
            "corn": ("logo_features", "corn"),
            "ribbon": ("logo_features", "ribbon"),
            "harp": ("logo_features", "harp"),
            "torch": ("logo_features", "torch"),

            # Trophy
            "ucl": ("trophy", "ucl"),
            "champions league": ("trophy", "ucl"),
            "uel": ("trophy", "uel"),
            "europa league": ("trophy", "uel"),
            "uecl": ("trophy", "uecl"),
            "conference": ("trophy", "uecl"),
            "intertoto": ("trophy", "intertoto"),
            "title": ("trophy", "title"),
            "cup": ("trophy", "cup"),
            "uefa super cup": ("trophy", "uefa super cup"),
            "club world cup": ("trophy", "club world cup"),
            "cwc": ("trophy", "club world cup"),
            "intercontinental": ("trophy", "club world cup"),
            "cup winners cup": ("trophy", "cup winners cup"),
            "libertadores": ("trophy", "copa libertadores"),
            "sudamericana": ("trophy", "copa sudamericana"),
            "recopa": ("trophy", "recopa sudamericana"),
            "concacaf champions cup": ("trophy", "concacaf champions cup"),
            "champions cup": ("trophy", "concacaf champions cup"),
            "concacaf caribbean cup": ("trophy", "concacaf caribbean cup"),
            "caribbean cup": ("trophy", "concacaf caribbean cup"),
            "concacaf central american cup": ("trophy", "concacaf central american cup"),
            "central american cup": ("trophy", "concacaf central american cup"),
            "leagues cup": ("trophy", "leagues cup"),
            "caf champions league": ("trophy", "caf champions league"),
            "caf cl": ("trophy", "caf champions league"),
            "caf confederation cup": ("trophy", "caf confederation cup"),
            "confederation": ("trophy", "caf confederation cup"),
            "caf super cup": ("trophy", "caf super cup"),
            "afc champions league": ("trophy", "afc champions league elite"),
            "elite": ("trophy", "afc champions league elite"),
            "champions league 2": ("trophy", "afc champions league 2"),
            "acl 2": ("trophy", "afc champions league 2"),
            "afc cup": ("trophy", "afc champions league 2"),
            "challenge league": ("trophy", "afc challenge league"),
            "acgl": ("trophy", "afc challenge league"),
            "ofc champions league": ("trophy", "ofc challenge league"),
            "ofc": ("trophy", "ofc challenge league")
        }

    def normalize(self, text):
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        text = re.sub(r"[^a-z0-9]", "", text)  # remove spaces, punctuation
        return text

    def check_guess(self, guess):
        norm_guess = self.normalize(guess)
        names = []

        if isinstance(self.correct_team["name"], str):
            names.append(self.correct_team["name"])
        else:
            names.extend(self.correct_team["name"])

        full_name = self.correct_team.get("full_name")
        if full_name:
            names.append(full_name)

        for n in names:
            if self.normalize(n) == norm_guess:
                return True

        return False

    def answer_question(self, question):
        question = question.lower().strip()
        sorted_keywords = sorted(self.attribute_mappings.items(), key=lambda item: -len(item[0]))

        for keyword, (attr, expected) in sorted_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, question):
                if isinstance(self.correct_team[attr], list):
                    return ("Yes", "yes") if expected.lower() in [item.lower() for item in self.correct_team[attr]] else ("No", "no")
                elif callable(expected):
                    return ("Yes", "yes") if expected(self.correct_team[attr]) else ("No", "no")
                else:
                    return ("Yes", "yes") if str(self.correct_team[attr]).lower() == expected.lower() else ("No", "no")

        return "???", "neutral"

