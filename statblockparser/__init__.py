from pyparsing import *

ParserElement.setDefaultWhitespaceChars(" \t")
ParentheticalRE = Optional(Regex("\(.*?\)"))
NL = ParentheticalRE + LineEnd().suppress()
END = StringEnd()
SignedInteger = pyparsing_common.signed_integer
Integer = pyparsing_common.integer
Comma = Literal(",").suppress()
SemiColon = Literal(";").suppress()
SkipRest = Suppress(restOfLine) + NL
Divider = Literal("--------------------")
NextSection = SkipTo(Divider | END)
NameRE = Regex("[^\n,]+").setParseAction(lambda s, l, t: t[0].strip())
NamedList = delimitedList(NameRE, delim=",")

# Basics content
"""
Gwendolyn Gwynne
Female human (Garundi) druid 9
N Medium humanoid (human)
Init +2; Senses Perception +12
"""
# Line 1
CharacterName = restOfLine.setParseAction(lambda s, l, t: t[0].split("CR")[0].strip())
NameLine = CharacterName("character_name") + NL

XPLine = Literal("XP") + restOfLine + NL

# Line 2
Genders = (Literal("Female") | Literal("Male"))
Race = OneOrMore(Word(alphas)).setParseAction(lambda s, l, t: " ".join(t))
RaceAndNationality = Race("race") + Suppress(Optional(ParentheticalRE))
Class = OneOrMore(Word(alphas)).setParseAction(lambda s, l, t: " ".join(t))
Level = Word(nums)
ClassLevel = Group(Class("class") + Suppress(Optional(ParentheticalRE)) + Level("level"))
Classes = delimitedList(ClassLevel, delim="/")
GRCLine = Genders("gender") + RaceAndNationality + Classes("classes") + NL

# Line 3
# Alignment
Chaotic = Literal("C")("chaotic")
Lawful = Literal("L")("lawful")
Evil = Literal("E")("evil")
Good = Literal("G")("good")
Neutral = Literal("N")("neutral")
Legal = (Chaotic | Lawful)
Moral = (Evil | Good | Neutral)
Alignment = Group(Optional(Legal) + Moral)
Sizes = (Literal("Diminutive") | Literal("Tiny") | Literal("Small") | Literal("Medium") | Literal("Large") | Literal("Huge") | Literal("Gargantuan"))
ASTLine = Alignment("alignment") + Sizes("size") + restOfLine + NL

# Line 4
Initiative = Suppress(Literal("Init")) + SignedInteger("initiative")
Perception = Suppress(Literal("Perception")) + SignedInteger("perception")
InitLine = Initiative + SkipTo(Perception, include=True) + NL

Basics = NameLine + Optional(XPLine) + GRCLine + ASTLine + InitLine + NextSection

# Defense
"""
--------------------
Defense
--------------------
AC 20, touch 12, flat-footed 18 (+8 armor, +2 Dex)
hp 75 (9d8+27)
Fort +9, Ref +6, Will +15; +4 vs. fey and plant-targeted effects
Immune poison"""
DefenseHeader = Divider + NL + "Defense" + NL + Divider + NL

# Line 1
AC = Suppress(Literal("AC")) + SignedInteger("ac") + Comma
TouchAC = Literal("touch") + SignedInteger("touch_ac") + Comma
FlatFootedAC = Literal("flat-footed") + SignedInteger("flat_footed_ac")
ACLine = AC + TouchAC + FlatFootedAC + Suppress(restOfLine) + NL

# Line 2
HPLine = Literal("hp") + SignedInteger("hp") + Suppress(restOfLine) + NL

# Line 3
FortSave = Suppress(Literal("Fort")) + SignedInteger("fort_save") + Comma
ReflexSave = Suppress(Literal("Ref")) + SignedInteger("reflex_save") + Comma
WillSave = Suppress(Literal("Will")) + SignedInteger("will_save")
OtherSaves = Suppress(Literal(";")) + restOfLine("other_saves")
SaveLine = FortSave + ReflexSave + WillSave + Optional(OtherSaves) + NL

Defense = Suppress(DefenseHeader) + ACLine + HPLine + SaveLine + Suppress(NextSection)

# Offense
"""
--------------------
Offense
--------------------
Speed 30 ft. (20 ft. in armor)
Melee hope knife +5/+0 (1d4-2/19-20) or
   quarterstaff of entwined serpents +5/+0 (1d6-1) or
   scimitar +4/-1 (1d6-2/18-20)
Special Attacks wild shape 3/day
Druid Spells Prepared (CL 9th; concentration +18)
   5th—control winds (DC 22), cure critical wounds
   4th—air walk, cure serious wounds, dispel magic
   3rd—cure moderate wounds, hide campsite[APG] (DC 20), ice spears (DC 21), greater magic fang, protection from energy
   2nd—barkskin, bull"s strength, delay poison, flaming sphere (DC 19), flurry of snowballs (DC 19), reduce animal
   1st—ant haul[APG] (DC 18), cure light wounds, entangle (DC 18), entangle (DC 18), faerie fire, longstrider
   0 (at will)—create water, detect magic, light, stabilize
"""
OffenseHeader = Divider + NL + "Offense" + NL + Divider + NL

# Line 1
Speed = Suppress(Literal("Speed")) + SignedInteger("speed") + Suppress(Literal("ft."))
ArmorSpeed = Suppress(Literal("(")) + SignedInteger("speed_in_armor") + Suppress(Literal("ft.") + Literal("in") + Literal ("armor") + Literal(")"))
SpeedLine = Speed + Optional(ArmorSpeed) + NL

Offense = Suppress(OffenseHeader) + SpeedLine + Suppress(NextSection)

