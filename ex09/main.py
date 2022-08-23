from translator import Translator
from language import Language


if __name__ == '__main__':
    t = Translator()
    print(t.translate(Language.PORTUGUESE, Language.ENGLISH, 'gestão'))

