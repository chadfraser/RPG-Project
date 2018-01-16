import random
import time
from collections import Counter
from operator import itemgetter
import Characters as Char


def checkIfAnyHeroesAlive(combatantList):
    for combatant in combatantList:
        if isinstance(combatant, Char.Hero) and not combatant.isIncapacitated():
            return True
    return False


def checkIfAnyEnemiesAlive(combatantList):
    for combatant in combatantList:
        if isinstance(combatant, Char.Enemy) and not combatant.isIncapacitated():
            return True
    return False


def getHeroReflex(character):
    if isinstance(character, Char.Hero):
        return character.reflex + random.randint(-5, 5)
    else:
        return character.speed * 2 + random.randint(-5, 5)


def chooseTarget(targetList):
    while True:
        Char.printWithDelay("Choose your target.")
        for index, target in enumerate(targetList):
            print("\t\t{}. {}".format(index + 1, target))
        print("\t\tc. Cancel")
        targetChosen = input()
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
            return int(targetChosen)
        elif targetChosen.lower() == "c":
            return None
        print("That is not a valid response.")
        time.sleep(1)


def determineFirstRoundInitiative(combatantList):
    clonedCombatantList = combatantList[:]
    randomInitiativeList = [getHeroReflex(char) for char in clonedCombatantList]
    unsortedCombatantTuple = zip(clonedCombatantList, randomInitiativeList)
    return sorted(unsortedCombatantTuple, key=itemgetter(1), reverse=True)


def addCharacterToInitiativeQueue(newCharacter, combatantListWithInitiative):
    combatantListWithInitiative = [(character[0], character[1] + 5) for character in combatantListWithInitiative]
    speedValue = newCharacter.speed + random.randint(-5, 5)
    combatantListWithInitiative.append((newCharacter, speedValue))
    return sorted(combatantListWithInitiative, key=itemgetter(1), reverse=True)


def printEnemyFormations(enemyList):
    ordinalDict = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    for enemy in enemyList:
        enemy.checkIdentifyCounterForName()
    enemyIdentityList = [(enemyTarget.name, enemyTarget.pluralName) for enemyTarget in enemyList]
    enemyCounter = Counter(enemyIdentityList)
    for enemyName, enemyQuantity in enemyCounter.items():
        if enemyQuantity == 1:
            print("{} {}".format(ordinalDict[enemyQuantity], enemyName[0]))
        else:
            print("{} {}".format(ordinalDict[enemyQuantity], enemyName[1]))


def selectTurnAction(actingHero, heroList, enemyList):
    listOfOptions = ["Attack", "Use a skill", "Use an item", "Run away", "Examine battlefield", "Pass turn"]
    while True:
        Char.printWithDelay("{}! Choose your action.".format(actingHero.name), 0.5)
        for index, option in enumerate(listOfOptions):
            print("\t\t{}. {}".format(index + 1, option))
        targetChosen = input()
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(listOfOptions):
            actionCompleted = applyTurnAction(actingHero, heroList, enemyList, int(targetChosen))
            if actionCompleted:
                break
        else:
            Char.printWithDelay("That is not a valid response.")


# Attack, skill, item, run result, examine

def applyTurnAction(actingHero, heroList, enemyList, actionChosen):
    turnCompleted = False
    if actionChosen == 1:
        livingEnemies = [enemy for enemy in enemyList if not enemy.isIncapacitated()]
        targetChosen = chooseTarget([enemy.name for enemy in livingEnemies])
        if targetChosen:
            actingHero.attackTarget(livingEnemies[targetChosen - 1])
            actingHero.actionCount += 1
            actingHero.checkCombatExhaustion()
            turnCompleted = True
    elif actionChosen == 2:
        pass  # turnCompleted = actingHero.selectAndCastSpell(heroList, enemyList)
    elif actionChosen == 3:
        pass  # turnCompleted = playerCurrentInventory.useItem(heroList + enemyList)
    elif actionChosen == 4:
        turnCompleted = attemptToRun(actingHero, enemyList)
    elif actionChosen == 5:
        examineBattlefield(heroList, enemyList)
    elif actionChosen == 6:
        Char.printWithDelay("{} passes.".format(actingHero.name), 0.5)
        turnCompleted = True
    return turnCompleted


