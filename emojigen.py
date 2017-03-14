'''
  This file is part of emojigen.
  emojigen is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  emojigen is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with emojigen.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys, json, random, os

class WordMapGen:
  def __init__(self, filename, force_regen):
    self.wordmap = {}
    self.filename = filename
    self.force_regen = force_regen
  def add(self, emoji, word):
    if word in self.wordmap:
      self.wordmap[word].append(emoji)
    else:
      self.wordmap[word] = [emoji]
  def add_multi(self, emoji, words):
    for w in words:
      self.add(emoji, w)
  def gen_word_map(self):
    if not self.force_regen:
      emojimap_time = os.stat('EMOJIMAP').st_mtime
      wordmap_time = os.stat('wordmap.json').st_mtime
      if wordmap_time > emojimap_time:
        return
    emojimap = open(self.filename, 'r')
    for line in emojimap:
      data = line.split()
      self.add_multi(data[0], data[1:])
    wordmap = open('wordmap.json', 'w')
    json.dump(self.wordmap, open('wordmap.json', 'w'), indent=4,
        separators=(',', ': '))
  @staticmethod
  def run(filename, force_regen):
    WordMapGen(filename, force_regen).gen_word_map()

class Emojigen:
  def __init__(self, text, coef):
    self.words = text.split()
    self.wordmap = json.load(open('wordmap.json', 'r'))
    self.coef = coef
  def get_emojis_for(self, word):
    if word in self.wordmap:
      return self.wordmap[word]
    if len(word) >= 3:
      return self.get_emojis_for(word[:-1])
    return []
  def get_emoji_for(self, word):
    if random.random() > self.coef:
      return ''
    emojis = self.get_emojis_for(word)
    if len(emojis):
      return random.choice(emojis)
    return ''
  def decorate(self):
    out = ''
    for w in self.words:
      emo = self.get_emoji_for(w)
      if len(emo):
        out += w + emo + '  '
      else:
        out += w + ' '
    return out

if __name__ == '__main__':
    emoji_coef = 1
    emojimap = 'EMOJIMAP'
    force_regen = False
    if len(sys.argv) >= 2:
      text = sys.argv[1]
      if len(sys.argv) >= 3:
        emoji_coef = float(sys.argv[2])
        if len(sys.argv) >= 4:
          emojimap = sys.argv[3]
          if len(sys.argv) >= 5:
            force_regen = True
    else:
      text = sys.stdin.readline()
    WordMapGen.run(emojimap, force_regen)
    print Emojigen(text, emoji_coef).decorate()
