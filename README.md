# ASKilit
Bu uygulama öğrencilerin tahtayı kurcalamasını engellemek içindir.

Etap 19 da çalışır durumda.Etap 5.3’te test ettim ama python(python 3.4.2) ve pip sürümünün çok eski olmasından dolayı çalışmadı.(Çalışan bir sürüm ayarlamaya çalışıyorum ama olumlu bir sonuç çıkacak gibi gözükmüyor.5.3’te Ebaqr çalışsa bile normal qr çalışmıyor.)

# ASkilit-3.0 Yayınlandı :)
-Görüntü iyileştirmeleri

-Kod düzenlenmesi,yorum satırları ve pep-8 kurallarına uyum.

# İşte Tüm Özellikleri:
-İnternet var iken ebaqr aktif olur.

-Öğretmen hesabı ile Ebaqr okutulduğunda kilit açılır.

-45 dakika sonra otomatik olarak tekrar kilitlenir.(Destekleyen cihazlar için 25 dakika boyunca dokunma olmaz ise otomatik kilitleme sistemi)

-Kilit ekranı açık iken 20 dakika boyunca giriş yapılmazsa tahta otomatik olarak kapanır.

-İnternet yok ise normal qr devreye girer okutunca şifre çıkar ve o şifre girilerek kilit açılır.

-Eğer kilit normal qr ile açıldıysa 30 saniyede bir internet kontrolü başlatılır ve internet geldiğinde kilit tekrar devreye girer(ebaqr gösterilir)(Öğrenciler internet kablosunu çekip tahtayı açmayı denerse diye bu sistem eklendi.)

-Hiçbir şekilde kapatılamaz kapatılırsa anında tekrar açılır ve alta alınamaz.(Bir şekilde alta alınsa bile herhangi bir uygulama açılırsa kilit en üste çıkar)

-1 dakikada bir internet bağlantısı kontrol edilir ve ona göre ebaqr ya da normal qr gösterilir.

-Kilit uygulaması zaten açıksa tekrar açılamaz.

-Açılışta otomatik olarak başlatılır.

-Masaüstündeki simge ile kilit başlatılabilir.

-Bir şekilde pencere boyutu küçültülürse otomatik olarak uygulama yeniden başlatılır ve tam ekran olur.

-v2.0 sürümü ile tahta açılışta EbaQr yükleniyor yazısı göstererek 20 saniyelik bir bekleme yapar.Böylece interneti geç algılayan tahtalarda internet bu süre içinde algılanır.

-v2.0 sürümü ile internet gidip geldiğinde uygulama kapanıp açılmaz direkt olarak normal qr ve ebaqr arasında geçiş yapılır.

-v2.0 sürümü ile kararlılık arttırıldı ve iyileştirmeler,hata gidermeler yapıldı.

# Kurulum:

-pip3 kurulu değil ise(etaplarda genelde kurulu olmaz.) pkexec apt install python3-pip komutunu uçbirimde çalıştırınız.

-Debian uzantılı paket dosyasını kurulumu başlatınız.

-Cihazı yeniden başlatınız.

-Ekrana gelen komutu uçbirimde çalıştırınız.(Örnek resimdeki kod çalışmaz uygulama cihaza göre kod oluşturuyor.Lütfen uygulamadan aldığınız kodu kullanın)(Opsiyonel)
-25 dakika boyunca dokunma olmaz ise otomatik kilit sistemini aktif etmek için uygulamayı ilk açtığınızda gözüken komutu uçbirimde çalıştırınız.(Komut her tahtaya özel olarak belirlenmektedir.)

<img src="https://i.hizliresim.com/g64z8fc.png" alt="kod" height:150px>
-Tahtayı yeniden başlatınız ve kilit sistemi hazır.

# Todo:

-İnternet yokken ki gelen qr koda daha iyi bir çözüm bulmak(Öğrencilerin açamaması için)(geçici olarak daha iyi bir çözüm bulundu.)

# Görseller:

<img src="https://i.hizliresim.com/mfhkzd8.png" alt="Landing page" height="270px">
<img src="https://i.hizliresim.com/d90jzca.png" alt="Landing page" height="270px">
<img src="https://i.hizliresim.com/oq1xhpf.png" alt="Landing page" height="270px">
<img src="https://i.hizliresim.com/dy1n9eu.png" alt="Landing page" height="270px">

