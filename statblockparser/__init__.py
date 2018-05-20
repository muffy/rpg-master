from pyparsing import *

DIVIDER = "--------------------"

NL = LineEnd().suppress()
END = StringEnd()

ParserElement.setDefaultWhitespaceChars(" \t")
ParenRE = Regex("\(.*?\)")
SignedInteger = pyparsing_common.signed_integer
Integer = pyparsing_common.integer
Comma = Literal(",").suppress()
SemiColon = Literal(";").suppress()
Divider = Literal(DIVIDER)

NameRE = Regex("[^\n,]+").setParseAction(lambda s, l, t: t[0].strip())
NamedList = delimitedList(NameRE, delim=",")
HyphenWord = Word(alphas + "-")
Phrase = OneOrMore(HyphenWord).setParseAction(lambda s, l, t: " ".join(t))

Gender = oneOf("Female Male")
Alignment = oneOf("CE CN CG NE N NG LE LN LG")
Size = oneOf("Diminutive Tiny Small Medium Large Huge Gargantuan")

SectionHeader = Divider + NL + OneOrMore(Word(alphas)) + NL + Divider + NL
NextSection = Suppress(SkipTo(SectionHeader)) + Suppress(SectionHeader)

# NPC description
Description = restOfLine("description") + NL + Suppress(Divider) + NL

# Basics content
"""
Gwendolyn Gwynne
Female human (Garundi) druid 9
N Medium humanoid (human)
Init +2; Senses Perception +12
"""
CharacterName = restOfLine.setParseAction(lambda s, l, t: t[0].split("CR")[0].strip())
NameLine = CharacterName("character_name") + NL

XPLine = Literal("XP") + restOfLine + NL

ClassLevel = Group(Phrase("class") + Integer("level"))
Classes = delimitedList(ClassLevel, delim="/")
GRCLine = Gender("gender") + HyphenWord("race") + Optional(Classes("classes")) + NL
GRCLine.ignore(ParenRE)

ASTLine = Alignment("alignment") + Size("size") + Suppress(restOfLine) + NL

Initiative = Suppress(Literal("Init")) + SignedInteger("initiative")
Perception = Suppress(Literal("Perception")) + SignedInteger("perception")
InitLine = Initiative + SkipTo(Perception) + Perception + NL

Basics = NameLine + GRCLine + ASTLine + InitLine

# NPC Basics

GRLine = Gender("gender") + Phrase("race") + NL
GRLine.ignore(ParenRE)

NPCBasics = Description + NameLine + XPLine + GRLine + ASTLine + InitLine

# Defense
"""
--------------------
Defense
--------------------
AC 20, touch 12, flat-footed 18 (+8 armor, +2 Dex)
hp 75 (9d8+27)
Fort +9, Ref +6, Will +15; +4 vs. fey and plant-targeted effects
Immune poison"""
AC = Suppress(Literal("AC")) + SignedInteger("ac") + Comma
TouchAC = Literal("touch") + SignedInteger("touch_ac") + Comma
FlatFootedAC = Literal("flat-footed") + SignedInteger("flat_footed_ac")
ACLine = AC + TouchAC + FlatFootedAC + Suppress(restOfLine) + NL

HPLine = Literal("hp") + SignedInteger("hp") + Suppress(restOfLine) + NL

Save = Suppress(Word(alphas)) + SignedInteger + Optional(Comma)
Save.setParseAction(lambda s, l, t: t[0])
SaveLine = Save("fort_save") + Save("reflex_save") + Save("will_save") + Optional(SemiColon + restOfLine("other_saves"))

Defense = NextSection + ACLine + HPLine + SaveLine

# Offense
"""
--------------------
Offense
--------------------
Speed 30 ft. (20 ft. in armor)
[...]
"""
NumFeet = Integer + Suppress(Literal("ft."))
NumFeet.setParseAction(lambda s, l, t: f"{t[0]}")
SpeedLine = Suppress(Literal("Speed")) + NumFeet + Optional("(" + NumFeet) + restOfLine + NL
SpeedLine.setParseAction(lambda s, l, t: "/".join(t))

