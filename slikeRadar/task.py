from slikeRadar.models import Slike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor, \
    GifSlike, GifSlikeCappi, GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor, \
    SlikeCMaxZDR, GifSlikeCMaxZDR, SlikeCMaxRainRate, GifSlikeCMaxRainRate, SlikeVIL, GifSlikeVIL, \
    SlikePPI, GifSlikePPI
from slikeRadar.ImgToDB import ConvertNameToDateTime
from datetime import datetime, timedelta
from django.utils import timezone

models = [Slike, SlikeCappi, SlikeHmax, SlikeBase, SlikeNowcast, SlikeCMaxnoCor,
          SlikeCMaxZDR, SlikeCMaxRainRate, SlikeVIL, SlikePPI]
GIFmodels = [GifSlike, GifSlikeCappi, GifSlikeHmax, GifSlikeBase, GifSlikeNowcaste, GifSlikeCMaxnoCor,
             GifSlikeCMaxZDR, GifSlikeCMaxRainRate, GifSlikeVIL, GifSlikePPI]


def delete_slike_jpg_task():
    """
    Treba je dopuniti kako bi samo yadnjih 4 sata bilo prisutno u db
    Metod kojim cu da brisem iz DB sve jpg slike koje su strarije od time_inc koja je u satima
    """
    # definisem vrijeme unazad od zadnje primljnje slike
    # i sa time_inc kazem sve sto je starije od time_inc obrisi iz db
    time_inc = 4

    for model in models:
        # provjerava da li postoji datum i vrijeme za brisanje slika
        if time_query_iteration(model, time_inc):
            # obrisi sve slike iz baze od slike sa nazivom  title_value ka prvoj uneenoj slici
            # ali ne brisi sliku sa nazivom title_value
            title_value = time_query_iteration(model, time_inc)
            model.objects.filter(title__lt=title_value).delete()


def time_query_iteration(model, time_inc):
    """
        Ovaj metod ce da iyracuna koja je posljenjda slika u odnosu na ydnju sliku za
        vremenski period definisan sa time_inc koji predstavlja sate.
        Odnosno metod ce me reci koja je slika 4 sata starija u odnosu na zadnju primljenu sliku u db

        :model je nayiv modela iy db za koji se pravi guery u raymaku definisanim sa time_inc
        :time_inc je intejdzer koji kaze u kojem vremenskom razamku se uzima slika npr svakih 15, 20 min...
        :return vraza  queri koji time_inc stariji od zadnjeg primljenje slike
        """

    # definisem query za zadnju sliku koja je primljna u db
    last_query = model.objects.all().order_by('-title')[:1]
    # first_query = model.objects.all().order_by('title')[:1]
    # pravim  varijabl u koje smijestam datum i vrijem zadnje primljene slike tj title iy modela
    # za pocetak cu u nju staviti defaltnu vrijednost
    last_img_time_date = ''
    for a in last_query:
        last_img_time_date = a.title
    # stavit cu trnutni datum i vrijeme ukolikoo nema podatka u db i to ce biti default vrijednost
    if last_img_time_date == '':
        today = timezone.now()
        last_img_time_date = today.strftime("%Y-%m-%d-%H%M")
    # sa start_time pravim datetime object tako sto uzimam string od title i pretvaram ga u datetime obj
    start_time = datetime.strptime(last_img_time_date, '%Y-%m-%d-%H%M')
    # print(start_time - timedelta(hours=time_inc))
    # pravim title_valu u kou stavljav title od slike koja je starija time_inc od yadnje primljene slike
    title_value = start_time - timedelta(hours=time_inc)
    title_value = title_value.strftime("%Y-%m-%d-%H%M")
    return title_value


def delete_slike_gif_task():
    """
    Metod kojim cu da brisem sve gif slike sem zadnje kreirne slike.
    Ovaj metod prolazi kroz petlju i obrisat ce u svakom GIF modelu sve sem zadnje slike
    koja je kreirana
    """
    # pravim qury_gif i u njega smijestam zadnju napravljenu sliku
    # pravim petlju kroz sve GIF modele u db kako bih ostavio samo zadnju sliku
    for GIFmodel in GIFmodels:
        query_gif = GIFmodel.objects.order_by('-title')[:1]
        last_created_gif = ''
        for date in query_gif:
            last_created_gif = date.uploaded
        if last_created_gif == "":
            last_created_gif = timezone.now()
        GIFmodel.objects.filter(uploaded__lt=last_created_gif).delete()
    # query_gif = GifSlike.objects.order_by('-title')[:1]
    # last_created_gif = ''
    # for date in query_gif:
    #     last_created_gif = date.uploaded
    # GifSlike.objects.filter(uploaded__lt=last_created_gif).delete()


def import_image_to_db_task():
    """
    Metoda kojom se importuje slika iz Queue foldera u DB svakih 1 minuta
    Provjerava se koja vrste slike je upitanju ismjesta se u odgovaraju model od DB
    """
    img_to_db = ConvertNameToDateTime()
    img_to_db.rename_img_save_to_db()


def create_gif_task():
    """
    Metod kojim se kreiraju gif slike iz db, prvo se provjerava da li ima jpg slika u db
    ako ima jpg. onda provjerava da li ima gif slika, ako ima gif slika onda provjerava da li je title od gif slike
    isti kao kod jpg slike ako je isti ne pravi se novi gif jer nije dosla nova jpg slika
    Ovde se difinise model ya koji se pravi gif slika ide se kroz petlju i definise se koji vremenski razmak
    izmedju slika ce se koristit.
    :GIFmodel definise  za koji GIF model u db se pravi GIF slika
    :model definise model u DB iy kojeg ce uzimati jpg slike kako bi se napravila GIF slike
    :time_inc definise vremenski razamak imedju dvije susjedne slike npr 20, 30min
    Ovaj metod krece od nastarije jpg slike u db do najnovije slike, prema tome treba velicinu slika u db
    drzati na 4 sata pomocu metoda delete_slike_jpg_task()
    """
    time_inc = 15
    # prolayim kroz petlju gdje za svaki model uzimam odgovarajuci GIF model
    for model, GIFmodel in zip(models, GIFmodels):
        img_jpg = model.objects.all()
        img_gif_to_db = ConvertNameToDateTime()

        if img_jpg.exists():
            if GIFmodel.objects.all().exists():
                if GIFmodel.objects.all().latest('title').title != img_jpg.latest('title').title:
                    # query_to_create_gif(self, GIFmodel, model, time_inc)
                    img_gif_to_db.query_to_create_gif(GIFmodel, model, time_inc)
            else:
                img_gif_to_db.query_to_create_gif(GIFmodel, model, time_inc)

    # img_jpg = Slike.objects.all()
    # img_gif_to_db = ConvertNameToDateTime()
    #
    # if img_jpg.exists():
    #     if GifSlike.objects.all().exists():
    #         if GifSlike.objects.all().latest('title').title != img_jpg.latest('title').title:
    #             # query_to_create_gif(self, GIFmodel, model, time_inc)
    #             img_gif_to_db.query_to_create_gif()
    #     else:
    #         img_gif_to_db.query_to_create_gif()

# from slikeRadar.task import delete_slike_jpg_task, delete_slike_gif_task,import_image_to_db_task, create_gif_task

def one_minute_task():
    #provjeri da lim novih jpg slika u folderu i upisi ih u db
    import_image_to_db_task()
    #obrisi sve slike starije od predvidjenog vremena
    delete_slike_jpg_task()
    #kreiraj gif slike
    create_gif_task()
    #obrisi gif slike sem zadnje
    delete_slike_gif_task()

