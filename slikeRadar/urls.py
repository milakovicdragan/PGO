from django.urls import path

from .views import SlikeListView, GifSlikeListView, SearchResultsView, SlikeHMaxListView, SearchHMaxResultsView, \
    GifSlikeHmaxListView, SlikeBaseListView, SearchBaseResultsView, GifSlikeBaseListView, SlikeCMaxnoCorListView, \
    SearchCMaxnoCorResultsView, GifSlikeCMaxnoCorListView, SlikeCappiListView, SearchCappiResultsView, GifSlikeCappiListView, \
    SlikeNowcastListView, SearchNowcastResultsView, GifSlikeNowcastListView, SlikeCMaxZDRListView, SearchCMaxZDRResultsView, \
    GifSlikeCMaxZDRListView, SlikeCMaxRainRateListView, SearchCMaxRainRateResultsView, GifSlikeCMaxRainRateListView, \
    SlikeVILListView, SearchVILResultsView, GifSlikeVILListView, SlikePPIListView, SearchPPIResultsView, GifSlikePPIListView

urlpatterns = [
    # prikazuje CMax slike
    path("", SlikeListView.as_view(), name="home"),
    path("radar/archiva/CMax/result", SearchResultsView.as_view(), name="archiva_search"),
    path("radar/gif/CMax", GifSlikeListView.as_view(), name="borja_gif"),
    # prikazuje HMax slike
    path("radar/img/hmax", SlikeHMaxListView.as_view(), name="home_hmax"),
    path("radar/archiva/HMax/result", SearchHMaxResultsView.as_view(), name="archiva_search_hmax"),
    path("radar/gif/HMax", GifSlikeHmaxListView.as_view(), name="gif_hmax"),
    # prikazuje Base slike
    path("radar/img/base", SlikeBaseListView.as_view(), name="home_base"),
    path("radar/archiva/Base/result", SearchBaseResultsView.as_view(), name="archiva_search_base"),
    path("radar/gif/Base", GifSlikeBaseListView.as_view(), name="gif_base"),
    # prikazuje CMaxnoCor slike
    path("radar/img/cmaxnocor", SlikeCMaxnoCorListView.as_view(), name="home_cmaxnocor"),
    path("radar/archiva/CMaxnoCor/result", SearchCMaxnoCorResultsView.as_view(), name="archiva_search_cmaxnocor"),
    path("radar/gif/CMaxnoCor", GifSlikeCMaxnoCorListView.as_view(), name="gif_cmaxnocor"),
    # prikazuje Cappi slike
    path("radar/img/cappi", SlikeCappiListView.as_view(), name="home_cappi"),
    path("radar/archiva/Cappi/result", SearchCappiResultsView.as_view(), name="archiva_search_cappi"),
    path("radar/gif/Cappi", GifSlikeCappiListView.as_view(), name="gif_cappi"),
    # prikazuje Nowcast slike
    path("radar/img/nowcast", SlikeNowcastListView.as_view(), name="home_nowcast"),
    path("radar/archiva/Nowcast/result", SearchNowcastResultsView.as_view(), name="archiva_search_nowcast"),
    path("radar/gif/Nowcast", GifSlikeNowcastListView.as_view(), name="gif_nowcast"),
    # prikazuje CMaxZDR slike
    path("radar/img/cmaxzdr", SlikeCMaxZDRListView.as_view(), name="home_cmaxzdr"),
    path("radar/archiva/cmaxzdr/result", SearchCMaxZDRResultsView.as_view(), name="archiva_search_cmaxzdr"),
    path("radar/gif/cmaxzdr", GifSlikeCMaxZDRListView.as_view(), name="gif_cmaxzdr"),
    # prikazuje CMaxRainRate slike
    path("radar/img/cmaxrainrate", SlikeCMaxRainRateListView.as_view(), name="home_cmaxrainrate"),
    path("radar/archiva/cmaxrainrate/result", SearchCMaxRainRateResultsView.as_view(), name="archiva_search_cmaxrainrate"),
    path("radar/gif/cmaxrainrate", GifSlikeCMaxRainRateListView.as_view(), name="gif_cmaxrainrate"),
    # prikazuje VIL slike
    path("radar/img/vil", SlikeVILListView.as_view(), name="home_vil"),
    path("radar/archiva/vil/result", SearchVILResultsView.as_view(), name="archiva_search_vil"),
    path("radar/gif/vil", GifSlikeVILListView.as_view(), name="gif_vil"),
    # prikazuje PPI slike
    path("radar/img/ppi", SlikePPIListView.as_view(), name="home_ppi"),
    path("radar/archiva/ppi/result", SearchPPIResultsView.as_view(), name="archiva_search_ppi"),
    path("radar/gif/ppi", GifSlikePPIListView.as_view(), name="gif_ppi"),




    # path("older/", SlikeOlderView.as_view(), name="archiva_borja"),
    # path("archiva/<int:pk>", SlikeDetailView.as_view(), name="archiva_borja_detail"),
    # path("terms/<int:page>", listing, name="terms-by-page"),
    # path("borja/search/", search, name="search"),
    # path("borja/archiva/", SearchView.as_view(), name="search"),
    # path("terms.json", listing_api, name="terms-api"),

]
