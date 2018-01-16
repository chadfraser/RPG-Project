import random
import time

# HP, strength, defense, critical hit chance
# Spell cool down, casting duration, magic defense
# First turn reaction, speed, agility, run chance

# In combat spells. Camping/preparatory skills. Out of combat support skills.
# FIRE, PARRY       SET TRAPS, HIDE             IDENTIFY ARMOR, BREAK CURSE
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
        self.maxHP = 0
        self.currentHP = self.maxHP
        self.damage = 0
        self.defense = 0
        self.intelligence = 0
        self.magicDef = 0
        self.evasion = 0
        self.accuracy = 0
        self.speed = 0
        self.criticalRate = 0
        self.strikeCount = 1

        self.weakness = []
        self.resistance = []
        self.status = []
        self.equipment = []
        self.contactElement = []
        self.experience = 0

        self.currentDamage = self.damage
        self.currentDefense = self.defense
        self.currentMagicDefense = self.magicDef
        self.currentEvasion = self.evasion
        self.currentAccuracy = self.accuracy
        self.currentCriticalRate = self.criticalRate
        self.currentStrikeCount = self.strikeCount

    def attackTarget(self, target):
        timesAttackDone = 0
        while timesAttackDone < self.strikeCount:
            if self.shouldAttackHit(target):
                damage, wasCritical = self.determineDamage(target)
                target.applyDamage(damage, wasCritical)
                if target.isIncapacitated():
                    target.printDeathMessage()
                    break
            else:
                self.printAttackMiss()
            timesAttackDone += 1

    def shouldAttackHit(self, target):
        toHitFormula = 160 + self.accuracy - target.evasion
        randomCheckToHit = random.randint(1, 200)
        if randomCheckToHit <= toHitFormula:
            return True
        return False

    def shouldCriticalHit(self):
        criticalHitDiceRoll = random.randint(1, 200)
        if criticalHitDiceRoll <= self.criticalRate:
            return True
        return False

    def determineDamage(self, target):
        penetratedDamage = random.randint(self.damage - target.defense, (2 * self.damage) - target.defense)
        damage = max(1, penetratedDamage)
        wasCritical = self.shouldCriticalHit()
        if wasCritical:
            damage += random.randint(self.damage, 2 * self.damage)
        finalDamage = target.applyWeaknessAndResistance(damage, self.contactElement)
        return finalDamage, wasCritical

    def applyDamage(self, damage, wasCritical=False):
        self.currentHP -= damage
        self.printDamageAndCritical(damage, wasCritical)
        if self.currentHP <= 0:
            self.currentHP = 0
        if isinstance(self, Hero):
            self.printCurrentHP()

    def isIncapacitated(self):
        if self.currentHP <= 0:
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
            damage = damage // 2
        return damage

    # Prints the damage dealt, and if the attack was a critical hit
    def printDamageAndCritical(self, damage, wasCritical):
        if wasCritical:
            printWithDelay("--Critical hit!")
        printWithDelay("--{} takes {} damage.".format(self.name, damage))

    # Prints the character's current HP
    def printCurrentHP(self):
        printWithDelay("--{}'s HP is now {}.".format(self.name, self.currentHP))

    # Prints that the target was killed
    def printDeathMessage(self):
        printWithDelay("--{} has fallen.".format(self.name))

    def printAttackMiss(self):
        printWithDelay("--{} missed!".format(self.name))

    def printAmountHealed(self, healHPValue):
        printWithDelay("--{} healed {} HP!".format(self.name, healHPValue))


