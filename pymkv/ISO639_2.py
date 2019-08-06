# sheldon woodward
# 3/18/18

"""ISO639-2 Three Character Language Codes"""

from iso639 import languages

def is_ISO639_2(language):
  try:
    languages.get(part2b=language)
    return True
  except KeyError:
    return False
