
from django.db import models
from django.urls import reverse
#

class Slike(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/CMax/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # new
        return reverse("archiva_borja_detail", kwargs={'pk': self.pk})

class GifSlike(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/CMax/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeBase(models.Model):
    """tabela u kou smjestam Base slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/Base/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeBase(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/Base/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeNowcast(models.Model):
    """tabela u kou smjestam Nowcast slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/Nowcast/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeNowcaste(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/Nowcaste/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeHmax(models.Model):
    """tabela u kou smjestam Hmax slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/Hmax/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeHmax(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/Hmax/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeCappi(models.Model):
    """tabela u kou smjestam Cappi slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/Cappi/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeCappi(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/Cappi/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeCMaxnoCor(models.Model):
    """tabela u kou smjestam Cappi slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/CMaxnoCor/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeCMaxnoCor(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/CMaxnoCor/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeCMaxZDR(models.Model):
    """tabela u kou smjestam CMaxZDR slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/CMaxZDR/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeCMaxZDR(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/CMaxZDR/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeCMaxRainRate(models.Model):
    """tabela u kou smjestam CMaxRainRate slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/CMaxRainRate/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeCMaxRainRate(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/CMaxRainRate/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikeVIL(models.Model):
    """tabela u kou smjestam VIL slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/VIL/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikeVIL(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/VIL/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SlikePPI(models.Model):
    """tabela u kou smjestam PPI slike"""
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='images/PPI/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    #definisem polje sa vremenom kako bi ga coristio ya paggination
    time_create = models.CharField(max_length=20)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GifSlikePPI(models.Model):
    title = models.CharField(max_length=200)
    # definisemo gdje da se sacuvaju slike
    img = models.ImageField(upload_to='gifs/PPI/%Y/%m/%d/')
    #polje sa opisom description
    descr = models.CharField(max_length=200)
    time_create = models.CharField(max_length=20, null=True)
    # definisemo da se odmah upise datum/vrijeme kada je slika upisana u bazu
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title