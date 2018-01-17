import random
import Characters as Char
import Combat


class Skill:
    def __init__(self):
        self.name = ""
        self.startOfTurn = False
        self.onEnemyAttack = False
        self.afterEnemyAttack = False
        self.cost = 0
        self.level = 1


class Identify(Skill):
    def __init__(self):
        super().__init__()
        self.name = "Identify"
        self.identifyWeaponScore = 0
        self.identifyArmorScore = 0
        self.identifyEnemyScore = 0
        self.cost = 2

    def identifyWeapon(self, heroList):
        weaponList = []
#        weaponList = [equip for hero in heroList for equip in hero.equipment if isinstance(equip, Weapon)]
        while True:
            Char.printWithDelay("Which weapon would you like to attempt to identify?")
            for index, target in enumerate(weaponList):
                print("\t\t{}. {}".format(index + 1, target.name))
            print("\t\tc. Cancel")
            targetChosen = input()
            if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(weaponList):
                weaponList[int(targetChosen) - 1].beIdentified(self.identifyWeaponScore)
                return True
            elif targetChosen.lower() == "c":
                return False
            Char.printWithDelay("That is not a valid response.")

    def identifyArmor(self, heroList):
        armorList = []
#        armorList = [equip for hero in heroList for equip in hero.equipment if isinstance(equip, Armor)]
        while True:
            Char.printWithDelay("Which armor would you like to attempt to identify?")
            for index, target in enumerate(armorList):
                print("\t\t{}. {}".format(index + 1, target.name))
            print("\t\tc. Cancel")
            targetChosen = input()
            if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(armorList):
                armorList[int(targetChosen) - 1].beIdentified(self.identifyArmorScore)
                return True
            elif targetChosen.lower() == "c":
                return False
            Char.printWithDelay("That is not a valid response.")

    def identifyEnemy(self, enemyList):
        while True:
            Char.printWithDelay("Which enemy would you like to attempt to identify?")
            for index, target in enumerate(enemyList):
                print("\t\t{}. {}".format(index + 1, target.name))
            print("\t\tc. Cancel")
            targetChosen = input()
            if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(enemyList):
                enemyList[int(targetChosen) - 1].beIdentified(self.identifyEnemyScore)
                return True
            elif targetChosen.lower() == "c":
                return False
            Char.printWithDelay("That is not a valid response.")

    def useSkill(self, actingHero, heroList, enemyList):
        while True:
            Char.printWithDelay("What would you like to attempt to identify?")
            print("\t\t1. Enemy")
            print("\t\t2. Weapon")
            print("\t\t3. Armor")
            print("\t\tc. Cancel")
            targetChosen = input()
            if targetChosen == "1":
                identifyCompleted = self.identifyEnemy(enemyList)
                return identifyCompleted
            elif targetChosen == "2":
                identifyCompleted = self.identifyWeapon(heroList)
                return identifyCompleted
            elif targetChosen == "3":
                identifyCompleted = self.identifyArmor(heroList)
                return identifyCompleted
            elif targetChosen.lower() == "c":
                return False
            Char.printWithDelay("That is not a valid response.")


class Defend(Skill):
    def __init__(self):
        super().__init__()
        self.name = "Defend"
        self.startOfTurn = True
        self.power = 1
        self.defensiveBonus = 1
        self.turnCount = 0
        self.cost = 2

    def useSkill(self, actingHero, heroList, enemyList):
        self.turnCount = 1
        self.defensiveBonus = self.power + random.randint(0, 2)
        actingHero.activeSkills.append(self)
        Char.printWithDelay("{} takes a defensive stance.".format(actingHero.name))
        actingHero.defense["modified"] += self.defensiveBonus
        actingHero.actionCount += 1
        actingHero.checkCombatExhaustion()
        return True

    def startOfTurnEffect(self, actingHero, heroList, enemyList):
        self.turnCount -= 1
        if self.turnCount == 0:
            actingHero.defense["modified"] -= self.defensiveBonus
            return False
        return True


class Parry(Skill):
    def __init__(self):
        super().__init__()
        self.name = "Parry"
        self.startOfTurn = True
        self.afterEnemyAttack = True
        self.turnCount = 0
        self.parryCount = 0
        self.cost = 5

    def useSkill(self, actingHero, heroList, enemyList):
        livingEnemies = [enemy for enemy in enemyList if not enemy.isIncapacitated()]
        targetChosen = Combat.chooseTarget([enemy.name for enemy in livingEnemies])
        if targetChosen:
            targetEnemy = livingEnemies[targetChosen - 1]
            self.turnCount = 1
            self.parryCount += 3
            actingHero.printAttackTarget(targetEnemy)
            self.parryAttack(actingHero, targetEnemy)
            actingHero.activeSkills.append(self)
            actingHero.actionCount += 1
            actingHero.checkCombatExhaustion()
            return True
        return False

    def parryAttack(self, actingHero, targetEnemy):
        if self.parryCount:
            tempDamage = actingHero.strength["modified"]
            actingHero.modifiedDamage = max(1, round(actingHero.strength["modified"] * 0.75))
            actingHero.attackTarget(targetEnemy)
            actingHero.strength["modified"] = tempDamage
            actingHero.aggression += 1
            self.parryCount -= 1

    def startOfTurnEffect(self, actingHero, heroList, enemyList):
        self.turnCount -= 1
        if self.turnCount == 0:
            self.parryCount = 0
            return False
        return True

    def afterEnemyAttackEffect(self, actingHero, heroList, enemyList, attackingEnemy, attackTarget):
        if not actingHero.isIncapacitated() and self.parryCount:
            Char.printWithDelay("{} counterattacks!".format(actingHero.name))
            self.parryAttack(actingHero,attackingEnemy)
        return True


class DodgeThrough(Skill):
    def __init__(self):
        super().__init__()
        self.name = "Dodge Through"
        self.startOfTurn = True
        self.onEnemyAttack = True
        self.afterEnemyAttack = True
        self.power = 2
        self.evasionBonus = 0
        self.storedHP = 0
        self.turnCount = 0
        self.cost = 5

    def useSkill(self, actingHero, heroList, enemyList):
        self.turnCount = 1
        self.evasionBonus = self.power + random.randint(0, 4)
        actingHero.activeSkills.append(self)
        Char.printWithDelay("{} prepares to dodge.".format(actingHero.name))
        actingHero.evasion["modified"] += self.evasionBonus
        actingHero.actionCount += 1
        actingHero.checkCombatExhaustion()
        return True

    def startOfTurnEffect(self, actingHero, heroList, enemyList):
        self.turnCount -= 1
        if self.turnCount == 0:
            actingHero.evasion["modified"] -= self.evasionBonus
            self.storedHP = 0
            return False
        return True

    def onEnemyAttackEffect(self, actingHero, heroList, enemyList, attackingEnemy, attackTarget):
        if actingHero is attackTarget:
            self.storedHP = actingHero.HP["current"]
        return True

    def afterEnemyAttackEffect(self, actingHero, heroList, enemyList, attackingEnemy, attackTarget):
        if actingHero is attackTarget:
            if not actingHero.isIncapacitated() and actingHero.HP["current"] == self.storedHP and len(enemyList) > 1:
                remainingEnemyList = [enemy for enemy in enemyList if enemy is not attackingEnemy]
                targetEnemy = random.choice(remainingEnemyList)
                Char.printWithDelay("{} redirects {}'s attack to {}!".format(actingHero.name, attackingEnemy.name,
                                                                             targetEnemy.name), 2)
                attackingEnemy.attackTarget(targetEnemy)
                self.storedHP = 0
                return False


class Skillet(Skill):
    pass
