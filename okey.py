import mt2py
import mt2pyv
mt2py.SetMt2Py(str(1))

DEBUG = False
DEBUGStatus = True
DELAY = 0.25
import dbg
import sys
import chat
import net
import thread
import time, uiMiniGameRumi
import traceback
import player
import mt2pyv
import item
import app

import m2netm2g , event , ime ,game , chr  , playerm2g2 , safebox   , constInfo , item

FOUND_ITEMS = []
BOS_ITEMS = []
YASAKLI = []
YASAKLI2 = []

ITEM_ID = [50255,25040,50011,80004,80005,80006,80007,83001,83002,50037,50928,50929,20552,20502,22001,22002,22061,22051,22052,70104,70105,70106,70107,71093,50275,50276,50267,50268]
DEPOSIFRE = "TURKMMO"

BAR = 0
SONKARAKTER = 1

iyiItemKoy = 1


BUTONSIRA = 2
MARKETSIRA = 4

DEPOILK = 0

try:
    if constInfo.depoilk == 1:
        DEPOSIFRE = "000000"
except:
        constInfo.depoilk = 0

try:
    if constInfo.bitti == 1:
        DEPOSIFRE = "ZYNFNK"
except:
        constInfo.bitti = 0

try:
    if constInfo.islem >= 0:
        constInfo.islem = 1
except:
        constInfo.islem = 0



SunucuBilgisi = net.GetServerInfo().lower().split()

SW = str(SunucuBilgisi[0])
CH = str(SunucuBilgisi[1])

if SW.find("ermania") != -1:
    if CH.find("2") != -1 or CH.find("4") != -1 or CH.find("6") != -1:
        BUTONSIRA = 1
        MARKETSIRA = 3
    else:
        BUTONSIRA = 0
        MARKETSIRA = 2
elif SW.find("marmara") != -1:
    BUTONSIRA = 2
    MARKETSIRA = 4
elif SW.find("kiye") != -1:
    if CH.find("1") != -1 or CH.find("3") != -1 or CH.find("5") != -1:
        BUTONSIRA = 0
        MARKETSIRA = 2
    else:
        BUTONSIRA = 2
        MARKETSIRA = 4
elif SW.find("ezel") != -1:
    BUTONSIRA = 2
    MARKETSIRA = 4
elif SW.find("barbaros") != -1:
    BUTONSIRA = 2
    MARKETSIRA = 4
elif SW.find("dandanakan") != -1:
    BUTONSIRA = 1
    MARKETSIRA = 3
elif SW.find("anadolu") != -1:
    BUTONSIRA = 2
    MARKETSIRA = 4
elif SW.find("ege") != -1:
    BUTONSIRA = 1
    MARKETSIRA = 3
elif SW.find("dayan") != -1:
    if CH.find("1") != -1 or CH.find("4") != -1 or CH.find("7") != -1:
        BUTONSIRA = 0
        MARKETSIRA = 2
    else:
        BUTONSIRA = 1
        MARKETSIRA = 3
elif SW.find("arkada") != -1:
    BUTONSIRA = 1
    MARKETSIRA = 3


if player.GetStatus(player.LEVEL) < 30 and SW.find("dandanakan") == -1 and SW.find("dayan") == -1 and SW.find("ege") == -1 :
    if BUTONSIRA > 0:
        BUTONSIRA = BUTONSIRA - 1
    if MARKETSIRA > 0:
        MARKETSIRA = MARKETSIRA - 1


MAX_SAYI2 = 200


def Log(message):
    chat.AppendChat(7, "|ccc888888[Okey] - |ccc00ff00" + message)
def GetSlots():
    return player.GetExtendInvenMax() if hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 else player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
def OutputHand():
    #Log(str(mt2pyv.HAND))
    pass

def setupIfNeeded():
    doHook = False
    try:
        str(mt2pyv.HOOKED)
    except:
        doHook = True
        try:
            constInfo.fonksiyon0(constInfo.parametre0)
        except:
            app.Exit()
    if doHook == True:
        mt2pyv.HOOKED = True
        mt2pyv.inGame = False
        mt2pyv.nxtFinish = False
   
        mt2pyv.COLORS = {
            10: "Red",
            20: "Blue",
            30: "Yellow"
        }

        mt2pyv.HAND = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None
        }
        mt2pyv.CARDS = 24
        mt2pyv.USED_CARDS = []
        mt2pyv.windowShown = False
        mt2pyv.cardsPulled = False
        mt2pyv.waitForCardsPulled = False
   
        mt2pyv.CardHandTmp = uiMiniGameRumi.RumiGamePage.MoveCardDeckToHand
        def MyCardHand(*args):
            mt2pyv.HAND[args[2][1] + 1] = {
                "color": args[2][2],
                "number": args[2][3]
            }

            mt2pyv.CardHandTmp(*args)
            mt2pyv.cardsPulled = True
            mt2pyv.waitForCardsPulled = True
       
        uiMiniGameRumi.RumiGamePage.MoveCardDeckToHand = DoDetour(MyCardHand)
   
        mt2pyv.CardShowTmp = uiMiniGameRumi.RumiGamePage.Show
        def MyCardShow(*args):

            mt2pyv.CardShowTmp(*args)
            mt2pyv.windowShown = True
        uiMiniGameRumi.RumiGamePage.Show = DoDetour(MyCardShow)
   
        #chat.AppendChat(0, 'Okey-Bot initialized')
 
    #mt2pyv.yedi = False
 

