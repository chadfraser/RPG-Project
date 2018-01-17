import Characters as Char
import Combat
import Skills


# USE FOR TESTING PURPOSES ONLY

hero1 = Char.Fencer()
hero2 = Char.Healer()
enemy1 = Char.Goblin()
enemy2 = Char.Goblin()
enemy3 = Char.Hobgoblin()

heroes = [hero1, hero2]
enemies = [enemy1, enemy2, enemy3]
hero1.HP["current"] = hero1.HP["max"]
hero2.HP["current"] = hero2.HP["max"]
hero1.reflex["base"] = 20
hero1.speed["base"] = -10
hero1.evasion["base"] += 150
hero1.luck["base"] = hero1.defense["base"] = 100
hero1.endurance["base"] = 1
Char.Hobgoblin.identifyCounter = 3
hero1.knownSkills.append(Skills.DodgeThrough())
hero2.knownSkills.append(Skills.Defend())
hero1.knownSkills.append(Skills.Parry())
Combat.startCombat(heroes, enemies)