class Hero(Character):
    def __init__(self):
        Character.__init__(self)
        self.strength = 0
        self.damage = max(1, self.strength // 2)
        self.armor = 0
        self.defense = self.armor
        self.agility = 0
        self.evasion = self.agility
        self.weaponSpeed = 0
        self.strikeCount = 1 + self.weaponSpeed // 32
        self.scouting = 0
        self.spirituality = 0
        self.charisma = 0
        self.perception = 0
        self.endurance = 0
        self.exhaustion = 0
        self.reflex = 0
        self.luck = 0
        self.level = 1
        self.actionCount = 0
        self.encounterCount = 0

        self.modifiedDamage = self.damage
        self.modifiedDefense = self.defense
        self.modifiedIntelligence = self.intelligence
        self.modifiedMagicDefense = self.magicDef
        self.modifiedEvasion = self.evasion
        self.modifiedStrikeCount = self.strikeCount
        self.modifiedAccuracy = self.accuracy
        self.modifiedSpeed = self.speed
        self.modifiedCriticalRate = self.criticalRate
        self.modifiedScouting = self.scouting
        self.modifiedSpirituality = self.spirituality
        self.modifiedCharisma = self.charisma
        self.modifiedPerception = self.perception
        self.modifiedEndurance = self.endurance
        self.modifiedReflex = self.reflex
        self.modifiedLuck = self.luck

        self.exhaustionDamage = self.damage
        self.exhaustionDefense = self.defense
        self.exhaustionIntelligence = self.intelligence
        self.exhaustionMagicDefense = self.magicDef
        self.exhaustionEvasion = self.evasion
        self.exhaustionStrikeCount = self.strikeCount
        self.exhaustionAccuracy = self.accuracy
        self.exhaustionSpeed = self.speed
        self.exhaustionCriticalRate = self.criticalRate
        self.exhaustionScouting = self.scouting
        self.exhaustionSpirituality = self.spirituality
        self.exhaustionCharisma = self.charisma
        self.exhaustionPerception = self.perception
        self.exhaustionReflex = self.reflex
        self.exhaustionLuck = self.luck

    def setHeroDefaultValues(self):
        self.modifiedDamage = max(1, self.strength // 2) + self.exhaustionDamage
        self.modifiedDefense = self.armor + self.exhaustionDefense
        self.modifiedIntelligence = self.intelligence + self.exhaustionIntelligence
        self.modifiedMagicDefense = self.magicDef + self.exhaustionMagicDefense
        self.modifiedEvasion = self.agility + self.exhaustionEvasion
        self.modifiedStrikeCount = 1 + self.weaponSpeed // 32 + self.exhaustionStrikeCount
        self.modifiedAccuracy = self.accuracy + self.exhaustionAccuracy
        self.modifiedSpeed = self.speed + self.exhaustionSpeed
        self.modifiedCriticalRate = self.criticalRate + self.exhaustionCriticalRate
        self.modifiedScouting = self.scouting + self.exhaustionScouting
        self.modifiedSpirituality = self.spirituality + self.exhaustionSpirituality
        self.modifiedCharisma = self.charisma + self.exhaustionCharisma
        self.modifiedPerception = self.perception + self.exhaustionPerception
        self.modifiedEndurance = self.endurance
        self.modifiedReflex = self.reflex + self.exhaustionReflex
        self.modifiedLuck = self.luck + self.exhaustionLuck

    def applyStatVarianceOnInitialization(self):
        self.maxHP = max(1, self.maxHP + random.randint(-5, 5))
        self.strength = max(1, self.maxHP + random.randint(-3, 3))
        self.armor = max(0, self.maxHP + random.randint(0, 3))
        self.intelligence = max(1, self.maxHP + random.randint(-3, 3))
        self.magicDef = max(0, self.maxHP + random.randint(-3, 3))
        self.agility = max(1, self.maxHP + random.randint(-5, 5))
        self.weaponSpeed = max(1, self.maxHP + random.randint(-2, 2))
        self.accuracy = max(1, self.maxHP + random.randint(-3, 3))
        self.speed = max(1, self.maxHP + random.randint(-2, 2))
        self.criticalRate = max(0, self.maxHP + random.randint(0, 2))
        self.scouting = max(1, self.maxHP + random.randint(-5, 5))
        self.spirituality = max(1, self.maxHP + random.randint(-5, 5))
        self.charisma = max(1, self.maxHP + random.randint(-5, 5))
        self.perception = max(1, self.maxHP + random.randint(-5, 5))
        self.endurance = max(1, self.maxHP + random.randint(-10, 10))
        self.reflex = max(1, self.maxHP + random.randint(-5, 5))
        self.luck = max(1, self.maxHP + random.randint(-5, 5))

    def checkCombatExhaustion(self):
        exhaustionDiceRoll = 0
        for __ in range(self.actionCount):
            exhaustionDiceRoll += random.randint(1, 20)
        if exhaustionDiceRoll > self.endurance:
            self.sufferExhaustion()
            self.actionCount = 0

    def checkEncounterExhaustion(self):
        exhaustionDiceRoll = 0
        for __ in range(self.encounterCount):
            exhaustionDiceRoll += random.randint(1, 20)
        if exhaustionDiceRoll > self.endurance:
            self.sufferExhaustion()
            self.encounterCount = 0

    def sufferExhaustion(self):
        self.exhaustion += 1
        lowValueExhaustionStats = [self.exhaustionDamage, self.exhaustionIntelligence, self.exhaustionMagicDefense,
                                   self.exhaustionAccuracy, self.exhaustionDefense, self.exhaustionStrikeCount,
                                   self.exhaustionCriticalRate]
        highValueExhaustionStats = [self.exhaustionEvasion, self.exhaustionSpeed, self.exhaustionScouting,
                                    self.exhaustionSpirituality, self.exhaustionLuck, self.exhaustionCharisma,
                                    self.exhaustionPerception, self.exhaustionReflex]
        lowValueStatPenalty = [(random.randint(1, 4) if self.exhaustion + random.randint(1, 10) >= 8 else 0)
                               for _ in range(7)]
        highValueStatPenalty = [(random.randint(1, 3) if self.exhaustion + random.randint(1, 10) >= 8 else 0)
                                for _ in range(8)]

        self.exhaustionDamage, self.exhaustionIntelligence, self.exhaustionMagicDefense, self.exhaustionAccuracy, \
            self.exhaustionDefense, self.exhaustionStrikeCount,\
            self.exhaustionCriticalRate = [x - y for x, y in zip(lowValueExhaustionStats, lowValueStatPenalty)]

        self.exhaustionEvasion, self.exhaustionSpeed, self.exhaustionScouting, self.exhaustionSpirituality, \
            self.exhaustionLuck, self.exhaustionCharisma, self.exhaustionPerception,\
            self.exhaustionReflex = [x - y for x, y in zip(highValueExhaustionStats, highValueStatPenalty)]
        printWithDelay("{} is becoming exhausted!".format(self.name), 2)

    def shouldRun(self, listOfEnemies):
        listOfEnemyEvasion = [enemy.evasion for enemy in listOfEnemies if not enemy.isIncapacitated()]
        maxEnemyEvasion = max(listOfEnemyEvasion)
        runningDiceRoll = random.randint(0, 2 * maxEnemyEvasion)
        if self.luck > runningDiceRoll:
            return True
        return False


class Fencer(Hero):
    def __str__(self):
        return "Fencer"

    def __init__(self, name="Cousland"):
        super().__init__()
        self.name = name
        self.maxHP = 30
        self.strength = 13
        self.armor = 3
        self.intelligence = 5
        self.magicDef = 10
        self.agility = 15
        self.weaponSpeed = 15
        self.accuracy = 15
        self.speed = 15
        self.criticalRate = 0

        self.scouting = 5
        self.spirituality = 15
        self.charisma = 5
        self.perception = 15
        self.endurance = 40
        self.reflex = 10
        self.luck = 5


class Hunter(Hero):
    def __str__(self):
        return "Hunter"

    def __init__(self, name="Eliza"):
        super().__init__()
        self.name = name
        self.maxHP = 30
        self.strength = 15
        self.armor = 1
        self.intelligence = 1
        self.magicDef = 5
        self.agility = 7
        self.weaponSpeed = 20
        self.accuracy = 15
        self.speed = 8
        self.criticalRate = 0

        self.scouting = 25
        self.spirituality = 20
        self.charisma = 10
        self.perception = 15
        self.endurance = 60
        self.reflex = 25
        self.luck = 1


class Archer(Hero):
    def __str__(self):
        return "Archer"

    def __init__(self, name="Oakwood"):
        super().__init__()
        self.name = name
        self.maxHP = 30
        self.strength = 13
        self.armor = 0
        self.intelligence = 20
        self.magicDef = 5
        self.agility = 12
        self.weaponSpeed = 20
        self.accuracy = 25
        self.speed = 10
        self.criticalRate = 2

        self.scouting = 15
        self.spirituality = 5
        self.charisma = 20
        self.perception = 25
        self.endurance = 40
        self.reflex = 5
        self.luck = 5


class Mage(Hero):
    def __str__(self):
        return "Mage"

    def __init__(self, name="Canin"):
        super().__init__()
        self.name = name
        self.maxHP = 15
        self.strength = 5
        self.armor = 0
        self.intelligence = 20
        self.magicDef = 20
        self.agility = 12
        self.weaponSpeed = 5
        self.accuracy = 10
        self.speed = 8
        self.criticalRate = 0

        self.scouting = 15
        self.spirituality = 5
        self.charisma = 10
        self.perception = 20
        self.endurance = 45
        self.reflex = 15
        self.luck = 10


class Druid(Hero):
    def __str__(self):
        return "Druid"

    def __init__(self, name="Serena"):
        super().__init__()
        self.name = name
        self.maxHP = 25
        self.strength = 10
        self.armor = 2
        self.intelligence = 18
        self.magicDef = 7
        self.agility = 12
        self.weaponSpeed = 15
        self.accuracy = 20
        self.speed = 5
        self.criticalRate = 0

        self.scouting = 25
        self.spirituality = 25
        self.charisma = 15
        self.perception = 5
        self.endurance = 55
        self.reflex = 25
        self.luck = 1


class Summoner(Hero):
    def __str__(self):
        return "Summoner"

    def __init__(self, name="Goldwall"):
        super().__init__()
        self.name = name
        self.maxHP = 25
        self.strength = 10
        self.armor = 1
        self.intelligence = 17
        self.magicDef = 5
        self.agility = 10
        self.weaponSpeed = 14
        self.accuracy = 15
        self.speed = 8
        self.criticalRate = 0

        self.scouting = 20
        self.spirituality = 15
        self.charisma = 25
        self.perception = 10
        self.endurance = 45
        self.reflex = 25
        self.luck = 10


class Healer(Hero):
    def __str__(self):
        return "Healer"

    def __init__(self, name="Heaylin"):
        super().__init__()
        self.name = name
        self.maxHP = 20
        self.strength = 5
        self.armor = 3
        self.intelligence = 10
        self.magicDef = 10
        self.agility = 10
        self.weaponSpeed = 18
        self.accuracy = 20
        self.speed = 15
        self.criticalRate = 4

        self.scouting = 15
        self.spirituality = 20
        self.charisma = 15
        self.perception = 20
        self.endurance = 40
        self.reflex = 0
        self.luck = 15


class Apprentice(Hero):
    def __str__(self):
        return "Apprentice"

    def __init__(self, name="Rosalin"):
        super().__init__()
        self.name = name
        self.maxHP = 15
        self.strength = 10
        self.armor = 0
        self.intelligence = 20
        self.magicDef = 15
        self.agility = 15
        self.weaponSpeed = 16
        self.accuracy = 18
        self.speed = 5
        self.criticalRate = 0

        self.scouting = 10
        self.spirituality = 25
        self.charisma = 20
        self.perception = 20
        self.endurance = 60
        self.reflex = 5
        self.luck = 10


class Scholar(Hero):
    def __str__(self):
        return "Scholar"

    def __init__(self, name="Flynn"):
        super().__init__()
        self.name = name
        self.maxHP = 20
        self.strength = 12
        self.armor = 0
        self.intelligence = 15
        self.magicDef = 20
        self.agility = 7
        self.weaponSpeed = 14
        self.accuracy = 15
        self.speed = 8
        self.criticalRate = 0

        self.scouting = 5
        self.spirituality = 5
        self.charisma = 25
        self.perception = 25
        self.endurance = 40
        self.reflex = 25
        self.luck = 10


class Guard(Hero):
    def __str__(self):
        return "Guard"

    def __init__(self, name="Bagsword"):
        super().__init__()
        self.name = name
        self.maxHP = 40
        self.strength = 8
        self.armor = 4
        self.intelligence = 10
        self.magicDef = 15
        self.agility = 5
        self.weaponSpeed = 15
        self.accuracy = 10
        self.speed = 4
        self.criticalRate = 0

        self.scouting = 20
        self.spirituality = 15
        self.charisma = 5
        self.perception = 15
        self.endurance = 70
        self.reflex = 0
        self.luck = 1


class SiegeMan(Hero):
    def __str__(self):
        return "Siege Man"

    def __init__(self, name="Saba"):
        super().__init__()
        self.name = name
        self.maxHP = 35
        self.strength = 10
        self.armor = 4
        self.intelligence = 6
        self.magicDef = 20
        self.agility = 5
        self.weaponSpeed = 5
        self.accuracy = 20
        self.speed = 1
        self.criticalRate = 0

        self.scouting = 5
        self.spirituality = 20
        self.charisma = 15
        self.perception = 5
        self.endurance = 75
        self.reflex = 5
        self.luck = 1


class Tactician(Hero):
    def __str__(self):
        return "Tactician"

    def __init__(self, name="Ornath"):
        super().__init__()
        self.name = name
        self.maxHP = 25
        self.strength = 12
        self.armor = 2
        self.intelligence = 3
        self.magicDef = 16
        self.agility = 12
        self.weaponSpeed = 20
        self.accuracy = 18
        self.speed = 7
        self.criticalRate = 2

        self.scouting = 10
        self.spirituality = 10
        self.charisma = 25
        self.perception = 25
        self.endurance = 60
        self.reflex = 25
        self.luck = 8


class Scout(Hero):
    def __str__(self):
        return "Scout"

    def __init__(self, name="Danae"):
        super().__init__()
        self.name = name
        self.maxHP = 25
        self.strength = 4
        self.armor = 0
        self.intelligence = 2
        self.magicDef = 5
        self.agility = 15
        self.weaponSpeed = 20
        self.accuracy = 25
        self.speed = 8
        self.criticalRate = 10

        self.scouting = 25
        self.spirituality = 15
        self.charisma = 20
        self.perception = 20
        self.endurance = 40
        self.reflex = 25
        self.luck = 5


class Vassal(Hero):
    def __str__(self):
        return "Vassal"

    def __init__(self, name="Thaddeus"):
        super().__init__()
        self.name = name
        self.maxHP = 20
        self.strength = 9
        self.armor = 0
        self.intelligence = 15
        self.magicDef = 15
        self.agility = 10
        self.weaponSpeed = 5
        self.accuracy = 20
        self.speed = 5
        self.criticalRate = 0

        self.scouting = 20
        self.spirituality = 25
        self.charisma = 20
        self.perception = 15
        self.endurance = 75
        self.reflex = 25
        self.luck = 30


class Messenger(Hero):
    def __str__(self):
        return "Messenger"

    def __init__(self, name="Barron"):
        super().__init__()
        self.name = name
        self.maxHP = 15
        self.strength = 5
        self.armor = 1
        self.intelligence = 10
        self.magicDef = 15
        self.agility = 13
        self.weaponSpeed = 5
        self.accuracy = 15
        self.speed = 15
        self.criticalRate = 0

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
        self.currentHP = self.maxHP
        self.contactStatus = []
        self.spellChance = 0

    def setEnemyDefaultValues(self):
        self.currentHP = self.maxHP
        if type(self).identifyCounter >= 1:
            self.name = self.trueName

    def beIdentified(self, identificationScore):
        identificationDiceRoll = random.randint(1, 50)
        identificationResult = identificationDiceRoll + identificationScore - type(self).identifyPenalty
        if identificationResult >= type(self).identifyValueList[2]:
            type(self).identifyCounter = max(type(self).identifyCounter, 3)
        elif identificationResult >= type(self).identifyValueList[1]:
            type(self).identifyCounter = max(type(self).identifyCounter, 2)
        elif identificationResult >= type(self).identifyValueList[0]:
            type(self).identifyCounter = max(type(self).identifyCounter, 1)
            printWithDelay("{} identified as a {}.".format(self.name, self.trueName))
        else:
            pass


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
        self.maxHP = 18
        self.damage = 8
        self.defense = 3
        self.intelligence = 1
        self.magicDef = 16
        self.evasion = 6
        self.accuracy = 8
        self.speed = 4
        self.criticalRate = 4
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
        self.maxHP = 18
        self.damage = 8
        self.defense = 3
        self.intelligence = 1
        self.magicDef = 16
        self.evasion = 6
        self.accuracy = 8
        self.speed = 4
        self.criticalRate = 4
        self.experience = 6

    def checkIdentifyCounterForName(self):
        if self.identifyCounter > 0:
            self.name = self.trueName
            self.pluralName = self.pluralTrueName
