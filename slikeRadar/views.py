
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView

from slikeRadar.models import Slike, SlikeCMaxnoCor, SlikeBase, SlikeHmax, SlikeCappi, SlikeNowcast
from slikeRadar.models import GifSlike, GifSlikeCMaxnoCor, GifSlikeBase, GifSlikeHmax, GifSlikeCappi, GifSlikeNowcaste
from .models import SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL
from .models import SlikePPI, GifSlikePPI
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages


# Create your views here.
# used for CMax
class SlikeListView(LoginRequiredMixin, ListView):
    """view koji prikazuje CMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = Slike.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list.html'


# used for CMax
def query_four_hours_old():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = Slike.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if Slike.objects.filter(title__icontains=title_value):
        return Slike.objects.filter(title__icontains=title_value)
    else:
        return Slike.objects.all().order_by('title')[:1]


# used for CMax
class SearchResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = Slike
    template_name = "slikeRadar/serach_list.html"
    context_object_name = 'images'
    first_query = Slike.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = Slike.objects.filter(Q(time_create__icontains=query))
            #provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            #ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING, 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for CMax
class GifSlikeListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlike.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gifList.html'


# used for HMax
class SlikeHMaxListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeHmax.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_hmax.html'


# used for HMax
def query_four_hours_old_hmax():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeHmax.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeHmax.objects.filter(title__icontains=title_value):
        return SlikeHmax.objects.filter(title__icontains=title_value)
    else:
        return SlikeHmax.objects.all().order_by('title')[:1]


# used for HMax
class SearchHMaxResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeHmax
    template_name = "slikeRadar/search__hmax_list.html"
    context_object_name = 'images'
    first_query = SlikeHmax.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_hmax()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)
        print(query)
        if query is not None and query !='':
            object_list = SlikeHmax.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING, 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for HMax
class GifSlikeHmaxListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeHmax.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_hmax_list.html'


# used for Base
class SlikeBaseListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeBase.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_base.html'


# used for Base
def query_four_hours_old_base():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeBase.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeBase.objects.filter(title__icontains=title_value):
        return SlikeBase.objects.filter(title__icontains=title_value)
    else:
        return SlikeBase.objects.all().order_by('title')[:1]


# used for Base
class SearchBaseResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeBase
    template_name = "slikeRadar/search__base_list.html"
    context_object_name = 'images'
    first_query = SlikeBase.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_base()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeBase.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for Base
class GifSlikeBaseListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeBase.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_base_list.html'


# used for CMaxnoCor
class SlikeCMaxnoCorListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeCMaxnoCor.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_cmaxnocor.html'


# used for CMaxnoCor
def query_four_hours_old_cmaxnocor():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeCMaxnoCor.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeCMaxnoCor.objects.filter(title__icontains=title_value):
        return SlikeCMaxnoCor.objects.filter(title__icontains=title_value)
    else:
        return SlikeCMaxnoCor.objects.all().order_by('title')[:1]


# used for CMaxnoCor
class SearchCMaxnoCorResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeCMaxnoCor
    template_name = "slikeRadar/search__cmaxnocor_list.html"
    context_object_name = 'images'
    first_query = SlikeCMaxnoCor.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_cmaxnocor()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeCMaxnoCor.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for CMaxnoCor
class GifSlikeCMaxnoCorListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeCMaxnoCor.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_cmaxnocor_list.html'


# used for Cappi
class SlikeCappiListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeCappi.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_cappi.html'


# used for Cappi
def query_four_hours_old_Cappi():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeCappi.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeCappi.objects.filter(title__icontains=title_value):
        return SlikeCappi.objects.filter(title__icontains=title_value)
    else:
        return SlikeCappi.objects.all().order_by('title')[:1]


# used for Cappi
class SearchCappiResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeCappi
    template_name = "slikeRadar/search__cappi_list.html"
    context_object_name = 'images'
    first_query = SlikeCappi.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_Cappi()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeCappi.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for Cappi
class GifSlikeCappiListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeCappi.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_cappi_list.html'


# used for Nowcast
class SlikeNowcastListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeNowcast.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_nowcast.html'


# used for Nowcast
def query_four_hours_old_Nowcast():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeNowcast.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeNowcast.objects.filter(title__icontains=title_value):
        return SlikeNowcast.objects.filter(title__icontains=title_value)
    else:
        return SlikeNowcast.objects.all().order_by('title')[:1]


# used for Nowcast
class SearchNowcastResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeNowcast
    template_name = "slikeRadar/search__nowcast_list.html"
    context_object_name = 'images'
    first_query = SlikeNowcast.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_Nowcast()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeNowcast.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for Nowcast
class GifSlikeNowcastListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeNowcaste.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_nowcast_list.html'


# used for CMaxZDR
class SlikeCMaxZDRListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeCMaxZDR.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_CMaxZDR.html'


# used for CMaxZDR
def query_four_hours_old_CMaxZDR():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeCMaxZDR.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeCMaxZDR.objects.filter(title__icontains=title_value):
        return SlikeCMaxZDR.objects.filter(title__icontains=title_value)
    else:
        return SlikeCMaxZDR.objects.all().order_by('title')[:1]


# used for CMaxZDR
class SearchCMaxZDRResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeCMaxZDR
    template_name = "slikeRadar/search_CMaxZDR_list.html"
    context_object_name = 'images'
    first_query = SlikeCMaxZDR.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_CMaxZDR()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeCMaxZDR.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for CMaxZDR
class GifSlikeCMaxZDRListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeCMaxZDR.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_CMaxZDR_list.html'


# used for CMaxRainRate
class SlikeCMaxRainRateListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeCMaxRainRate.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_CMaxRainRate.html'


# used for CMaxRainRate
def query_four_hours_old_CMaxRainRate():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeCMaxRainRate.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeCMaxRainRate.objects.filter(title__icontains=title_value):
        return SlikeCMaxRainRate.objects.filter(title__icontains=title_value)
    else:
        return SlikeCMaxRainRate.objects.all().order_by('title')[:1]


# used for CMaxRainRate
class SearchCMaxRainRateResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeCMaxRainRate
    template_name = "slikeRadar/search_CMaxRainRate_list.html"
    context_object_name = 'images'
    first_query = SlikeCMaxRainRate.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_CMaxRainRate()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeCMaxRainRate.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))


# used for CMaxRainRate
class GifSlikeCMaxRainRateListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeCMaxRainRate.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_CMaxRainRate_list.html'


# used for VIL
class SlikeVILListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikeVIL.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_VIL.html'
# used for VIL
def query_four_hours_old_VIL():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikeVIL.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikeVIL.objects.filter(title__icontains=title_value):
        return SlikeVIL.objects.filter(title__icontains=title_value)
    else:
        return SlikeVIL.objects.all().order_by('title')[:1]
# used for VIL
class SearchVILResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikeVIL
    template_name = "slikeRadar/search_VIL_list.html"
    context_object_name = 'images'
    first_query = SlikeVIL.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_VIL()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikeVIL.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))
# used for VIL
class GifSlikeVILListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikeVIL.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_VIL_list.html'


# used for PPI
class SlikePPIListView(LoginRequiredMixin, ListView):
    """view koji prikazuje HMax current img"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = SlikePPI.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/list_PPI.html'
