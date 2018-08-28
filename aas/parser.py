from aas.models import HashtagList
from django.utils.html import escape
from pyparsing import Word, alphanums, Combine

rus_alphas = 'йцукеёнгшщзхъфывапролджэячсмитьбюЙЦУКЕЁНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'


hash_list = []

def hashtag_append(strg, loc, toks):
    try:
        hashtag = HashtagList.objects.get(hashtag=toks[0][1:])
        hashtag.popularity += 1
        hashtag.save()
    except HashtagList.DoesNotExist:
        hashtag = HashtagList()
        hashtag.hashtag = toks[0][1:]
        hashtag.save()

    hash_list.append(hashtag)

    # lambda toks: '< href={{{{ url hashtag/ {} }}}} > {} </a>'.format(toks.asList()[0][1:],toks.asList()[0])
    #return '[a href=r"{{% url "hashtag" {} %}}"] {} [/a]'.format(toks[0][1:], toks[0])
    return "[url=/hashtag/{}] {} [/url]".format(toks[0][1:], toks[0])

hasa = Combine('#' + Word(alphanums + '_' + rus_alphas)).setParseAction(hashtag_append)