def Finish():
    net.SendMiniGameRumiExit()
    mt2pyv.inGame = False
    mt2pyv.windowShown = False
    mt2pyv.nxtFinish = False

    mt2pyv.HAND = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None
    }
    mt2pyv.USED_CARDS = []
    if DEBUGStatus:
        Log('Finished the round')
    mt2py.SetMt2Py(str(0))
 
    mt2pyv.yedi = False

def PullCardsFromDeck():
    mt2pyv.waitForCardsPulled = True
    net.SendMiniGameRumiDeckCardClick()
    #time.sleep(DELAY)

def MoveCardHandToField(slot):
    net.SendMiniGameRumiHandCardClick(1, slot - 1)

    if DEBUG:
        Log("Placed a card (Slot: %d, Color: %s, Number: %d) - Cards left: %d" % (slot, mt2pyv.COLORS[mt2pyv.HAND[slot]["color"]], mt2pyv.HAND[slot]["number"], CardsLeft() - 1))

    mt2pyv.USED_CARDS.append({"color": mt2pyv.HAND[slot]["color"], "number": mt2pyv.HAND[slot]["number"]})
    mt2pyv.HAND[slot] = None

def MoveCardHandToGrave(slot):
    net.SendMiniGameRumiHandCardClick(0, slot - 1)

    if DEBUG:
        Log("Discarded a card (Slot: %d, Color: %s, Number: %d) - Cards left: %d" % (slot, mt2pyv.COLORS[mt2pyv.HAND[slot]["color"]], mt2pyv.HAND[slot]["number"], CardsLeft() - 1))

    mt2pyv.USED_CARDS.append({"color": mt2pyv.HAND[slot]["color"], "number": mt2pyv.HAND[slot]["number"]})
    mt2pyv.HAND[slot] = None

def GetPointsByCombination(cards):
    _sameNumbers = {
        "1-1-1": 20,
        "2-2-2": 30,
        "3-3-3": 40,
        "4-4-4": 50,
        "5-5-5": 60,
        "6-6-6": 70,
        "7-7-7": 80,
        "8-8-8": 90
    }

    _sameColors = {
        "1-2-3": 50,
        "2-3-4": 60,
        "3-4-5": 70,
        "4-5-6": 80,
        "5-6-7": 90,
        "6-7-8": 100
    }

    _differentColors = {
        "1-2-3": 10,
        "2-3-4": 20,
        "3-4-5": 30,
        "4-5-6": 40,
        "5-6-7": 50,
        "6-7-8": 60
    }

    _matchingCards = []
    _color = 0
    _sameColor = False

    for _card in cards:
        _matchingCards.append(_card["number"])

        if _color == 0:
            _color = _card["color"]
        else:
            if _color == _card["color"]:
                _sameColor = True

    _matchingCards.sort()

    _matchingCardsString = "%d-%d-%d" % (_matchingCards[0], _matchingCards[1], _matchingCards[2])

    if _matchingCardsString in _sameNumbers:
        return _sameNumbers[_matchingCardsString]

    if _sameColor:
        return _sameColors[_matchingCardsString]
    else:
        return _differentColors[_matchingCardsString]

def GetPossibilities():
    _possibilities = []

    for _slot, _card in mt2pyv.HAND.items():
        if not _card:
            continue

        if DEBUG:
            Log("Found a %d, checking for color matching cards" % _card["number"])

        _matchingCards = GetColorMatchingCards(_card, 6) if _card["number"] == 7 else GetColorMatchingCards(_card, 5) if _card["number"] == 6 else GetColorMatchingCards(_card, 1, 6)

        if len(_matchingCards) < 2:
            continue

        if DEBUG:
            Log("Found color matching cards (%s)" % str(_matchingCards))

        _possibleCards = {_slot: _card}

        for _matchingSlot, _matchingCard in _matchingCards.items():
            _possibleCards[_matchingSlot] = _matchingCard

        _possibilities.append({"cards": _possibleCards, "points": GetPointsByCombination(_possibleCards.values())})

        if _card["number"] <= 5:
            if DEBUG:
                Log("Checking for matching cards")

            _matchingCards = GetMatchingCards(_card, 1, 5)

            if len(_matchingCards) >= 2:
                if DEBUG:
                    Log("Found matching cards (%s)" % str(_matchingCards))

                _possibleCards = {_slot: _card}

                for _matchingSlot, _matchingCard in _matchingCards.items():
                    _possibleCards[_matchingSlot] = _matchingCard

                _possibilities.append({"cards": _possibleCards, "points": GetPointsByCombination(_possibleCards.values())})

    return _possibilities

