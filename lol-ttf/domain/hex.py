class Hex:
    def __init__(self):
        self.hex_level = ''
        self.hex_components = []


class HexComponent:
    def __init__(self):
        self.hex_component_name = ''
        self.hex_component_img = ''
        self.hex_component_desc = ''


class ChampionHex:
    def __init__(self):
        self.champion_hex_img = ''
        self.champion_hex_name = ''
        self.champion_hex_desc = ''
        self.champion_hex_stages = []


class ChampionHexStage:
    def __init__(self):
        self.galaxy_stage_con = ''
        self.galaxy_hex_list = []


class ChampionHexStageItem:
    def __init__(self):
        self.galaxy_hex_img = ''
        self.galaxy_hex_name = ''
        self.galaxy_hex_desc = ''


class GalaxyHex:
    def __init__(self):
        self.galaxy_hex_img = ''
        self.galaxy_hex_name = ''
        self.galaxy_hex_items = []


class GalaxyHexItem:
    def __init__(self):
        self.title = ''
        self.desc = ''
