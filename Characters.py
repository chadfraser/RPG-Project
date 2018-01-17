import random
import time

# HP, damage, defense, critical hit chance
# Spell cool down, casting duration, magic defense
# First turn reaction, speed, evasion, run chance

# In combat spells. Camping/preparatory skills. Out of combat support skills.
# FIRE, PARRY       SET TRAPS, HIDE             IDENTIFY DEFENSE, BREAK CURSE
# Out of combat support: Scouting, charisma, spirituality, perception
# SCOUTING:
# CHARISMA: Getting information and quests, avoiding non-random encounters
# SPIRITUALITY:
# PERCEPTION: Finding treasure, traps, hidden doors


def printWithDelay(text, delayTime=1):
    print(text)
    time.sleep(delayTime)


class Character:
    def __init__(self):
        self.name = ""
        self.HP = {"max": 0, "current": 0}
        self.strength = {"base": 0, "modified": 0, "exhaustion": 0}
        self.defense = {"base": 0, "modified": 0, "exhaustion": 0}
        self.conviction = {"base": 0, "modified": 0, "exhaustion": 0, "consumed": 0}
        self.magicDef = {"base": 0, "modified": 0, "exhaustion": 0}
        self.evasion = {"base": 0, "modified": 0, "exhaustion": 0}
        self.accuracy = {"base": 0, "modified": 0, "exhaustion": 0}
        self.speed = {"base": 0, "modified": 0, "exhaustion": 0}
        self.criticalRate = {"base": 0, "modified": 0, "exhaustion": 0}
        self.strikeCount = {"base": 1, "modified": 1, "exhaustion": 0}
        self.aggression = 0

        self.weakness = []
        self.resistance = []
        self.status = []
        self.equipment = []
        self.contactElement = []
        self.knownSkills = []
        self.activeSkills = []
        self.experience = 0

    def attackTarget(self, target):
        timesAttackDone = 0
        while timesAttackDone < self.strikeCount["modified"]:
            if self.shouldAttackHit(target):
                self.aggression += 1
                damage, wasCritical = self.determineDamage(target)
                finalDamage = target.applyWeaknessAndResistance(damage, self.contactElement)
                target.applyDamage(finalDamage, wasCritical)
                if target.isIncapacitated():
                    target.printDeathMessage()
                    self.aggression += 10
                    break
            else:
                self.printAttackMiss()
            timesAttackDone += 1

    def shouldAttackHit(self, target):
        toHitFormula = 160 + self.accuracy["modified"] - target.evasion["modified"]
        randomCheckToHit = random.randint(1, 200)
        if randomCheckToHit <= toHitFormula:
            return True
        return False

    def shouldCriticalHit(self):
        criticalHitDiceRoll = random.randint(1, 200)
        if criticalHitDiceRoll <= self.criticalRate["modified"]:
            return True
        return False

    def determineDamage(self, target):
        penetratedDamage = random.randint(self.strength["modified"] - target.defense["modified"],
                                          (2 * self.strength["modified"]) - target.defense["modified"])
        damage = max(1, penetratedDamage)
        wasCritical = self.shouldCriticalHit()
        if wasCritical:
            damage += random.randint(self.strength["modified"], 2 * self.strength["modified"])
        finalDamage = target.applyWeaknessAndResistance(damage, self.contactElement)
        return finalDamage, wasCritical

    def applyDamage(self, damage, wasCritical=False):
        self.HP["current"] -= damage
        self.printDamageAndCritical(damage, wasCritical)
        if self.HP["current"] <= 0:
            self.HP["current"] = 0
        if isinstance(self, Hero):
            self.printCurrentHP()

    def isIncapacitated(self):
        if self.HP["current"] <= 0:
            return True
        return False

    def applyWeaknessAndResistance(self, damage, attackElements):
        weakToAttack = resistantToAttack = False
        for element in attackElements:
            if element in self.weakness:
                weakToAttack = True
            if element in self.resistance:
                resistantToAttack = True
        if weakToAttack:
            damage = round(damage * 1.5)
        if resistantToAttack:
            damage = max(1, damage // 2)
        return damage

    def controlStartOfTurnSkills(self, heroList, enemyList):
        newSkills = self.activeSkills[:]
        for skill in self.activeSkills:
            if skill.startOfTurn:
                skillContinues = skill.startOfTurnEffect(self, heroList, enemyList)
                if not skillContinues:
                    newSkills.remove(skill)
        self.activeSkills = newSkills

    def controlOnEnemyAttackSkills(self, heroList, enemyList, attackingEnemy, attackTarget):
        newSkills = self.activeSkills[:]
        for skill in self.activeSkills:
            if skill.onEnemyAttack:
                skillContinues = skill.onEnemyAttackEffect(self, heroList, enemyList, attackingEnemy, attackTarget)
                if not skillContinues:
                    newSkills.remove(skill)
        self.activeSkills = newSkills

    def controlAfterEnemyAttackSkills(self, heroList, enemyList, attackingEnemy, attackTarget):
        newSkills = self.activeSkills[:]
        for skill in self.activeSkills:
            if skill.afterEnemyAttack:
                skillContinues = skill.afterEnemyAttackEffect(self, heroList, enemyList, attackingEnemy, attackTarget)
                if not skillContinues:
                    newSkills.remove(skill)
        self.activeSkills = newSkills

    def printAttackTarget(self, target):
        printWithDelay("{} attacks {}!".format(self.name, target.name))

    def printDamageAndCritical(self, damage, wasCritical):
        if wasCritical:
            printWithDelay("--Critical hit!")
        printWithDelay("--{} takes {} damage.".format(self.name, damage))

    def printCurrentHP(self):
        printWithDelay("--{}'s HP is now {}.".format(self.name, self.HP["current"]), 3)

    def printDeathMessage(self):
        printWithDelay("--{} has fallen.".format(self.name), 3)

    def printAttackMiss(self):
        printWithDelay("--{} missed!".format(self.name), 3)

    def printAmountHealed(self, healHPValue):
        printWithDelay("--{} healed {} HP!".format(self.name, healHPValue), 3)


class Hero(Character):
    def __init__(self):
        Character.__init__(self)
        self.weaponSpeed = {"base": 0, "modified": 0, "exhaustion": 0}
        self.strikeCount["base"] = 1 + self.weaponSpeed["base"] // 32
        self.scouting = {"base": 0, "modified": 0, "exhaustion": 0}
        self.spirituality = {"base": 0, "modified": 0, "exhaustion": 0}
        self.charisma = {"base": 0, "modified": 0, "exhaustion": 0}
        self.perception = {"base": 0, "modified": 0, "exhaustion": 0}
        self.endurance = {"base": 0, "modified": 0, "exhaustion": 0}
        self.reflex = {"base": 0, "modified": 0, "exhaustion": 0}
        self.luck = {"base": 0, "modified": 0, "exhaustion": 0}
        self.exhaustion = 0
        self.level = 1
        self.actionCount = 0
        self.encounterCount = 0

    def setHeroDefaultValues(self):
        self.strength["modified"] = self.strength["base"] + self.strength["exhaustion"]
        self.defense["modified"] = self.defense["base"] + self.defense["exhaustion"]
        self.conviction["modified"] = self.conviction["base"] + self.conviction["exhaustion"] - \
                                      self.conviction["consumed"]
        self.magicDef["modified"] = self.magicDef["base"] + self.magicDef["exhaustion"]
        self.evasion["modified"] = self.evasion["base"] + self.evasion["exhaustion"]
        self.strikeCount["modified"] = 1 + self.weaponSpeed["base"] // 32 + self.strikeCount["exhaustion"]
        self.accuracy["modified"] = self.accuracy["base"] + self.accuracy["exhaustion"]
        self.speed["modified"] = self.speed["base"] + self.speed["exhaustion"]
        self.criticalRate["modified"] = self.criticalRate["base"] + self.criticalRate["exhaustion"]
        self.scouting["modified"] = self.scouting["base"] + self.scouting["exhaustion"]
        self.spirituality["modified"] = self.spirituality["base"] + self.spirituality["exhaustion"]
        self.charisma["modified"] = self.charisma["base"] + self.charisma["exhaustion"]
        self.perception["modified"] = self.perception["base"] + self.perception["exhaustion"]
        self.endurance["modified"] = self.endurance["base"]
        self.reflex["modified"] = self.reflex["base"] + self.reflex["exhaustion"]
        self.luck["modified"] = self.luck["base"] + self.luck["exhaustion"]

    def applyStatVarianceOnInitialization(self):
        self.HP["max"] = max(1, self.HP["max"] + random.randint(-5, 5))
        self.strength["base"] = max(1, self.strength["base"] + random.randint(-3, 3))
        self.defense["base"] = max(0, self.defense["base"] + random.randint(0, 3))
        self.conviction["base"] = max(0, self.conviction["base"] + random.randint(-3, 3))
        self.magicDef["base"] = max(0, self.magicDef["base"] + random.randint(-3, 3))
        self.evasion["base"] = max(0, self.evasion["base"] + random.randint(-5, 5))
        self.weaponSpeed["base"] = max(1, self.weaponSpeed["base"] + random.randint(-5, 5))
        self.accuracy["base"] = max(0, self.accuracy["base"] + random.randint(-3, 3))
        self.speed["base"] = max(0, self.speed["base"] + random.randint(-2, 2))
        self.criticalRate["base"] = max(0, self.criticalRate["base"] + random.randint(0, 2))
        self.scouting["base"] = max(0, self.scouting["base"] + random.randint(-5, 5))
        self.spirituality["base"] = max(0, self.spirituality["base"] + random.randint(-5, 5))
        self.charisma["base"] = max(0, self.charisma["base"] + random.randint(-5, 5))
        self.perception["base"] = max(0, self.perception["base"] + random.randint(-5, 5))
        self.endurance["base"] = max(0, self.endurance["base"] + random.randint(-10, 10))
        self.reflex["base"] = max(0, self.reflex["base"] + random.randint(-5, 5))
        self.luck["base"] = max(0, self.luck["base"] + random.randint(-5, 5))

    def checkCombatExhaustion(self):
        exhaustionDiceRoll = 0
        for __ in range(self.actionCount):
            exhaustionDiceRoll += random.randint(1, 20)
        if exhaustionDiceRoll > self.endurance["modified"]:
            self.sufferExhaustion()
            self.actionCount = 0

    def checkEncounterExhaustion(self):
        exhaustionDiceRoll = 0
        for __ in range(self.encounterCount):
            exhaustionDiceRoll += random.randint(1, 20)
        if exhaustionDiceRoll > self.endurance["modified"]:
            self.sufferExhaustion()
            self.encounterCount = 0

    def modifyExhaustionStats(self):
        lowValueExhaustionStats = [self.strength["exhaustion"], self.conviction["exhaustion"],
                                   self.magicDef["exhaustion"], self.accuracy["exhaustion"],
                                   self.defense["exhaustion"], self.strikeCount["exhaustion"],
                                   self.criticalRate["exhaustion"]]
        highValueExhaustionStats = [self.evasion["exhaustion"], self.speed["exhaustion"], self.scouting["exhaustion"],
                                    self.luck["exhaustion"], self.spirituality["exhaustion"],
                                    self.charisma["exhaustion"], self.perception["exhaustion"],
                                    self.reflex["exhaustion"]]
        lowValueStatPenalty = [(random.randint(1, 4) if self.exhaustion + random.randint(1, 10) >= 8 else 0)
                               for _ in range(7)]
        highValueStatPenalty = [(random.randint(1, 3) if self.exhaustion + random.randint(1, 10) >= 8 else 0)
                                for _ in range(8)]

        self.strength["exhaustion"], self.conviction["exhaustion"], self.magicDef["exhaustion"], \
            self.accuracy["exhaustion"], self.defense["exhaustion"], self.strikeCount["exhaustion"], \
            self.criticalRate["exhaustion"] = [x - y for x, y in zip(lowValueExhaustionStats, lowValueStatPenalty)]

        self.evasion["exhaustion"], self.speed["exhaustion"], self.scouting["exhaustion"], self.luck["exhaustion"], \
            self.spirituality["exhaustion"], self.charisma["exhaustion"], self.perception["exhaustion"], \
            self.reflex["exhaustion"] = [x - y for x, y in zip(highValueExhaustionStats, highValueStatPenalty)]

    def sufferExhaustion(self):
        self.exhaustion += 1
        self.modifyExhaustionStats()
        exhaustionStatList = [self.strength["exhaustion"], self.conviction["exhaustion"], self.magicDef["exhaustion"],
                              self.accuracy["exhaustion"], self.defense["exhaustion"], self.strikeCount["exhaustion"],
                              self.criticalRate["exhaustion"], self.evasion["exhaustion"], self.speed["exhaustion"],
                              self.scouting["exhaustion"], self.luck["exhaustion"], self.spirituality["exhaustion"],
                              self.charisma["exhaustion"], self.perception["exhaustion"], self.reflex["exhaustion"]]
        modifiedStatList = [self.strength["modified"], self.conviction["modified"], self.magicDef["modified"],
                            self.accuracy["modified"], self.defense["modified"], self.strikeCount["modified"],
                            self.criticalRate["modified"], self.evasion["modified"], self.speed["modified"],
                            self.scouting["modified"], self.luck["modified"], self.spirituality["modified"],
                            self.charisma["modified"], self.perception["modified"], self.reflex["modified"]]
        self.strength["modified"], self.conviction["modified"], self.magicDef["modified"], self.accuracy["modified"], \
            self.defense["modified"], self.strikeCount["modified"], self.criticalRate["modified"], \
            self.evasion["modified"], self.speed["modified"], self.scouting["modified"], self.luck["modified"], \
            self.spirituality["modified"], self.charisma["modified"], self.perception["modified"], \
            self.reflex["modified"] = [x + y for x, y in zip(modifiedStatList, exhaustionStatList)]
        printWithDelay("{} is becoming exhausted!".format(self.name), 2)
        self.ensureAllStatsNonNegative()

    def ensureAllStatsNonNegative(self):
        self.strength["modified"] = max(1, self.strength["modified"])
        self.defense["modified"] = max(0, self.defense["modified"])
        self.conviction["modified"] = max(0, self.conviction["modified"])
        self.magicDef["modified"] = max(0, self.magicDef["modified"])
        self.evasion["modified"] = max(0, self.evasion["modified"])
        self.strikeCount["modified"] = max(1, self.strikeCount["modified"])
        self.accuracy["modified"] = max(0, self.defense["modified"])
        self.speed["modified"] = max(0, self.speed["modified"])
        self.criticalRate["modified"] = max(0, self.criticalRate["modified"])
        self.scouting["modified"] = max(0, self.scouting["modified"])
        self.spirituality["modified"] = max(0, self.spirituality["modified"])
        self.charisma["modified"] = max(0, self.charisma["modified"])
        self.perception["modified"] = max(0, self.perception["modified"])
        self.endurance["modified"] = max(0, self.endurance["modified"])
        self.reflex["modified"] = max(0, self.reflex["modified"])
        self.luck["modified"] = max(0, self.luck["modified"])

    def shouldRun(self, listOfEnemies):
        listOfEnemyEvasion = [enemy.evasion["modified"] for enemy in listOfEnemies if not enemy.isIncapacitated()]
        maxEnemyEvasion = max(listOfEnemyEvasion)
        runningDiceRoll = random.randint(0, 2 * maxEnemyEvasion)
        if self.luck["modified"] > runningDiceRoll:
            return True
        return False


class Fencer(Hero):
    def __str__(self):
        return "Fencer"

    def __init__(self, name="Cousland"):
        super().__init__()
        self.name = name
        self.HP["max"] = 30
        self.strength["base"] = 13
        self.defense["base"] = 2
        self.conviction["base"] = 5
        self.magicDef["base"] = 10
        self.evasion["base"] = 15
        self.weaponSpeed["base"] = 15
        self.accuracy["base"] = 15
        self.speed["base"] = 15
        self.criticalRate["base"] = 0

        self.scouting["base"] = 5
        self.spirituality["base"] = 15
        self.charisma["base"] = 5
        self.perception["base"] = 15
        self.endurance["base"] = 40
        self.reflex["base"] = 10
        self.luck["base"] = 5


class Hunter(Hero):
    def __str__(self):
        return "Hunter"

    def __init__(self, name="Eliza"):
        super().__init__()
        self.name = name
        self.HP["max"] = 30
        self.strength["base"] = 15
        self.defense["base"] = 1
        self.conviction["base"] = 1
        self.magicDef["base"] = 5
        self.evasion["base"] = 7
        self.weaponSpeed["base"] = 20
        self.accuracy["base"] = 15
        self.speed["base"] = 8
        self.criticalRate["base"] = 0

        self.scouting["base"] = 25
        self.spirituality["base"] = 20
        self.charisma["base"] = 10
        self.perception["base"] = 15
        self.endurance["base"] = 60
        self.reflex["base"] = 25
        self.luck["base"] = 1


class Archer(Hero):
    def __str__(self):
        return "Archer"

    def __init__(self, name="Oakwood"):
        super().__init__()
        self.name = name
        self.HP["max"] = 30
        self.strength["base"] = 13
        self.defense["base"] = 0
        self.conviction["base"] = 20
        self.magicDef["base"] = 5
        self.evasion["base"] = 12
        self.weaponSpeed["base"] = 20
        self.accuracy["base"] = 25
        self.speed["base"] = 10
        self.criticalRate["base"] = 2

        self.scouting["base"] = 15
        self.spirituality["base"] = 5
        self.charisma["base"] = 20
        self.perception["base"] = 25
        self.endurance["base"] = 40
        self.reflex["base"] = 5
        self.luck["base"] = 5


class Mage(Hero):
    def __str__(self):
        return "Mage"

    def __init__(self, name="Canin"):
        super().__init__()
        self.name = name
        self.HP["max"] = 15
        self.strength["base"] = 5
        self.defense["base"] = 0
        self.conviction["base"] = 20
        self.magicDef["base"] = 20
        self.evasion["base"] = 12
        self.weaponSpeed["base"] = 5
        self.accuracy["base"] = 10
        self.speed["base"] = 8
        self.criticalRate["base"] = 0

        self.scouting["base"] = 15
        self.spirituality["base"] = 5
        self.charisma["base"] = 10
        self.perception["base"] = 20
        self.endurance["base"] = 45
        self.reflex["base"] = 15
        self.luck["base"] = 10


class Druid(Hero):
    def __str__(self):
        return "Druid"

    def __init__(self, name="Serena"):
        super().__init__()
        self.name = name
        self.HP["max"] = 25
        self.strength["base"] = 10
        self.defense["base"] = 2
        self.conviction["base"] = 18
        self.magicDef["base"] = 7
        self.evasion["base"] = 12
        self.weaponSpeed["base"] = 15
        self.accuracy["base"] = 20
        self.speed["base"] = 5
        self.criticalRate["base"] = 0

        self.scouting["base"] = 25
        self.spirituality["base"] = 25
        self.charisma["base"] = 15
        self.perception["base"] = 5
        self.endurance["base"] = 55
        self.reflex["base"] = 25
        self.luck["base"] = 1


class Summoner(Hero):
    def __str__(self):
        return "Summoner"

    def __init__(self, name="Goldwall"):
        super().__init__()
        self.name = name
        self.HP["max"] = 25
        self.strength["base"] = 10
        self.defense["base"] = 1
        self.conviction["base"] = 17
        self.magicDef["base"] = 5
        self.evasion["base"] = 10
        self.weaponSpeed["base"] = 14
        self.accuracy["base"] = 15
        self.speed["base"] = 8
        self.criticalRate["base"] = 0

        self.scouting["base"] = 20
        self.spirituality["base"] = 15
        self.charisma["base"] = 25
        self.perception["base"] = 10
        self.endurance["base"] = 45
        self.reflex["base"] = 25
        self.luck["base"] = 10


class Healer(Hero):
    def __str__(self):
        return "Healer"

    def __init__(self, name="Heaylin"):
        super().__init__()
        self.name = name
        self.HP["max"] = 20
        self.strength["base"] = 5
        self.defense["base"] = 3
        self.conviction["base"] = 10
        self.magicDef["base"] = 10
        self.evasion["base"] = 10
        self.weaponSpeed["base"] = 18
        self.accuracy["base"] = 20
        self.speed["base"] = 15
        self.criticalRate["base"] = 4

        self.scouting["base"] = 15
        self.spirituality["base"] = 20
        self.charisma["base"] = 15
        self.perception["base"] = 20
        self.endurance["base"] = 40
        self.reflex["base"] = 0
        self.luck["base"] = 15


class Apprentice(Hero):
    def __str__(self):
        return "Apprentice"

    def __init__(self, name="Rosalin"):
        super().__init__()
        self.name = name
        self.HP["max"] = 15
        self.strength["base"] = 10
        self.defense["base"] = 0
        self.conviction["base"] = 20
        self.magicDef["base"] = 15
        self.evasion["base"] = 15
        self.weaponSpeed["base"] = 16
        self.accuracy["base"] = 18
        self.speed["base"] = 5
        self.criticalRate["base"] = 0

        self.scouting["base"] = 10
        self.spirituality["base"] = 25
        self.charisma["base"] = 20
        self.perception["base"] = 20
        self.endurance["base"] = 60
        self.reflex["base"] = 5
        self.luck["base"] = 10


class Scholar(Hero):
    def __str__(self):
        return "Scholar"

    def __init__(self, name="Flynn"):
        super().__init__()
        self.name = name
        self.HP["max"] = 20
        self.strength["base"] = 12
        self.defense["base"] = 0
        self.conviction["base"] = 15
        self.magicDef["base"] = 20
        self.evasion["base"] = 7
        self.weaponSpeed["base"] = 14
        self.accuracy["base"] = 15
        self.speed["base"] = 8
        self.criticalRate["base"] = 0

        self.scouting["base"] = 5
        self.spirituality["base"] = 5
        self.charisma["base"] = 25
        self.perception["base"] = 25
        self.endurance["base"] = 40
        self.reflex["base"] = 25
        self.luck["base"] = 10


class Guard(Hero):
    def __str__(self):
        return "Guard"

    def __init__(self, name="Bagsword"):
        super().__init__()
        self.name = name
        self.HP["max"] = 40
        self.strength["base"] = 8
        self.defense["base"] = 4
        self.conviction["base"] = 10
        self.magicDef["base"] = 15
        self.evasion["base"] = 5
        self.weaponSpeed["base"] = 15
        self.accuracy["base"] = 10
        self.speed["base"] = 4
        self.criticalRate["base"] = 0

        self.scouting["base"] = 20
        self.spirituality["base"] = 15
        self.charisma["base"] = 5
        self.perception["base"] = 15
        self.endurance["base"] = 70
        self.reflex["base"] = 0
        self.luck["base"] = 1


class SiegeMan(Hero):
    def __str__(self):
        return "Siege Man"

    def __init__(self, name="Saba"):
        super().__init__()
        self.name = name
        self.HP["max"] = 35
        self.strength["base"] = 10
        self.defense["base"] = 4
        self.conviction["base"] = 6
        self.magicDef["base"] = 20
        self.evasion["base"] = 5
        self.weaponSpeed["base"] = 5
        self.accuracy["base"] = 20
        self.speed["base"] = 1
        self.criticalRate["base"] = 0

        self.scouting["base"] = 5
        self.spirituality["base"] = 20
        self.charisma["base"] = 15
        self.perception["base"] = 5
        self.endurance["base"] = 75
        self.reflex["base"] = 5
        self.luck["base"] = 1


class Tactician(Hero):
    def __str__(self):
        return "Tactician"

    def __init__(self, name="Ornath"):
        super().__init__()
        self.name = name
        self.HP["max"] = 25
        self.strength["base"] = 12
        self.defense["base"] = 2
        self.conviction["base"] = 3
        self.magicDef["base"] = 16
        self.evasion["base"] = 12
        self.weaponSpeed["base"] = 20
        self.accuracy["base"] = 18
        self.speed["base"] = 7
        self.criticalRate["base"] = 2

        self.scouting["base"] = 10
        self.spirituality["base"] = 10
        self.charisma["base"] = 25
        self.perception["base"] = 25
        self.endurance["base"] = 60
        self.reflex["base"] = 25
        self.luck["base"] = 8


class Scout(Hero):
    def __str__(self):
        return "Scout"

    def __init__(self, name="Danae"):
        super().__init__()
        self.name = name
        self.HP["max"] = 25
        self.strength["base"] = 4
        self.defense["base"] = 0
        self.conviction["base"] = 2
        self.magicDef["base"] = 5
        self.evasion["base"] = 15
        self.weaponSpeed["base"] = 20
        self.accuracy["base"] = 25
        self.speed["base"] = 8
        self.criticalRate["base"] = 10

        self.scouting["base"] = 25
        self.spirituality["base"] = 15
        self.charisma["base"] = 20
        self.perception["base"] = 20
        self.endurance["base"] = 40
        self.reflex["base"] = 25
        self.luck["base"] = 5


class Vassal(Hero):
    def __str__(self):
        return "Vassal"

    def __init__(self, name="Thaddeus"):
        super().__init__()
        self.name = name
        self.HP["max"] = 20
        self.strength["base"] = 9
        self.defense["base"] = 0
        self.conviction["base"] = 15
        self.magicDef["base"] = 15
        self.evasion["base"] = 10
        self.weaponSpeed["base"] = 5
        self.accuracy["base"] = 20
        self.speed["base"] = 5
        self.criticalRate["base"] = 0

        self.scouting["base"] = 20
        self.spirituality["base"] = 25
        self.charisma["base"] = 20
        self.perception["base"] = 15
        self.endurance["base"] = 75
        self.reflex["base"] = 25
        self.luck["base"] = 30


class Messenger(Hero):
    def __str__(self):
        return "Messenger"

    def __init__(self, name="Barron"):
        super().__init__()
        self.name = name
        self.HP["max"] = 15
        self.strength["base"] = 5
        self.defense["base"] = 1
        self.conviction["base"] = 10
        self.magicDef["base"] = 15
        self.evasion["base"] = 13
        self.weaponSpeed["base"] = 5
        self.accuracy["base"] = 15
        self.speed["base"] = 15
        self.criticalRate["base"] = 0

        self.scouting = 20
        self.spirituality = 15
        self.charisma = 25
        self.perception = 15
        self.endurance = 55
        self.reflex = 25
        self.luck = 30


class Enemy(Character):
    identifyCounter = 0
    identifyPenalty = 0
    identifyValueList = [0, 0, 0]

    def __init__(self):
        Character.__init__(self)
        self.pluralName = ""
        self.trueName = ""
        self.pluralTrueName = ""
        self.contactStatus = []
        self.spellChance = 0

    def setEnemyDefaultValues(self):
        self.HP["current"] = self.HP["max"]
        if type(self).identifyCounter >= 1:
            self.name = self.trueName

    def beIdentified(self, identificationScore):
        identificationDiceRoll = random.randint(1, 50)
        identificationResult = identificationDiceRoll + identificationScore - type(self).identifyPenalty
        if identificationResult >= type(self).identifyValueList[2] or self.identifyCounter == 3:
            type(self).identifyCounter = max(type(self).identifyCounter, 3)
        elif identificationResult >= type(self).identifyValueList[1] or self.identifyCounter == 2:
            type(self).identifyCounter = max(type(self).identifyCounter, 2)
        elif identificationResult >= type(self).identifyValueList[0] or self.identifyCounter == 1:
            type(self).identifyCounter = max(type(self).identifyCounter, 1)
            printWithDelay("{} identified as a {}.".format(self.name, self.trueName))
        else:
            printWithDelay("You cannot identify the {}.".format(self.name))


class Goblin(Enemy):
    identifyCounter = 0
    identifyPenalty = 0
    identifyValueList = [0, 0, 0]

    def __init__(self, name="Armed Humanoid"):
        Enemy.__init__(self)
        self.name = name
        self.pluralName = "Armed Humanoids"
        self.trueName = "Goblin"
        self.pluralTrueName = "Goblins"
        self.HP["max"] = 18
        self.strength["base"] = 8
        self.defense["base"] = 3
        self.conviction["base"] = 1
        self.magicDef["base"] = 16
        self.evasion["base"] = 6
        self.accuracy["base"] = 8
        self.speed["base"] = 4
        self.criticalRate["base"] = 4
        self.experience = 6

    def checkIdentifyCounterForName(self):
        if self.identifyCounter > 0:
            self.name = self.trueName
            self.pluralName = self.pluralTrueName


class Hobgoblin(Enemy):
    identifyCounter = 0
    identifyPenalty = 0
    identifyValueList = [0, 0, 0]

    def __init__(self, name="Armed Humanoid"):
        Enemy.__init__(self)
        self.name = name
        self.pluralName = "Armed Humanoids"
        self.trueName = "Hobgoblin"
        self.pluralTrueName = "Hobgoblins"
        self.HP["max"] = 18
        self.strength["base"] = 8
        self.defense["base"] = 3
        self.conviction["base"] = 1
        self.magicDef["base"] = 16
        self.evasion["base"] = 6
        self.accuracy["base"] = 8
        self.speed["base"] = 4
        self.criticalRate["base"] = 4
        self.experience["base"] = 6

    def checkIdentifyCounterForName(self):
        if self.identifyCounter > 0:
            self.name = self.trueName
            self.pluralName = self.pluralTrueName
