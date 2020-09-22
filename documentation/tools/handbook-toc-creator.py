# -*- coding: utf-8 -*-
"""
BSD 2-Clause License

Copyright (c) 2020, The FreeBSD Project
Copyright (c) 2020, Sergio Carlavilla

This script will generate the Table of Contents of the Handbook
"""
#!/usr/bin/env python3

import sys, getopt
import re

language = 'en' # English by default

def setAppendixTitle(language):
  languages = {
    'en': 'Appendix',
    'de': 'Anhang',
    'gr': 'Παράρτημα',
    'es': 'Apéndice',
    'fr': 'Annexe',
    'hu': 'függelék',
    'it': 'Appendice',
    'jp': '付録',
    'mn': 'Хавсралт',
    'nl': 'Bijlage',
    'br': 'Apêndice',
    'ru': 'Приложение',
    'cn': '附录',
    'tw': '附錄'
  }

  return languages.get(language)

def setPartTitle(language):
  languages = {
    'en': 'Part',
    'de': 'Teil',
    'gr': 'Μέρος',
    'es': 'Parte',
    'fr': 'Partie',
    'hu': 'rész',
    'it': 'Parte',
    'jp': 'パート〓',
    'mn': 'хэсэг',
    'nl': 'Deel',
    'br': 'Parte',
    'ru': 'Часть',
    'cn': '部分',
    'tw': '部'
  }

  return languages.get(language)

def setChapterTitle(language):
  languages = {
    'en': 'Chapter',
    'de': 'Kapitel',
    'gr': 'Κεφάλαιο',
    'es': 'Capítulo',
    'fr': 'Chapitre',
    'hu': 'Fejezet',
    'it': 'Capitolo',
    'jp': '章',
    'mn': 'Бүлэг',
    'nl': 'Hoofdstuk',
    'br': 'Capítulo',
    'ru': 'Глава',
    'cn': '章',
    'tw': '章'
  }

  return languages.get(language)

def setTOCTitle(language):
  languages = {
    'en': 'Table of Contents',
    'de': 'Inhaltsverzeichnis',
    'gr': 'Πίνακας Περιεχομένων',
    'es': 'Tabla de contenidos',
    'fr': 'Table des matières',
    'hu': 'Tartalom',
    'it': 'Indice',
    'jp': '目次',
    'mn': 'Гарчиг',
    'nl': 'Inhoudsopgave',
    'br': 'Índice',
    'ru': 'Содержание',
    'cn': '目录',
    'tw': '內容目錄'
  }

  return languages.get(language)

def getPartNumber(number):
  numbers = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V'
  }

  return numbers.get(number)

def checkIsPart(chapter):
  if ("part" in chapter):
    return True
  return False

def checkIsPreface(chapterContent):
  if ("[preface]" in chapterContent):
    return True
  return False

def checkIsAppendix(chapterContent):
  if ("[appendix]" in chapterContent):
    return True
  return False

def main(argv):

  try:
    opts, args = getopt.getopt(argv,"hl:",["language="])
  except getopt.GetoptError:
    print('handbook-toc-creator.py -l <language>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('handbook-toc-creator.py -l <language>')
      sys.exit()
    elif opt in ("-l", "--language"):
      language = arg

  chapters = []
  with open('./content/{}/books/handbook/chapters-order.adoc'.format(language), 'r', encoding = 'utf-8') as chaptersFile:
    chapters = [line.strip() for line in chaptersFile]

  toc =  "// Code generated by the FreeBSD Documentation toolchain. DO NOT EDIT.\n"
  toc += "// Please don't change this file manually but run `make` to update it.\n"
  toc += "// For more information, please read the FreeBSD Documentation Project Primer\n\n"
  toc += "[.toc]\n"
  toc += "--\n"
  toc += '[.toc-title]\n'
  toc += setTOCTitle(language) + '\n\n'

  chapterCounter = 1
  subChapterCounter = 1
  partCounter = 1
  for chapter in chapters:
    with open('./content/{0}/books/handbook/{1}'.format(language, chapter), 'r', encoding = 'utf-8') as chapterFile:
      chapterContent = chapterFile.read().splitlines()
      chapterFile.close()
      chapter = chapter.replace("/_index.adoc", "")

      if (checkIsPart(chapter)):
        for lineNumber, chapterLine in enumerate(chapterContent, 1):
          if (re.match(r"^={1} [^\n]+", chapterLine)):
            toc += "* link:{0}[{1} {2}. {3}]\n".format(chapter, setPartTitle(language), getPartNumber(partCounter), chapterLine.replace("=", "").strip())
        partCounter += 1

      elif (checkIsPreface(chapterContent)):
        for lineNumber, chapterLine in enumerate(chapterContent, 1):
          if (re.match(r"^={1} [^\n]+", chapterLine)):
            toc += "* link:{0}[{1}]\n".format(chapter, chapterLine.replace("=", "").strip())

      elif (checkIsAppendix(chapterContent)):
        for lineNumber, chapterLine in enumerate(chapterContent, 1):
          if (re.match(r"^={1} [^\n]+", chapterLine)):
            toc += "** link:{0}[{1} {2}]\n".format(chapter, setAppendixTitle(language), chapterLine.replace("=", "").strip())
          elif (re.match(r"^={2} [^\n]+", chapterLine)):
            toc += "*** link:{0}/#{1}[{2}]\n".format(chapter, chapterContent[lineNumber-3].replace("[[", "").replace("]]", ""), chapterLine.replace("==", "").lstrip())

      else: # Normal chapter
        for lineNumber, chapterLine in enumerate(chapterContent, 1):
          if (re.match(r"^={1} [^\n]+", chapterLine)):
            toc += "** link:{0}[{1} {2}. {3}]\n".format(chapter, setChapterTitle(language), chapterCounter, chapterLine.replace("=", "").strip())
          elif (re.match(r"^={2} [^\n]+", chapterLine)):
            toc += "*** link:{0}/#{1}[{2}.{3}. {4}]\n".format(chapter, chapterContent[lineNumber-3].replace("[[", "").replace("]]", ""), chapterCounter, subChapterCounter, chapterLine.replace("==", "").lstrip())
        chapterCounter += 1
        subChapterCounter = 1

  toc += "--\n"

  with open('./content/{}/books/handbook/toc.adoc'.format(language), 'w', encoding = 'utf-8') as tocFile:
    tocFile.write(toc)

if __name__ == "__main__":
  main(sys.argv[1:])