# used for PPI
def query_four_hours_old_PPI():
    """definisem metod kojim iyvlacim query star 4 satat kako bi se mogao koristit
        start i end time u SearchResultsView kada se gleda arhiva slike
        """
    # provjeravam koji je
    last_query = SlikePPI.objects.all().order_by('-title')[:1]
    # first_query = Slike.objects.all().order_by('title')[:1]
    # pravim dvije varijable u koje smijestam pocetni datum i vrijem
    start_time_date = ''
    # sa petljom  string u formatu '2023-01-21-0652' u varijablu start_time_date
    for a in last_query:
        start_time_date = a.title
    if start_time_date == '':
        today = timezone.now()
        start_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start time  pravim datetime object tako sto uzimam string title i pretvaram ga u datetime obj
    start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
    # end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')
    # definisem vrijeme unayad 4 sata kako bi izdvoji   query unutar toga
    end_time = start_time - timedelta(hours=4)
    # definisem title od query koji je star 4 sata
    title_value = end_time.strftime("%Y-%m-%d-%H%M")
    if SlikePPI.objects.filter(title__icontains=title_value):
        return SlikePPI.objects.filter(title__icontains=title_value)
    else:
        return SlikePPI.objects.all().order_by('title')[:1]
# used for PPI
class SearchPPIResultsView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax arhive slika"""
    model = SlikePPI
    template_name = "slikeRadar/search_PPI_list.html"
    context_object_name = 'images'
    first_query = SlikePPI.objects.all().order_by('-title')[:1]
    last_query = query_four_hours_old_PPI()
    extra_context = {'first_query': first_query, 'last_query': last_query}

    def get_queryset(self):  # new
        query = self.request.GET.get("q", None)

        if query is not None and query !='':
            object_list = SlikePPI.objects.filter(Q(time_create__icontains=query))
            # provjeravam da li je prazan Query set tj da li ima podatak u db  za vrijednost q ako ima izvrsi sledece
            if object_list.exists():
                print(query)
                print(object_list)
                return object_list
            # ovde treba da iskoci alarm messages tj kada nema uneseno vrijeme onda da iskoci alalrm message
            print(object_list)
            messages.add_message(self.request, messages.WARNING,
                                 'No data found in database for time {}UTC!'.format(query))

        # return Slike.objects.all().order_by('-title')[:1]
        # return Slike.objects.filter(Q(time_create__icontains='None'))

# used for PPI
class GifSlikePPIListView(LoginRequiredMixin, ListView):
    """ view koji se koristi ya prikaz CMax GIF slika"""
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = GifSlikePPI.objects.all().order_by('-title')
    paginate_by = 1
    context_object_name = 'images'
    template_name = 'slikeRadar/gif_PPI_list.html'






class SlikeOlderView(LoginRequiredMixin, ListView):
    # u slucaju kada koristimo default menager onda stavljamo umjesto queryset model
    queryset = Slike.objects.all().order_by('-title')
    paginate_by = 20
    context_object_name = 'images'
    extra_context = {'probas': Slike.objects.all().order_by('-title')[:1]}
    template_name = 'slikeRadar/list_older.html'


class SlikeDetailView(LoginRequiredMixin, DetailView):
    model = Slike
    context_object_name = 'images'
    extra_context = {'probas': Slike.objects.all().order_by('-title')[:20]}
    template_name = 'slikeRadar/list_detail.html'

def search(request):
    query_data = Slike.objects.all()
    date_filter = SlikeFilter(request.GET, queryset=query_data)
    return render(request, 'slikeRadar/serach_list.html', {'filter': date_filter})

class SearchView(LoginRequiredMixin, TemplateView):
    """samo privremeno koristio radi testa"""
    template_name = "slikeRadar/search.html"