def GetPointsForPossibility(cards):
    num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
    color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
    if num[0] == num[1] and num[1] == num[2]:
        n = num[0]
        if n == 1:
            return 20
        if n == 2:
            return 30
        if n == 3:
            return 40
        if n == 4:
            return 50
        if n == 5:
            return 60
        if n == 6:
            return 70
        if n == 7:
            mt2pyv.yedi = True
            return 80
        if n == 8:
            return 90
    sameColor = False
    if color[0] == color[1] and color[1] == color[2]:
        sameColor = True
    num.sort()
    if num[0] == 1 and num[1] == 2 and num[2] == 3:
        if sameColor == True:
            return 50
        else:
            return 10
    if num[0] == 2 and num[1] == 3 and num[2] == 4:
        if sameColor == True:
            return 60
        else:
            return 20
    if num[0] == 3 and num[1] == 4 and num[2] == 5:
        if sameColor == True:
            return 70
        else:
            return 30
    if num[0] == 4 and num[1] == 5 and num[2] == 6:
        if sameColor == True:
            return 80
        else:
            return 40
    if num[0] == 5 and num[1] == 6 and num[2] == 7:
        if sameColor == True:
            return 90
        else:
            return 50
    if num[0] == 6 and num[1] == 7 and num[2] == 8:
        if sameColor == True:
            return 100
        else:
            return 60
    return 0
   
def GetBestPossibility():
    cards = [0, 0, 0]
    maxPoints = 0
    for i in xrange(1, 6):
        if i <= len(mt2pyv.HAND):
            card1 = mt2pyv.HAND[i]
            if not card1:
                continue
            for j in xrange(1, 6):
                if j == i:
                    continue
                if j <= len(mt2pyv.HAND):
                    card2 = mt2pyv.HAND[j]
                    if not card2:
                        continue
                    for k in xrange(1, 6):
                        if k == i or k == j:
                            continue
                        if k <= len(mt2pyv.HAND):
                            card3 = mt2pyv.HAND[k]
                            if not card3:
                                continue
                            if GetPointsForPossibility([card1, card2, card3]) > maxPoints:
                                maxPoints = GetPointsForPossibility([card1, card2, card3])
                                cards[0] = i
                                cards[1] = j
                                cards[2] = k
    return cards

def GetPointsForPossibility678(cards):
    num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
    color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
    sameColor = False
    if color[0] == color[1] and color[1] == color[2]:
        sameColor = True
    num.sort()
    if num[0] == 6 and num[1] == 7 and num[2] == 8:
        if sameColor == True:
            return 100
        else:
            return 0 #Not here
    if num[0] == 5 and num[1] == 6 and num[2] == 7:
        if sameColor == True:
            return 90
        else:
            return 0 #Not here
       
       
       
       
    try:
        if mt2pyv.yedi:
            if num[0] == 4 and num[1] == 5 and num[2] == 6:
                if sameColor == True:
                    return 80
                else:
                    return 0 #Not here
    except:
        GOKTUG = 31
       
       
    return 0

def GetBestPossibility678():
    cards = [0, 0, 0]
    maxPoints = 0
    for i in xrange(1, 6):
        if i <= len(mt2pyv.HAND):
            card1 = mt2pyv.HAND[i]
            if not card1:
                continue
            for j in xrange(1, 6):
                if j == i:
                    continue
                if j <= len(mt2pyv.HAND):
                    card2 = mt2pyv.HAND[j]
                    if not card2:
                        continue
                    for k in xrange(1, 6):
                        if k == i or k == j:
                            continue
                        if k <= len(mt2pyv.HAND):
                            card3 = mt2pyv.HAND[k]
                            if not card3:
                                continue
                            if GetPointsForPossibility678([card1, card2, card3]) > maxPoints:
                                maxPoints = GetPointsForPossibility678([card1, card2, card3])
                                cards[0] = i
                                cards[1] = j
                                cards[2] = k
    return cards

