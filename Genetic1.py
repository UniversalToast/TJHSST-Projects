import random
import operator
from math import log2
import sys

TEXT = sys.argv[1]
POPULATION_SIZE = 300  # very large for the short texts, can be smaller for larger texts
Ngram = 3
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN = .75
CROSSOVER = 5
MUTATION = .8
CLONES = 1
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = list(alphabet)
alphabetdict = dict()
gram_1 = dict()
gram_2 = dict()
gram_3 = dict()
gram_4 = dict()
for a, b in enumerate(alphabet):
    alphabetdict[a] = b


def generate_ngram():
    cur = gram_1
    with open("ngrams1.tsv") as f:
        for line in f:
            if line[0] == "1":
                continue
            if line[0] == "2":
                cur = gram_2
                continue
            elif line[0] == "3":
                cur = gram_3
                continue
            elif line[0] == "4":
                cur = gram_4
                continue
            elif line[0] == "5":
                break
            line = line.split()
            cur[line[0]] = log2(int(line[1]))


def randomalphabet():
    temp = alphabet.copy()
    random.shuffle(temp)
    tempdict = dict()
    for a, b in enumerate(temp):
        tempdict[b] = a
    return tempdict


population = []
for a in range(POPULATION_SIZE):
    population.append(randomalphabet())


def rate(text):
    rating = 0
    for a in text.split():
        length = len(a)
        if length>=4:
            cur = a[:4]
            if cur in gram_4:
                rating += gram_4[cur]
            for b in range(4, length):
                cur = cur[1:] + a[b]
                if cur in gram_4:
                    rating += gram_4[cur]
        elif length>=3:
            if a in gram_3:
                rating += gram_3[a]
        elif length>=2:
            if a in gram_2:
                rating += gram_2[a]
        else:
            if a in gram_1:
                rating += gram_1[a]
    return log2(rating)

# def rate(text):
#     rating = 0
#     for a in text.split():
#         length = len(a)
#         if length >= 3:
#             cur = a[:3]
#             if cur in gram_3:
#                 rating += gram_3[cur]
#             else:
#                 rating += -10
#             for b in range(3, length):
#                 cur = cur[1:] + a[b]
#                 if cur in gram_3:
#                     rating += gram_3[cur]
#                 else:
#                     rating += -10
#     return rating


# cipher is dictionary
def decode(cipher, text):
    temp = []
    for a in text:
        try:
            temp.append(alphabetdict[cipher[a]])
        except:
            temp.append(a)
    b = ''.join(temp)
    return b


generate_ngram()


# Ratingdict has the key values corresponding to the rating,
# contestants are what keys are being competed
def tournament(contestants, ratingdict):
    c = c1 = c2 = 0
    cur = cur1 = cur2 = -1000000000
    for a in contestants:
        if ratingdict[a] > cur:
            cur2 = cur1
            cur1 = cur
            cur = ratingdict[a]
            c2 = c1
            c1 = c
            c = a
    if random.random() > TOURNAMENT_WIN:
        if random.random() > TOURNAMENT_WIN:
            if c2 != 0:
                return c2
            elif c1 != 0:
                return c1
        elif c1 != 0:
            return c1
    return c


def mutate(dict):
    a = random.choice(alphabet)
    b = random.choice(alphabet)
    temp = dict[a]
    dict[a] = dict[b]
    dict[b] = temp


def breed(one, two):
    onekeys = one.keys()
    twokeys = sorted(two.items(), key=operator.itemgetter(1))
    usedletters = set()
    numbers = [a for a in range(25, -1, -1)]
    new = dict()
    crossover = CROSSOVER
    for a in onekeys:
        if random.random() < .65:
            continue
        if crossover == 0:
            break
        usedletters.add(a)
        new[a] = one[a]
        numbers.remove(one[a])
        crossover += -1
    for b, c in twokeys:
        if b not in usedletters:
            new[b] = numbers.pop()
    if random.random() < MUTATION:
        mutate(new)
    return new


def generatenew(ratings, keypop, keydict):
    ratingsdict = dict()  # keys of each dictionary lead to their rating
    keys = []  # identifier for the dict since it cannot be hashed, is a list of the keys
    keysdict = dict()  # connects to list keys to their dictionary
    decodedset = set()  # because keys are unordered, I can check to make sure no messages are the same
    for a in range(CLONES):
        new = keydict[max(ratings.items(), key=operator.itemgetter(1))[0]]
        msg = decode(new, TEXT)
        decodedset.add(msg)
        key = tuple(new.keys())
        keys.append(key)
        keysdict[key] = new
        ratingsdict[key] = rate(msg)
    for a in range(1):
        new = keydict[max(ratings.items(), key=operator.itemgetter(1))[0]]
        mutate(new)
        msg = decode(new, TEXT)
        decodedset.add(msg)
        key = tuple(new.keys())
        keys.append(key)
        keysdict[key] = new
        ratingsdict[key] = rate(msg)
    x = CLONES
    while x < 500:
        contestants = random.sample(keypop, 40)
        contestants1 = contestants[:20]
        contestants2 = contestants[21:]
        winner1 = tournament(contestants1, ratings)
        winner2 = tournament(contestants2, ratings)
        new = breed(keydict[winner1], keydict[winner2])
        msg = decode(new, TEXT)
        if msg in decodedset:
            continue
        else:
            x += 1
            decodedset.add(msg)
            key = tuple(new.keys())
            keys.append(key)
            keysdict[key] = new
            ratingsdict[key] = rate(msg)
    print(decode(keysdict[max(ratingsdict.items(), key=operator.itemgetter(1))[0]], TEXT))
    return ratingsdict, keys, keysdict


ratingsdict1 = dict()
keys1 = []
keysdict1 = dict()
for a in population:
    msg1 = decode(a, TEXT)
    key1 = tuple(a.keys())
    keys1.append(key1)
    keysdict1[key1] = a
    ratingsdict1[key1] = rate(msg1)
for a in range(500):
    ratingsdict1, keys1, keysdict1 = generatenew(ratingsdict1, keys1, keysdict1)
# print(population[0])
# print(population[1])
# print(breed(population[0],population[1]))
