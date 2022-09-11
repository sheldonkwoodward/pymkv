# sheldon woodward
# 10/21/20

"""BCP47 language region code"""

import bcp47


def is_bcp47(language_ietf):
    if language_ietf == "und":
        return True
    else:
        return language_ietf in bcp47.languages.values()
