from django.contrib import admin
from .models import Slike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor
from .models import GifSlike, GifSlikeCappi, GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor
from .models import SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL
from .models import SlikePPI, GifSlikePPI


# Register your models here.

# prvo cu registrovati Slike model u Admin dijelu
@admin.register(Slike, GifSlike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor, GifSlikeCappi,
                SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL, SlikePPI,
                GifSlikePPI,
                GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor)
class SlikeAdmin(admin.ModelAdmin):
    list_display = ['title', 'img', 'descr', 'time_create', 'uploaded']
    ordering = ['uploaded']