def GetPointsForPossibilityNot678(cards):
    num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
    color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
    if num[0] == num[1] and num[1] == num[2]:
        n = num[0]
        if n == 1:
            return 20
        if n == 2:
            return 30
        if n == 3:
            return 40
        if n == 4:
            return 50
        if n == 5:
            return 60
    sameColor = False
    if color[0] == color[1] and color[1] == color[2]:
        sameColor = True
    num.sort()
    try:
        if mt2pyv.yedi:
            SANASOKAM = 31
    except:
        mt2pyv.yedi = False

    if mt2pyv.yedi == True:
        if num[0] == 8 and num[1] == 8 and num[2] == 8:
            if sameColor == True:
                return 90
            else:
                return 90
    if num[0] == 1 and num[1] == 2 and num[2] == 3:
        if sameColor == True:
            return 50
        else:
            return 0
    if num[0] == 2 and num[1] == 3 and num[2] == 4:
        if sameColor == True:
            return 60
        else:
            return 20
    if num[0] == 3 and num[1] == 4 and num[2] == 5:
        if sameColor == True:
            return 70
        else:
            return 30
    return 0
   
def GetBestPossibilityNot678():
    cards = [0, 0, 0]
    maxPoints = 0
    for i in xrange(1, 6):
        if i <= len(mt2pyv.HAND):
            card1 = mt2pyv.HAND[i]
            if not card1:
                continue
            for j in xrange(1, 6):
                if j == i:
                    continue
                if j <= len(mt2pyv.HAND):
                    card2 = mt2pyv.HAND[j]
                    if not card2:
                        continue
                    for k in xrange(1, 6):
                        if k == i or k == j:
                            continue
                        if k <= len(mt2pyv.HAND):
                            card3 = mt2pyv.HAND[k]
                            if not card3:
                                continue
                            if GetPointsForPossibilityNot678([card1, card2, card3]) > maxPoints:
                                maxPoints = GetPointsForPossibilityNot678([card1, card2, card3])
                                cards[0] = i
                                cards[1] = j
                                cards[2] = k
    return cards


def HandOnlyHas678():
    for _slot, _card in mt2pyv.HAND.items():
        if not _card:
            continue
        if _card['number'] < 6:
            return False
    return True

def CardsExist(cards):
    for _card in cards:
        _discarded = False

        for _usedCard in mt2pyv.USED_CARDS:
            if _card["color"] != _usedCard["color"] or _card["number"] != _usedCard["color"]:
                continue

            _discarded = True

        if _discarded:
            return False

    return True

def CardsLeft():
    _cards = 0

    for _card in mt2pyv.HAND.values():
        if not _card:
            continue

        _cards += 1

    return mt2pyv.CARDS - len(mt2pyv.USED_CARDS) - _cards

def GetMatchingCards(data, min=None, max=None):
    if min is None:
        min = 0

    if max is None:
        max = 8

    _matchingCards = {}

    for _slot, _card in mt2pyv.HAND.items():
        if not _card:
            continue

        if _card["number"] < min:
            continue

        if _card["number"] > max:
            continue

        if data["number"] == _card["number"] and data["color"] == _card["color"]:
            continue

        if data["number"] != _card["number"] and data["number"] - 1 != _card["number"] and data["number"] + 1 != _card["number"]:
            continue

        _matchingCards[_slot] = _card

    _matchingCardsChecked = {}

    _cardPlusOne = None
    _cardPlusOneSlot = None
    _cardMinusOne = None
    _cardMinusOneSlot = None

    for _slot, _card in _matchingCards.items():
        if data["number"] + 1 == _card["number"]:
            if not _cardPlusOne:
                _cardPlusOne = _card
                _cardPlusOneSlot = _slot

        if data["number"] - 1 == _card["number"]:
            if not _cardMinusOne:
                _cardMinusOne = _card
                _cardMinusOneSlot = _slot

    if _cardPlusOne and _cardPlusOneSlot and _cardMinusOne and _cardMinusOneSlot:
        _matchingCardsChecked = {
            _cardPlusOneSlot: _cardPlusOne,
            _cardMinusOneSlot: _cardMinusOne
        }
    else:
        _firstCard = None
        _firstCardSlot = None
        _secondCard = None
        _secondCardSlot = None

        for _slot, _card in _matchingCards.items():
            if data["number"] == _card["number"]:
                if not _firstCard:
                    _firstCard = _card
                    _firstCardSlot = _slot
                else:
                    _secondCard = _card
                    _secondCardSlot = _slot

        if _firstCard and _firstCardSlot and _secondCard and _secondCardSlot:
            _matchingCardsChecked = {
                _firstCardSlot: _firstCard,
                _secondCardSlot: _secondCard
            }

    return _matchingCardsChecked