# NPC
Space = Literal("Space")
Reach = Literal("Reach")
SpaceFeet = SkipTo(Space) + Suppress(Space) + NumFeet("space")
ReachFeet = SkipTo(Reach) + Suppress(Reach) + NumFeet("reach")

Offense = NextSection + SpeedLine("speed")
NPCOffense = NextSection + SpeedLine("speed") + SpaceFeet + ReachFeet

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
Score = Suppress(Word(alphas)) + Integer + Optional(Comma)
Score.setParseAction(lambda s, l, t: t[0])
AbilityLine = Score("strength") + Score("dexterity") + Score("constitution") + Score("intelligence") + Score("wisdom") + Score("charisma") + NL

CMB = Suppress(SkipTo(Literal("CMB")) + Literal("CMB")) + SignedInteger("cmb") + Optional(ParenRE) + SemiColon
CMD = Suppress(Literal("CMD")) + Integer("cmd") + Optional(ParenRE)
AttackLine = CMB + CMD + Suppress(restOfLine) + NL

FeatsLine = Suppress(Literal("Feats")) + NamedList("feats") + NL
TraitsLine = Suppress(Literal("Traits")) + NamedList("traits") + NL
TricksLine = Suppress(Literal("Tricks")) + NamedList("tricks") + NL

FeatsEtc = FeatsLine + Optional(TraitsLine) + Optional(TricksLine)

SkillName = Regex("[^+\-\d\n]+").setParseAction(lambda s, l, t: t[0].strip())
Skill = Group(SkillName("skill") + SignedInteger("bonus") + Optional(ParenRE("extra")))
Skills = delimitedList(Skill, delim=",")("skills")
ExtraModifiers = SemiColon + restOfLine.suppress()
SkillsLine = Suppress(Literal("Skills")) + Skills + Optional(ExtraModifiers) + NL

LanguageLine = Suppress(Literal("Languages")) + NamedList("languages") + NL

SQLine = Suppress(Literal("SQ")) + NamedList("sq") + NL

GearType = (Literal("Combat Gear") | Literal("Other Gear"))
GearLine = Suppress(GearType) + NamedList("gear") + NL

SkillsEtc = SkillsLine + Optional(LanguageLine) + Optional(SQLine) + Optional(GearLine)

Statistics = NextSection + AbilityLine + AttackLine + FeatsEtc + SkillsEtc

# NPC Ecology
"""
--------------------
Ecology
--------------------
Environment cold mountains
Organization solitary, gang (3-5), band (6-12 plus 35% noncombatants and 1 adept or cleric of 1st-2nd level), raiding party (6-12 plus 35% noncombatants, 1 adept or sorcerer of 3rd-5th level, 1-4 winter wolves, and 2-3 ogres), or tribe (21-30 plus 1 adept, cleric, or sorcerer of 6th-7th level; 1 barbarian or ranger jarl of 7th-9th level; and 15-36 winter wolves, 13-22 ogres, and 1-2 young white dragons)
Treasure standard (chain shirt, greataxe, other treasure)
"""
Ecology = NextSection

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
SpecialAbilityRE = Regex("[^\n]+").setParseAction(lambda s, l, t: t[0].strip())
SpecialAbilityLine = SpecialAbilityRE + NL
SpecialAbilities = ZeroOrMore(SpecialAbilityLine)("special_abilities")

Special = NextSection + SpecialAbilities

PCStatBlock = Basics + Defense + Offense + Statistics + Special
NPCStatBlock = NPCBasics + Defense + NPCOffense + Statistics + Ecology + Special


def parse_statblock(statblock, npc=False):
    lines = statblock.split("\n")
    npc = npc or lines[1] == DIVIDER
    if npc:
        return NPCStatBlock.parseString(statblock).asDict()
    else:
        return PCStatBlock.parseString(statblock).asDict()


