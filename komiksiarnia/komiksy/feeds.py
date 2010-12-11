from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404

from models import Pasek, Seria, User

class KomiksyRSS(Feed):
    title = "Komiksy"
    link = "/"
    description = "Najnowsze komiksy na komiksiarnia.net."

    def get_object(self, bits):

        if not bits or len(bits)<2: u=None
        else: u = get_object_or_404(User, username=bits[1])

        if not bits or bits[0]=='*': s = None
        else: s = get_object_or_404(Seria, tytul=bits[0])

        return dict(user=u, seria=s)

    title_template = "komiksy/pasek_feed_title.html"
    description_template = "komiksy/pasek_feed_description.html"

    def items(self, obj):
        pp = Pasek.objects.all()
        if obj['user'] is not None: 
            pp = pp.exclude(
                seria__in=obj['user'].get_profile().serie_ignorowane.all() )
        elif obj['seria'] is not None:
            pp = pp.filter(seria=obj['seria'])
        return pp.order_by('-id')[:50]
    
class KomiksyAtom(KomiksyRSS):
    feed_type = Atom1Feed
    subtitle = KomiksyRSS.description