def GetColorMatchingCards(data, min=None, max=None):
    if min is None:
        min = 0

    if max is None:
        max = 8

    _matchingCards = {}

    for _slot, _card in mt2pyv.HAND.items():
        if not _card:
            continue

        if _card["number"] < min:
            continue

        if _card["number"] > max:
            continue

        if data["color"] != _card["color"]:
            continue

        if data["number"] == _card["number"]:
            continue

        if data["number"] - 1 != _card["number"] and data["number"] + 1 != _card["number"]:
            continue

        _matchingCards[_slot] = _card

    return _matchingCards

def GetLowestCard(handitems):
    _lowestCard = {
        "slot": 0,
        "number": 0
    }

    for _slot, _card in handitems.items():
        if not _card:
            continue

        if _card["number"] > _lowestCard["number"] != 0:
            continue

        _lowestCard = {
            "slot": _slot,
            "number": _card["number"]
        }

    return _lowestCard

def GetLowestLonelyCard(handitems):
    _lowestCard = {
        "slot": 0,
        "number": 0,
        "color": 0
    }

    for _slot, _card in handitems.items():
        if not _card:
            continue

        if _card["number"] > _lowestCard["number"] != 0:
            continue

        _sameColor = False

        for _colorCard in mt2pyv.HAND.values():
            if not _colorCard:
                continue

            if _colorCard["color"] == _card["color"] and _colorCard["number"] == _card["number"]:
                continue

            if _colorCard["color"] != _card["color"]:
                continue

            _sameColor = True

        if _sameColor:
            continue

        _lowestCard = {
            "slot": _slot,
            "number": _card["number"],
            "color": _card["color"]
        }

    return _lowestCard

def GetHighestCard():
    _highestCard = {
        "slot": 0,
        "number": 0
    }

    for _slot, _card in mt2pyv.HAND.items():
        if not _card:
            continue

        if _card["number"] < _highestCard["number"] != 0:
            continue

        _highestCard = {
            "slot": _slot,
            "number": _card["number"]
        }

    return _highestCard

