import os
from pathlib import Path
import imageio
from pygifsicle import optimize, gifsicle

from zipfile import ZipFile
from PIL import Image, ImageFont, ImageDraw, ImageSequence
from datetime import datetime, timedelta
from django.conf import settings
import platform
from slikeRadar.models import Slike, GifSlike
from django.core.files import File
from django.utils import timezone


# definisem klasu koja ce da odredi putanju za folder u koji stizu PGO slike iz tog foldera se slika uzima preiminuje
# u naziv YYYYMMDDHHMM datetime format, a to radi tako sto koristi timestamp kada je slika kreirana i na osnovu toga
# pravi naziv slike
class ConvertNameToDateTime:
    # definisem naziv foldera unutar kojeg se nalaze dolazece slike od pgo
    # sam folder se nalazi unutar django projekta
    pgo_folder_name = 'Queue'
    temp_folder_name = 'Temp'

    def img_path(self):
        '''
           Funkcija koja odredju path za sliku koja se nalazi u Queue folderu
           vracca listu u obliku [a,z,c]

        '''
        # definisem path za folder u koji dolaze slike od PGO, ovde je definisano da dolaze u folder Queue
        # ovaj folder se nalazi umutar django projekta
        pgo_folder_path = settings.BASE_DIR / self.pgo_folder_name

        # Provjeravamo naziv fajlova unutra foldera kako bi se mogli izmjeniti
        # ova varijabla sadrzi listu u obliku[a.txt, b.txt., c.txt]
        files_in_folder = os.listdir(pgo_folder_path)
        # odredjujem velicinu liste kako bi mogao je koristiti za for petlju  radi dobijanja apsolutne putanje za slike u folderu
        number_of_files_in_folder = len(files_in_folder)

        # Varijabla koja odredju path za sliku koja se nalazi u Queue folderu kako bi se vidjelo timestamp kada je kreirana
        path_to_file = []

        # pravim path za svaku sliku koja senalazi u folderu Queue
        for i in range(number_of_files_in_folder):
            path_to_file.append(str(os.path.join(pgo_folder_path, files_in_folder[i])))
        return path_to_file

    def rename_img_save_to_db(self):
        '''
        Metod koji mijenja naziv slike u oblik %Y-%m-%d-%H%M na osnovu nayiva slika koja
        dolazi u folder Queue, kreira desc varijablu u obliku %d-%m-%Y %H:%M""UTC", i sacuva
        sliku u model Slike
        '''
        # Definisem varijablu koja ce da sadrzi listu za path od svake slike koja dodje u folder od pgo
        paths = self.img_path()
        # definisem path za folder u koji dolaze slike od PGO, ovde je definisano da dolaze u folder Queue
        # ovaj folder se nalazi umutar django projekta
        pgo_folder_path = settings.BASE_DIR / self.pgo_folder_name
        # print(paths)
        # print(pgo_folder_path)
        # kroz petlju mijenjam naziv svake slike sa datumom i vremenom

        for i in range(len(paths)):
            # kreiram varijable koje ce da sadrze trnutni naziv imena i slike i ekstenziju slike
            d = os.path.basename(paths[i])
            # razdvajam naziv slike i ekstenziju u varijable file_name i ext respektivno
            file_name, ext = os.path.splitext(d)

            # pravim case kako bi mogo isfiltrirati fajlove koji se zavrsavaju _Base,  _CAPPI, _CMax, _HMax, _Nowcast
            # kako bi ih pravilno smjestio u db zatim obrisao iz foldera
            if '_Base' in file_name:
                pass
            if '_CAPPI' in file_name:
                pass
            if '_CMax' in file_name:
                pass
            if '_HMax' in file_name:
                pass
            if '_Nowcast' in file_name:
                pass

            # sa imena slike koji je u obliku '2023-01-10-0522_CMax' skidam naziv '_CMax' i dobijam sadrzaj varijable
            # u obliku '2023-01-10-0522'
            file_name = file_name.replace('_CMax', '')
            # Radim rename slike iz formata '2023-01-10-0522_CMax.jpg' u '2023-01-10-0522.jpg' i smijestam
            # u varijablu pod imenom new_name_img, i ova se varijabla koristi kao putanja za uploda
            # slike u models
            new_name_img = os.path.join(pgo_folder_path, file_name + ext)
            # kreiram varijablu koja je string i saderzi datum i vrijeme u formatu '10-01-2023 05:22UTC' i ista se smjesta
            # u bazu u polje desc
            date_time_desc = datetime.strptime(file_name, '%Y-%m-%d-%H%M')
            # pravim varijablu koja ce samo imati u sebi vrijeme i koristit cu je da je ubacim u db kako bi je koristio kasnije
            # za pagination
            time_create = date_time_desc.strftime("%H:%M")
            date_time_desc = date_time_desc.strftime("%d-%m-%Y %H:%M""UTC")
            # print(paths[i])
            # Mijenjam naziv slike u novi naziv
            os.rename(paths[i], new_name_img)
            # provjeravam da li je uradjen rename slike ako jeste sacuvam je u model Slike i
            # obrisem je iz foldera Queue
            if os.path.exists(new_name_img):
                print(new_name_img)
                # print(date_time_desc)
                # ispisujem natpis na slici
                self.writing_text_on_image(new_name_img, new_name_img, date_time_desc, '1')
                # kreiram obj koji pokazuje na models.py i sluzi da sacuva sliku u bazu podataka
                pic = File(open(new_name_img, 'rb'))
                b = Slike(title=file_name, descr=date_time_desc, time_create=time_create)
                b.img.save(file_name + ext, pic)
                pic.close()
                # ukoliko je slika sacuvana u db onda cu je obrisati iz foldera Queue
                if Slike.objects.filter(descr=date_time_desc).exists():
                    # obrisati sliku iz Queue foldera
                    os.remove(new_name_img)
            else:
                raise Exception("Sorry, but file {file} does not exists".format(file=new_name_img))

    # promjena naziva slike ako bi se mogla sacuavti pod odredjenim nazivom u DB
    # os.rename('from.extension.whatever','to.another.extension')
    # datestamp.strftime("%Y%m%d")

    def time_query_iteration(self):
        """definisem metod kojim cu kroy petlju napraviti queri sa svim slikama u vremenskom rayamaku od
        npr 15min. tj svaku 15min sliku ce samo iydvojiti iy baze
        """
        last_query = Slike.objects.all().order_by('-title')[:1]
        first_query = Slike.objects.all().order_by('title')[:1]
        # pravim dvije varijable u koje smijestam pocetni i krajnji datum i vrijem
        start_time_date = ''
        end_time_date = ''
        for a, b in zip(first_query, last_query):
            start_time_date = a.title
            end_time_date = b.title
        # sa start time i end time pravim datetime object tako sto uzimam string descr i pretvaram ga u datetime obj
        start_time = datetime.strptime(start_time_date, '%Y-%m-%d-%H%M')
        end_time = datetime.strptime(end_time_date, '%Y-%m-%d-%H%M')

        # pravim varijablu var_for_loop u koju cu da smijestam sve nazive title koji postoje u db
        var_for_loop = []
        # definisem kolik aje deltatime ya svaki naredni query
        from itertools import chain
        delta = timedelta(minutes=30)
        while start_time <= end_time:
            title_value = start_time.strftime("%Y-%m-%d-%H%M")
            # print(title_value)
            if Slike.objects.filter(title__icontains=title_value):
                for i in Slike.objects.filter(title__icontains=title_value):
                    # query = list(chain(Slike.objects.filter(title__icontains=title_value)))
                    var_for_loop.append(i.title)
            start_time += delta
        print(var_for_loop)
        print(Slike.objects.filter(title__in=var_for_loop))
        return Slike.objects.filter(title__in=var_for_loop)

    def query_to_create_gif(self):
        '''
        Metod kojim uzimamo zadnjih X sati slika jpg iz baye kako bi od njih napravio GIF
        privremeno jpg slike smje[ta u Temp folder od njih pravi gif sliku u temp folderu
        smije[ta gif sliku u bazu i brise sve slike iz Temp foldera

        '''
        # varijabla koja sadrzi trenutni datum i vrijeme u formatu '10-02-2023 10:15'
        start_date_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        # varijabla koja sadrzi krajnji datum i vrijeme, gdje je vrijem stavljeno yadnja 4 sata
        end_date_time = timezone.now() - timedelta(hours=4)
        end_date_time = end_date_time.strftime('%d-%m-%Y %H:%M')

        # definisem queryset koji ce da filtrira zadnjih 4 sata slika od kojih treba napraviti GIF
        # query_descr = Slike.objects.filter(descr__range=(start_date_time, end_date_time))
        # query_descr = Slike.objects.filter(descr__range=('10-01-2023 05:22', '10-01-2023 18:22'))
        query_descr = self.time_query_iteration()
        gif_title = ''
        gif_img_name = ''
        # pravim path u MEDIA folderu, kako bi isfiltrirao slike u folderu na osnovu query_descr
        for object in query_descr:
            path_to_img = os.path.join(settings.BASE_DIR, 'media', object.img.name)
            path_to_img = Path(path_to_img)
            # popunjavam varijablu gif_img_name sa object.descr kako bi mogao iskoristiti descr od
            # zadnje slike za naziv GIF slike koja ce se kreirati
            gif_img_name = object.descr
            gif_title = object.title
            # pozivam funkciju da napravim novi jpg sliku na kojoj je ispisan datum i vrijem
            # smijestam je u folder Temp
            self.writing_text_on_image(path_to_img, os.path.join(settings.BASE_DIR, self.temp_folder_name),
                                       object.descr, '2')
        self.make_gif(os.path.join(settings.BASE_DIR, self.temp_folder_name), gif_img_name)
        # print(os.path.join(os.path.join(settings.BASE_DIR, self.temp_folder_name, gif_img_name.replace(':', '')) + '.gif'))
        path_to_gif_img = os.path.join(settings.BASE_DIR, self.temp_folder_name, gif_img_name.replace(':', '')) + '.gif'
        # provjeravam da li je kreirana gif slika ukoliko je jeste onda cu je sacuvati u DB
        # i nakon toga cu da obrisem sve slike iz Temp foldera
        if os.path.exists(path_to_gif_img):
            # print("yes it exists")
            # kreiram obj koji pokazuje na models.py i sluzi da sacuva sliku u bazu podataka
            pic = File(open(path_to_gif_img, 'rb'))
            b = GifSlike(title=gif_title, descr=gif_img_name)
            b.img.save(gif_title + '.gif', pic)
            pic.close()
            # ukoliko je slika sacuvana u db onda cu je obrisati iz foldera Temp kao i sve ostale kojesu koristene
            # ya kreiranje gif slike
            if GifSlike.objects.filter(descr=gif_img_name).exists():
                for file_name in os.listdir(os.path.join(settings.BASE_DIR, self.temp_folder_name)):
                    file = os.path.join(settings.BASE_DIR, self.temp_folder_name, file_name)
                    if os.path.isfile(file):
                        # obrisati sliku iz Queue foldera
                        os.remove(file)
        else:
            raise Exception("Sorry, but file {file} does not exists".format(file=path_to_gif_img))

    def writing_text_on_image(self, img_origin_path, img_to_save_path, img_text, func_call):
        '''
        Metod koji otvara sliku u media folderu, stavlja joj natpis definisan img_text
        i sacuva tu novu sliku u folderu Temp
        '''
        my_image = Image.open(img_origin_path, mode='r')
        title_text = img_text
        image_editable = ImageDraw.Draw(my_image)
        fnt = ImageFont.truetype("static/font/FreeMonoBold.ttf", 60)
        image_editable.text((50, 15), title_text, font=fnt, fill=(237, 230, 211))
        if func_call == '1':
            my_image.save(img_to_save_path, 'JPEG')
        else:
            my_image.save(os.path.join(img_to_save_path, img_text.replace(':', '') + '.jpg'), 'JPEG')

    def make_gif(self, frame_folder, gif_img_name):
        '''
        Metod koji pravi gif sliku na osnovu slika u Temp folderu
        '''
        in_path = frame_folder
        out_filename = gif_img_name.replace(':', '')
        # print(out_filename + ".gif")
        out_path = frame_folder

        in_filenames = os.listdir(frame_folder)
        # smanjujem kvalitet svake jpg slike
        for img in in_filenames:
            self.compress_jpg(os.path.join(frame_folder, img))

        with imageio.get_writer(os.path.join(out_path, out_filename + ".gif"), mode='I', duration='0.25') as writer:
            for in_filename in in_filenames:
                print(os.path.join(in_path, in_filename))
                # image = imageio.imread(in_path + in_filename)
                image = imageio.v2.imread(os.path.join(in_path, in_filename))
                writer.append_data(image)
        if os.path.exists(os.path.join(out_path, out_filename + ".gif")):
            self.resize_gif(os.path.join(out_path, out_filename + ".gif"))
            optimize(os.path.join(out_path, out_filename + ".gif"))
            # gifsicle(os.path.join(out_path, out_filename + ".gif"))
        else:
            raise 'GIF img does not exist in folder'

    ''' prije nego sto se pocne praviti gif od jpg u Temp folderu smanjujem kvalitet slike jpg kako bi bio manji gif'''

    def compress_jpg(self, file_path):

        image = Image.open(file_path)

        image.save(file_path, "JPEG", optimize=True, quality=9)

    def resize_gif(self, gif_path):
        # Output (max) size
        size = 2048, 1024

        # Open source
        im = Image.open(gif_path)

        # Get sequence iterator
        frames = ImageSequence.Iterator(im)

        # Wrap on-the-fly thumbnail generator
        def thumbnails(frames):
            for frame in frames:
                thumbnail = frame.copy()
                thumbnail.thumbnail(size, Image.ANTIALIAS)
                yield thumbnail

        frames = thumbnails(frames)

        # Save output
        om = next(frames)  # Handle first frame separately
        om.info = im.info  # Copy sequence info
        om.save(gif_path, save_all=True, append_images=list(frames), loop=0)

    def kmz_to_zip(self):
        '''
        Metod kojim se vr[i konverzija kmz fajla u zip fajl
        Kako bi se kasnije mogao zip konvertovati u kml tj uraditi unzip
        '''
        # file_path varijabla odredju je path gdje se nalaze kmz fajlovi
        file_path = self.img_path()
        for file_name in file_path:
            # razdvajam putanju kmz fajla u base_file varijablu bez kmz ekstenzije
            # odnosno razdvaja se root filename od ekstenzije
            # u varijablu ext stavljam samo kmz varijablu
            base_file, ext = os.path.splitext(file_name)
            # provjeravam da li fajl ima kmz ekstenziju ako ima onda je preimenuj u zip
            if ext == ".kmz":
                # preimenuj ekstenziju kmz u zip
                os.rename(file_name, base_file + ".zip")

    # Metod koji vraca timestamp kada je slika kreiran ili modifikovana
    # provjerava da li je operativni sistem windos ili linux
    def creation_date(self, path_to_file):
        """
        path_to_file je varijabla koja sadrzi  za path od  slike u folderu ukojm je


        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """

        if platform.system() == 'Windows':
            # ocitava se timestamp kada je slika napravljena i stavlja se u varijablu
            time_stamp = os.path.getctime(path_to_file)
            # formatiram u oblika date time
            date_time = datetime.fromtimestamp(time_stamp)
            # vraca vrijednost u obliku yyyymmdd
            return date_time.strftime("%Y%m%d%H%M")
        else:
            stat = os.stat(path_to_file)
            try:
                time_stamp = stat.st_birthtime
                date_time = datetime.fromtimestamp(time_stamp)
                return date_time.strftime("%Y%m%d%H%M")
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                time_stamp = stat.st_mtime
                date_time = datetime.fromtimestamp(time_stamp)
                return date_time.strftime("%Y%m%d%H%M")


'''
        for file_name in file_path:
            #print(file_name)
            with ZipFile(file_name, 'r') as zipObject:
                listOfFileNames = zipObject.namelist()
                for fileName in listOfFileNames:
                    if fileName.endswith('.kml'):
                        # Extract a single file from zip
                        zipObject.extract(fileName, 'temp_py')
                        print(file_name)
                        print('All the python files are extracted')
            zipObject.close()

'''

'''
In [1]: %load_ext autoreload
In [2]: %autoreload 2
 Potrebno je instantiate a class instance prvo kao u primjeru
    from slikeRadar.ImgToDB import ConvertNameToDateTime 
     a = ConvertNameToDateTime()
     a.query_to_create_gif()
     a.img_path()
    Da se dobije time stamp u obliku liste za sve fajlove unutar foldera uradi se sledece
    a.creation_date(a.img_path())

from importlib import reload

reload(ConvertNameToDateTime)
from slikeRadar.models import Slike
 b = Slike.objects.filter(descr__range=('10-01-2023 05:22','10-01-2023 10:22'))  

import datetime
now = datetime.datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)
# 2015 5 6 8 53 40

'''
