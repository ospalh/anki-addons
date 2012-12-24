#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import codecs
import cPickle
import random
import re

from anki.hooks import addHook
from anki.notes import Note
from aqt import mw

# Info on data base:
# http://www.edrdg.org/wiki/index.php/Tanaka_Corpus
#
# Data base. NB. EUC-JP encoding
# http://www.csse.monash.edu.au/~jwb/examples.gz

# --Change this value to set the number of examples you wish to have appear in the card
MAX = 1

# Code from previous version, modified to work with the new version of Anki
# file containing the Tanaka corpus sentences
file = os.path.join(mw.pm.addonFolder(), "example_sentences.txt")
file_pickle = os.path.join(mw.pm.addonFolder(), "example_sentences.pickle")
f = codecs.open(file, 'rb', 'utf8')
content = f.readlines()
f.close()
dictionary = {}

def build_dico():
    splitter = re.compile('\s|\[|\]|\(|\{|\)|\}').split
    for i, line in enumerate(content[1::2]):
        words = set(splitter(line)[:-1])
        for word in words:
            if word in dictionary and not word.isdigit():
                dictionary[word].append(2*i)
            elif not word.isdigit():
                dictionary[word]=[]
                dictionary[word].append(2*i)


if (os.path.exists(file_pickle) and
    os.stat(file_pickle).st_mtime > os.stat(file).st_mtime):
    f = open(file_pickle, 'rb')
    dictionary = cPickle.load(f)
    f.close()
else:
    build_dico()
    f = open(file_pickle, 'wb')
    cPickle.dump(dictionary, f, cPickle.HIGHEST_PROTOCOL)
    f.close()

def find_examples(expression):
    info_question = ""
    info_answer = ""

    if expression in dictionary:
            examples_question = []
            examples_answer = []
            index = dictionary[expression]
            index = random.sample(index, min(len(index),MAX))
            for j in index:
                example = content[j].split("#ID=")[0][3:]
                example = example.replace(expression,'<FONT COLOR="#ff0000">%s</FONT>' %expression)
                color_example = content[j+1]
                regexp = "(?:\(*%s\)*)(?:\([^\s]+?\))*(?:\[\d+\])*\{(.+?)\}" %expression
                match = re.compile("%s" %regexp).search(color_example)
                if match:
                    expression_bis = match.group(1)
                    example = example.replace(expression_bis,'<FONT COLOR="#ff0000">%s</FONT>' %expression_bis)
                else:
                    example = example.replace(expression,'<FONT COLOR="#ff0000">%s</FONT>' %expression)
                examples_question.append("<br>%s<br>" % example.split('\t')[0])
                examples_answer.append("<br>%s<br>%s<br>" % tuple(example.split('\t')))
            info_question = "".join(examples_question)
            info_answer = "".join(examples_answer)
    return (info_question,info_answer)




def append_example_QA ():
    f = mw.reviewer.card.note()
    try:
        (f["QExample"], f["AExample"]) = find_examples(f["Front"])
        f.flush()
        f.load()
        return
    except:
        return

addHook("showQuestion", append_example_QA)
