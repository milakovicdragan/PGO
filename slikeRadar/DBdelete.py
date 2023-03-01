from .models import Slike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor
from .models import GifSlike, GifSlikeCappi, GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor
from .models import SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL
from .models import SlikePPI, GifSlikePPI

models = [Slike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor,
          GifSlike, GifSlikeCappi, GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor,
          SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL,
          SlikePPI, GifSlikePPI]

def delete_db_all():
    for Model in models:
        Model.objects.all().delete()