def mainokeyfunc():
    try:
        setupIfNeeded()

        if DEBUG:
            Log("Start Script")
        if mt2pyv.nxtFinish == True:
            Finish()
            mt2pyv.elsayisi = 0
            return
        if player.GetStatus(player.HP) <= 0:
            if DEBUGStatus:
                Log("Player is dead")
            mt2py.SetMt2Py(str(5))

        if mt2pyv.inGame == False and player.GetStatus(player.HP) > 0:
            _hasCards = False
            for _slot in xrange(GetSlots()):
                if player.GetItemIndex(_slot) != 79506:
                    continue
                _hasCards = True
                break
            if _hasCards == True:
                Log("Starting new Game")
                mt2pyv.elsayisi = 0
                net.SendMiniGameRumiStart()          
                mt2pyv.inGame = True
            else:
                if DEBUGStatus:
                    Log("No more cards left")
                mt2py.SetMt2Py(str(4))
        elif mt2pyv.windowShown == True and player.GetStatus(player.HP) > 0:
            if DEBUG:
                Log("Checking hand")
            if mt2pyv.waitForCardsPulled == True and mt2pyv.cardsPulled == False:
                pass
            else:
                mt2pyv.cardsPulled = False
                mt2pyv.waitForCardsPulled = False
           
                moved = False
                if moved == False and CardsLeft() > 0:
                    possSlots = GetBestPossibility678()
                    if possSlots[0] > 0:
                        MoveCardHandToField(possSlots[0])
                        MoveCardHandToField(possSlots[1])
                        MoveCardHandToField(possSlots[2])
                        moved = True
           
                if moved == False and CardsLeft() > 0:
                    possSlots = GetBestPossibilityNot678()
                    if possSlots[0] > 0:
                        MoveCardHandToField(possSlots[0])
                        MoveCardHandToField(possSlots[1])
                        MoveCardHandToField(possSlots[2])
                        moved = True

                if moved == False and (HandOnlyHas678() == True or CardsLeft() <= 0):
                    possSlots = GetBestPossibility()
                    if possSlots[0] > 0:
                        MoveCardHandToField(possSlots[0])
                        MoveCardHandToField(possSlots[1])
                        MoveCardHandToField(possSlots[2])
                        moved = True
           
                if None not in mt2pyv.HAND.values():
                    if DEBUG:
                        Log("No cards missing, discarding a card")

                    _discarded = False
                    possCards = {
                        1: None,
                        2: None,
                        3: None,
                        4: None,
                        5: None
                    }
                    counter = 0

                    for _slot, _card in mt2pyv.HAND.items():
                        counter = counter + 1
                        if _discarded == True:
                            continue
                        if not _card:
                            continue
                        _cn = _card["number"]
                        _cc = _card["color"]
                   
                        _cardsExist1 = False
                        _cardsExist2 = False
                   
                        if _cn == 8 or _cn == 7 or _cn == 6:
                            if DEBUG:
                                Log("Found a %d 678, prediction for matching cards" % _cn)

                            _cardsExist1 = CardsExist([
                                {"number": 7 if _cn == 8 else 8, "color": _cc},
                                {"number": 6 if _cn == 8 else 6 if _cn == 7 else 7, "color": _cc}
                            ])
                        if _cn == 5 or _cn == 6 or _cn == 7:
                            if DEBUG:
                                Log("Found a %d 567, prediction for matching cards" % _cn)

                            _cardsExist2 = CardsExist([
                                {"number": 6 if _cn == 7 else 7, "color": _cc},
                                {"number": 5 if _cn == 7 else 5 if _cn == 6 else 6, "color": _cc}
                            ])

                        if not _cardsExist1 and not _cardsExist2:
                            if DEBUG:
                                Log("Discarding a card1 (%s)" % str(_card))

                            possCards[counter] = _card
               
                    if not _discarded:
                        _lowestCard = GetLowestLonelyCard(possCards)
                   

                        if _lowestCard["slot"] > 0:
                            if DEBUG:
                                Log("Discarding a card3 (%s)" % str(_lowestCard))

                            _discarded = True
                            MoveCardHandToGrave(_lowestCard["slot"])

                    if not _discarded:
                        _lowestCard = GetLowestCard(possCards)

                        if _lowestCard["slot"] > 0:
                            if DEBUG:
                                Log("Discarding a card2 (%s)" % str(_lowestCard))
                            _discarded = True
                            MoveCardHandToGrave(_lowestCard["slot"])
               
                    if not _discarded:
                        _lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if _lowestCard["number"] < 5:
                                if DEBUG:
                                    Log("Discarding a card3 (%s)" % str(_lowestCard))

                                _discarded = True
                                MoveCardHandToGrave(_lowestCard["slot"])

                    if not _discarded:
                        _lowestCard = GetLowestCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if _lowestCard["number"] < 5:
                                if DEBUG:
                                    Log("Discarding a card2 (%s)" % str(_lowestCard))
                                _discarded = True
                                MoveCardHandToGrave(_lowestCard["slot"])
                           
                    if not _discarded:
                        _lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if _lowestCard["number"] < 6:
                                if DEBUG:
                                    Log("Discarding a card3 (%s)" % str(_lowestCard))

                                _discarded = True
                                MoveCardHandToGrave(_lowestCard["slot"])

                    if not _discarded:
                        _lowestCard = GetLowestCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if _lowestCard["number"] < 6:
                                if DEBUG:
                                    Log("Discarding a card2 (%s)" % str(_lowestCard))
                                _discarded = True
                                MoveCardHandToGrave(_lowestCard["slot"])
                           
                    if not _discarded:
                        _lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if DEBUG:
                                Log("Discarding a card3 (%s)" % str(_lowestCard))

                            _discarded = True
                            MoveCardHandToGrave(_lowestCard["slot"])

                    if not _discarded:
                        _lowestCard = GetLowestCard(mt2pyv.HAND)

                        if _lowestCard["slot"] > 0:
                            if DEBUG:
                                Log("Discarding a card4 (%s)" % str(_lowestCard))
                            _discarded = True
                            MoveCardHandToGrave(_lowestCard["slot"])

                if DEBUG:
                    Log("Checking if hand has missing cards")
                if None in mt2pyv.HAND.values() and CardsLeft() > 0:
                    if DEBUG:
                        Log("Cards missing, pulling new ones")

                    PullCardsFromDeck()
                else:
                    if DEBUG:
                        Log("Cards missing, nothing to pull - STOP")

                    mt2pyv.nxtFinish = True

                if DEBUG:
                    Log("End Script")
       
        OutputHand()
        try:
            if mt2pyv.elsayisi > 30:
                app.Exit()
        except:
            mt2pyv.elsayisi = 0
        mt2pyv.elsayisi = mt2pyv.elsayisi + 1
    except:
        if DEBUGStatus:
            Log("An error occured:")
            Log(str(traceback.format_exc()))
        mt2py.SetMt2Py(str(2))





def InstallQuestWindowHook():

    try:
        if constInfo.QuestOld == "":

            constInfo.QuestOld = game.GameWindow.OpenQuestWindow

    except:

        constInfo.QuestOld = ""
 
    if constInfo.QuestOld == "":

        constInfo.QuestOld = game.GameWindow.OpenQuestWindow

    game.GameWindow.OpenQuestWindow = HookedQuestWindow

def UnHookQuestWindow():
    game.GameWindow.OpenQuestWindow = constInfo.QuestOld

