class Champion:
    def __init__(self):
        self.name = ''
        self.pic = ''
        self.price = 0
        self.skill = Skill()
        self.champion_stat = ChampionStat()
        self.roles = []


class Skill:
    def __init__(self):
        self.skill_name = ''
        self.skill_type = ''
        self.skill_desc = ''
        self.skill_pic = ''


class ChampionStat:

    def __init__(self):
        self.health = ''
        self.armor = ''
        self.magic_armor = ''
        self.attack_damage = ''
        self.attack_speed = ''
        self.dps = ''
        self.attack_range = ''
        self.init_magic = ''
        self.magic_resist = ''

    def set(self, infos):
        self.health = infos[0]
        self.armor = infos[1]
        self.magic_armor = infos[2]
        self.attack_damage = infos[3]
        self.attack_speed = infos[4]
        self.dps = infos[5]
        self.attack_range = infos[6]
        self.init_magic = infos[7]
        self.magic_resist = infos[8]
