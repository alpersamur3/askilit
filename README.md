# ASKilit
Bu uygulama öğrencilerin tahtayı kurcalamasını engellemek içindir.

Etap 19 da çalışır durumda.Etap 5.3’te test ettim ama python(python 4.3.2) ve pip sürümünün çok eski olmasından dolayı çalışmadı.(Çalışan bir sürüm ayarlamaya çalışıyorum ama olumlu bir sonuç çıkacak gibi gözükmüyor.5.3’te Ebaqr çalışsa bile normal qr çalışmıyor.)

# Özellikleri:
-İnternet var iken ebaqr aktif olur.

-Öğretmen hesabı ile Ebaqr okutulduğunda kilit açılır.

-45 dakika sonra otomatik olarak tekrar kilitlenir.(Güncelleme ile gelen özelliği okuyunuz)

-Kilit ekranı açık iken 20 dakika boyunca giriş yapılmazsa tahta otomatik olarak kapanır.

-İnternet yok ise normal qr devreye girer okutunca şifre çıkar ve o şifre girilerek kilit açılır.(Yeni güncelleme ile gelen özelliği inceleyiniz)

-Hiçbir şekilde kapatılamaz kapatılırsa anında tekrar açılır ve alta alınamaz.(Bir şekilde alta alınsa bile herhangi bir uygulama açılırsa kilit en üste çıkar)

-1 dakikada(13.01.2024) bir internet bağlantısı kontrol edilir ve ona göre ebaqr ya da normal qr gösterilir.

-Kilit uygulaması zaten açıksa tekrar açılamaz.

-Açılışta otomatik olarak başlatılır.

-Masaüstündeki simge ile kilit başlatılabilir.

-13.01.2024
-
-Destekleyen cihazlar için 25 dakika boyunca dokunma olmaz ise otomatik kilit sistemi eklendi.(Desteklemiyor ise 45 dakikada bir kilit devreye girer)
-25 dakika boyunca dokunma olmaz ise otomatik kilit sistemini aktif etmek için uygulamayı ilk açtığınızda gözüken komutu uçbirimde çalıştırınız.(Komut her tahtaya özel olarak belirlenmektedir.)
-Bir şekilde pencere boyutu küçültülürse otomatik olarak uygulama yeniden başlatılır ve tam ekran olur.
-Eğer kilit normal qr ile açıldıysa 30 saniyede bir internet kontrolü başlatılır ve internet geldiğinde kilit tekrar devreye girer(ebaqr gösterilir)(Öğrenciler internet kablosunu çekip tahtayı açmayı denerse diye bu sistem eklendi.)
-Oturumu kapat tuşu kaldırıldı.
# Todo:

-İnternet yokken ki gelen qr koda daha iyi bir çözüm bulmak(Öğrencilerin açamaması için)(geçici olarak daha iyi bir çözüm bulundu.)

# Görseller:

<img src="https://i.hizliresim.com/c9os21v.png" alt="Landing page" height="270px">
<img src="https://i.hizliresim.com/1m8qwj8.png" alt="Landing page" height="270px">
<img src="https://i.hizliresim.com/dy1n9eu.png" alt="Landing page" height="270px">