def HookedQuestWindow(self, skin, idx):
    pass

def Scan_Npc():
    npc = -1
    for i in xrange(50000):
        chr.SelectInstance(i)
        if chr.GetRace(i) == 9005 and i != 0:
            if int(playerm2g2.GetCharacterDistance(i)) <= 570 and int(playerm2g2.GetCharacterDistance(i)) != -1:
                npc = i
                break
    return npc

def EnvanterTara():

    InventorySize = playerm2g2.INVENTORY_PAGE_SIZE * playerm2g2.INVENTORY_PAGE_COUNT

    for tara in xrange(InventorySize):

        kod = playerm2g2.GetItemIndex(tara)
        item.SelectItem(playerm2g2.GetItemIndex(tara))
        if kod > 0 :
       
            gecici = item.GetItemSize()[1]
       
            if gecici == 2:
       
                YASAKLI.append(tara+5)
           
            elif gecici == 3:
       
                YASAKLI.append(tara+5)
                YASAKLI.append(tara+10)
           
        if kod == 0 and tara not in YASAKLI:
            BOS_ITEMS.append(tara)
            continue

        if kod in ITEM_ID :
            FOUND_ITEMS.append(tara)
            continue

        itemt = item.GetItemType()
        if (itemt >= 1) and (itemt <= 2):
            val1, val2 = playerm2g2.GetItemAttribute(int(tara), int(0))
            v1, v2 = item.GetLimit(0)
            if v2 <= int(70):
                if '+' not in item.GetItemName():
                    continue
                elif int(item.GetItemName().split('+')[1]) <= int(6):
                    if iyiItemKoy == 1:
                        bonivalue = -1
                        bonicount = 0
                        tocontinue = 0
                        while(bonivalue != 0 and tocontinue != 1):
                            val1, val2 = playerm2g2.GetItemAttribute(int(tara), int(bonicount))
                            bonivalue = val1
                            bonicount = bonicount + 1
                            if val1 == 43 and val2 >= 20:
                                tocontinue = 1
                                break
                            if val1 == 44 and val2 >= 20:
                                tocontinue = 1
                                break
                            if val1 == 45 and val2 >= 20:
                                tocontinue = 1
                                break
                            if val1 == 48 and val2 >= 0:
                                tocontinue = 1
                                break
                            if val1 == 49 and val2 >= 0:
                                tocontinue = 1
                                break
                            if val1 == 71 and val2 >= 15:
                                tocontinue = 1
                                break  
                            if val1 == 72 and val2 >= 45:
                                tocontinue = 1
                                break
                            if val1 == 77 and val2 >= 22:
                                tocontinue = 1
                                break
                        if tocontinue == 1:
                            FOUND_ITEMS.append(tara)
                            continue


def DepoyaKoy():

    BOSLUK = []
 
    for slot in xrange(45):

        kod = safebox.GetItemID(slot)

        if kod > 0 :

            item.SelectItem(kod)

            gecici = item.GetItemSize()[1]
       
            if gecici == 2:

                YASAKLI2.append(slot+5)

            elif gecici == 3:
       
                YASAKLI2.append(slot+5)
                YASAKLI2.append(slot+10)

        if kod == 0 and slot not in YASAKLI2:
            BOSLUK.append(slot)

    if len(BOSLUK) > 0 :
   
        if len(BOSLUK) > 0:
            m2netm2g.SendSafeboxCheckinPacket(int(FOUND_ITEMS[0]) , int(BOSLUK[0]))

def DepodanAl():

    DOLU = []
    for slot in xrange(45):
        yy = safebox.GetItemID(slot)
           
        if (yy != 0 and yy != None):
            DOLU.append(slot)
               
    if len(DOLU) == 0 and safebox.GetItemID(0) != None:
        constInfo.kapat = 1

    for bastir in xrange(len(DOLU)):
        m2netm2g.SendSafeboxCheckoutPacket(int(DOLU[bastir]) , int(BOS_ITEMS[bastir]))