def attemptToRun(actingHero, enemyList):
    if actingHero.shouldRun(enemyList):
        for enemy in enemyList:
            enemy.currentHP = 0
        Char.printWithDelay("Escaped!", 1.5)
    else:
        Char.printWithDelay("You couldn't escape!", 1.5)
        actingHero.actionCount += 1
        actingHero.checkCombatExhaustion()
    return True


def examineBattlefield(heroList, enemyList):
    for hero in heroList:
        print("{}'s HP: {} / {}".format(hero.name, hero.currentHP, hero.maxHP))
        heroStatusList = [statusEffect.name for statusEffect in hero.status]
        heroStatusString = ', '.join(heroStatusList)
        Char.printWithDelay("{}'s status: {}".format(hero.name, heroStatusString or 'Healthy'))
    livingUnidentifiedEnemyList = [enemyTarget for enemyTarget in enemyList if
                                   (not enemyTarget.isIncapacitated() and enemyTarget.name != enemyTarget.trueName)]
    livingIdentifiedEnemyList = [enemyTarget for enemyTarget in enemyList if
                                 (not enemyTarget.isIncapacitated() and enemyTarget.name == enemyTarget.trueName)]
    print()
    printEnemyFormations(livingUnidentifiedEnemyList)
    for livingEnemy in livingIdentifiedEnemyList:
        if livingEnemy.identifyCounter >= 3:
            Char.printWithDelay("{}'s HP: {} / {}".format(livingEnemy.name, livingEnemy.currentHP, livingEnemy.maxHP))
        else:
            Char.printWithDelay("{} (Appears {})".format(livingEnemy.name, "healthy" if
                                livingEnemy.currentHP / livingEnemy.maxHP >= 0.7 else "injured" if
                                livingEnemy.currentHP / livingEnemy.maxHP >= 0.2 else "dying"))
    Char.printWithDelay("", 1.5)


def startCombat(heroList, enemyList):
    for enemy in enemyList:
        enemy.setEnemyDefaultValues()
    for hero in heroList:
        hero.setHeroDefaultValues()
    listOfCombatants = [hero for hero in heroList if not hero.isIncapacitated()] + [enemy for enemy in enemyList if not
                                                                                    enemy.isIncapacitated()]
    battleInProgress = True
    initiativeList = determineFirstRoundInitiative(listOfCombatants)
    while battleInProgress:
        currentActingCombatant = initiativeList[0][0]
        del(initiativeList[0])
        if currentActingCombatant.isIncapacitated():
            continue
        elif isinstance(currentActingCombatant, Char.Hero):
            selectTurnAction(currentActingCombatant, heroList, enemyList)
            initiativeList = addCharacterToInitiativeQueue(currentActingCombatant, initiativeList)
        elif isinstance(currentActingCombatant, Char.Enemy):
            livingHeroes = [hero for hero in heroList if not hero.isIncapacitated()]
            targetChosen = random.choice(livingHeroes)
            currentActingCombatant.attackTarget(targetChosen)
            initiativeList = addCharacterToInitiativeQueue(currentActingCombatant, initiativeList)
        if not checkIfAnyEnemiesAlive(listOfCombatants) or not checkIfAnyHeroesAlive(listOfCombatants):
            battleInProgress = False
            for hero in heroList:
                hero.actionCount = 0
                hero.setHeroDefaultValues()


hero1 = Char.Fencer()
hero2 = Char.Healer()
enemy1 = Char.Goblin()
enemy2 = Char.Goblin()
enemy3 = Char.Hobgoblin()

heroes = [hero1, hero2]
enemies = [enemy1, enemy2, enemy3]
hero1.currentHP = hero1.maxHP
hero2.currentHP = hero2.maxHP
hero1.luck = hero1.defense = hero1.currentHP = 100
hero1.endurance = 1
Char.Hobgoblin.identifyCounter = 3
startCombat(heroes, enemies)