# Statistics
"""
--------------------
Statistics
--------------------
Str 7, Dex 14, Con 14, Int 11, Wis 24, Cha 7
Base Atk +6; CMB +4; CMD 16
Feats Augment Summoning, Eschew Materials, Extend Spell, Natural Spell, Scribe Scroll, Spell Focus (conjuration)
Traits focused mind, trunau native
Skills Acrobatics +2 (-2 to jump), Climb +3, Fly +8, Handle Animal +7, Heal +11, Knowledge (geography) +9, Knowledge (nature) +9, Linguistics +3, Perception +12, Ride +3, Spellcraft +6, Stealth +2, Survival +14, Swim +1
Languages Common, Druidic, Osiriani, Sign Language (Common), Sylvan, Terran
SQ nature bond (tiger named Carl), nature sense, trackless step, wild empathy +7, woodland stride
Combat Gear scroll of barkskin, scroll of barkskin, scroll of cure serious wounds, scroll of darkvision, scroll of delay poison, scroll of feather step, scroll of greater magic fang, scroll of lesser restoration, scroll of remove blindness/deafness, scroll of remove curse, scroll of remove disease, scroll of see invisibility, scroll of speak with animals, scroll of speak with plants, wand of barkskin (15 charges), wand of cure light wounds; Other Gear +2 dragonhide agile breastplate[APG], +2 light wooden shield, light wooden shield, quarterstaff of entwined serpents, hope knife, scimitar, cloak of resistance +1, headband of inspired wisdom +2, druid backpack, spell component pouch, 2,466 gp, 6 sp, 7 cp
"""
StatisticsHeader = Divider + NL + "Statistics" + NL + Divider + NL

# Line 1
Strength = Suppress(Literal("Str")) + SignedInteger("strength") + Comma
Dexterity = Suppress(Literal("Dex")) + SignedInteger("dexterity") + Comma
Constitution = Suppress(Literal("Con")) + SignedInteger("constitution") + Comma
Intelligence = Suppress(Literal("Int")) + SignedInteger("intelligence") + Comma
Wisdom = Suppress(Literal("Wis")) + SignedInteger("wisdom") + Comma
Charisma = Suppress(Literal("Cha")) + SignedInteger("charisma")
AbilityLine = Strength + Dexterity + Constitution + Intelligence + Wisdom + Charisma + NL

# Line 2
CMB = Suppress(SkipTo(Literal("CMB")) + Literal("CMB")) + SignedInteger("cmb") + ParentheticalRE + SemiColon
CMD = Suppress(Literal("CMD")) + Integer("cmd") + ParentheticalRE
AttackLine = CMB + CMD + Suppress(restOfLine) + NL

# Line 3
FeatsLine = Suppress(Literal("Feats")) + NamedList("feats") + NL

# Line 4
TraitsOrTricks = (Literal("Traits") | Literal("Tricks"))
TraitsLine = Suppress(TraitsOrTricks) + NamedList("traits_or_tricks") + NL

# Line 5
SkillName = Regex("[^+\-\d\n]+").setParseAction(lambda s, l, t: t[0].strip())
SkillBonus = SignedInteger
SkillExtra = Regex("\(.*?\)")
Skill = Group(SkillName("skill") + SkillBonus("bonus") + Optional(SkillExtra)("extra"))
Skills = delimitedList(Skill, delim=",")("skills")
ExtraModifiers = SemiColon + restOfLine.suppress()
SkillsLine = Suppress(Literal("Skills")) + Skills + Optional(ExtraModifiers) + NL

# Line 6
LanguageLine = Suppress(Literal("Languages")) + NamedList("languages") + NL

# Line 7
SQLine = Suppress(Literal("SQ")) + NamedList("sq") + NL

# Line 8
Gear = (Literal("Combat Gear") | Literal("Other Gear"))
GearLine = Suppress(Gear) + NamedList("gear") + NL

Statistics = Suppress(StatisticsHeader) + AbilityLine + AttackLine + FeatsLine + Optional(TraitsLine) + SkillsLine + Optional(LanguageLine) + SQLine + GearLine

# Special Abilities
"""
--------------------
Special Abilities
--------------------
Animal Companion Link (Ex) Handle or push Animal Companion faster, +4 to checks vs. them.
Augment Summoning Summoned creatures have +4 to Strength and Constitution.
Eschew Materials Cast spells without materials, if component cost is 1 gp or less.
Extend Spell Spell duration lasts twice as normal. +1 Level.
Immunity to Poison You are immune to poison.
Natural Spell You can cast spells while in Wild Shape.
Nature Sense (Ex) A druid gains a +2 bonus on Knowledge (nature) and Survival checks.
Share Spells with Companion (Ex) Can cast spells with a target of "you" on animal companion, as touch spells.
Spell Focus (Conjuration) Spells from one school of magic have +1 to their save DC.
Trackless Step (Ex) You do not leave a trail as you move through natural surroundings.
Wild Empathy +7 (Ex) Improve the attitude of an animal, as if using Diplomacy.
Wild Shape (9 hours, 3/day) (Su) Shapeshift into a different creature one or more times per day.
Woodland Stride (Ex) Move through undergrowth at normal speed. 
"""
SpecialHeader = Divider + NL + "Special Abilities" + NL + Divider + NL
SpecialAbilityRE = Regex("[^\n]+").setParseAction(lambda s, l, t: t[0].strip())
SpecialAbilityLine = SpecialAbilityRE + NL
SpecialAbilities = ZeroOrMore(SpecialAbilityLine)("special_abilities")

Special = Suppress(SpecialHeader) + SpecialAbilities

StatBlock = Basics + Defense + Offense + Statistics + Special

def parse_statblock(statblock):
    return StatBlock.parseString(statblock).asDict()