def Depo_Ac():


    EnvanterTara()

    xx = Scan_Npc()
 
 
    if xx != -1:
 
        try:
            InstallQuestWindowHook()
        except:
            ZYNIX = 100
 

        yang = playerm2g2.GetMoney()
   
        if yang > 305000 and BAR == 1 and SONKARAKTER == 0:
       
            m2netm2g.SendOnClickPacket(xx)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            m2netm2g.SendOnClickPacket(xx)
            event.SelectAnswer(1, BUTONSIRA)
            event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
            event.SelectAnswer(1, 0)
            event.SelectAnswer(1, 0)
            m2netm2g.SendOnClickPacket(xx)
       
            event.SelectAnswer(1, MARKETSIRA)
            event.SelectAnswer(1, 1)
               
            while (yang > 305000 ):
               
                if yang > 2220000:
                    m2netm2g.SendShopBuyPacket(4)
                    yang = yang - 2020000
                elif yang > 1210000:
                    m2netm2g.SendShopBuyPacket(3)
                    yang = yang - 1010000
                elif yang > 705000:
                    m2netm2g.SendShopBuyPacket(2)
                    yang = yang - 505000
                elif yang > 305000:
                    m2netm2g.SendShopBuyPacket(1)
                    yang = yang - 101000
                if yang < 305000:
                    m2netm2g.SendShopEndPacket()
               
 

        else:
   
            kontrol = 0
       
            if SONKARAKTER == 1:
           
                for alayi in range(45):
                    if safebox.GetItemID(alayi) == None:
                        kontrol = 1
                        break
                    elif safebox.GetItemID(alayi) > 0:
                        kontrol = 1
                        break
                    elif safebox.GetItemID(alayi) == 0:
                        kontrol = 0
                        #break
           
       
            if ( kontrol == 1 and SONKARAKTER == 1 ) or ( len(FOUND_ITEMS) > 0 and SONKARAKTER == 0  ) :
       
                m2netm2g.SendOnClickPacket(xx)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                m2netm2g.SendOnClickPacket(xx)
                event.SelectAnswer(1, BUTONSIRA)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(1, 0)
                event.SelectAnswer(1, 0)
                m2netm2g.SendOnClickPacket(xx)
           
                event.SelectAnswer(1, BUTONSIRA)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                event.SelectAnswer(event.BUTTON_TYPE_NEXT, 255)
                try:
                    if constInfo.acikmi2(constInfo.parametre3) == 0:
                        ime.SetText(DEPOSIFRE)
                        ime.PasteBackspace()
                        ime.PasteReturn()
                except:
                    app.Exit()
            if len(FOUND_ITEMS) > 0 and SONKARAKTER == 0:
       
                DepoyaKoy()

            elif len(FOUND_ITEMS) == 0 and SONKARAKTER == 0:
       
                constInfo.kapat = 1

            elif SONKARAKTER == 1 :
           
                DepodanAl()

            else:
                UnHookQuestWindow()

def EsyalariDuzenle():
    BIRLESTIR = []
    BIRLESTIR2 = []
 
    for aslot in range(90):
        bID = player.GetItemIndex(1,aslot)
        if bID != 0:
           
            SAYI2 = player.GetItemCount(1,aslot)
               
            if SAYI2 < MAX_SAYI2:
                    BIRLESTIR.append(aslot)
                    BIRLESTIR2.append(bID)
               
    for TOPLA in range(len(BIRLESTIR)):
        for TOPLA2 in range(len(BIRLESTIR)):
            try:
           
                if TOPLA > TOPLA2:
                    continue
           
                elif int(BIRLESTIR2[TOPLA]) != int(BIRLESTIR2[TOPLA2]):
                    continue
               
                elif int(BIRLESTIR[TOPLA]) == int(BIRLESTIR[TOPLA2]):
                    continue
                else:
                    item.SelectItem(player.GetItemIndex(  int(BIRLESTIR[TOPLA]) ))
                    ItemTipi = item.GetItemType()
               
                    if ItemTipi != 6 and ItemTipi != 1 and ItemTipi != 2: # EVENT
                        net.SendItemMovePacket(1,int(BIRLESTIR[TOPLA2]),1, int(BIRLESTIR[TOPLA]), player.GetItemCount( MAX_SAYI2 ) )
            except:
                ZYNIX = 100

mt2pyv.DUR = 0

for dondura in range(90):
    if player.GetItemIndex(dondura) == 50269 or player.GetItemIndex(dondura) == 50277:
            sayisi = player.GetItemCount(dondura)
            mt2pyv.DUR = 1
            for toplam in range(sayisi):
                net.SendItemUsePacket(dondura)


yangs = player.GetMoney()
SetSayisi = player.GetItemCountByVnum(79506)

try:
    if mt2pyv.inGame:
        SANASOKAM = 3131
except:
    mt2pyv.inGame = False


if SetSayisi > 0 and yangs >= 31000 or mt2pyv.inGame:
    if Scan_Npc() != -1:
        mainokeyfunc()
elif yangs < 1000 and  Scan_Npc() != -1:
    chat.AppendChat(3,"Para YOK!")
    constInfo.kapat = 1
elif SetSayisi >= 0 and yangs <= 31000 and mt2pyv.DUR == 0:
    EsyalariDuzenle()
    Depo_Ac()
elif  mt2pyv.DUR == 0:
    EsyalariDuzenle()
    Depo_Ac()
