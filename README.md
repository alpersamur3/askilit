# askilit
Bu uygulama öğrencilerin tahtayı kurcalamasını engellemek içindir.
Etap 19 da çalışır durumda.Etap 5.3’te test ettim ama python(python 4.3.2) ve pip sürümünün çok eski olmasından dolayı çalışmadı.(Çalışan bir sürüm ayarlamaya çalışıyorum ama olumlu bir sonuç çıkacak gibi gözükmüyor.5.3’te Ebaqr çalışsa bile normal qr çalışmıyor.)

Özellikleri:
-İnternet var iken ebaqr aktif olur.
-Ebaqr okutulduğunda kilit açılır.(Yalnızca öğretmen hesabı ebaqr’ı okuttuysa)
-45 dakika sonra otomatik olarak tekrar kilitlenir.
-Kilit ekranı açık iken 20 dakika boyunca giriş yapılmazsa tahta otomatik olarak kapanır.
-İnternet yok ise normal qr devreye girer okutunca şifre çıkar ve o şifre girilerek kilit açılır.
-Hiçbir şekilde kapatılamaz kapatılırsa anında tekrar açılır ve alta alınamaz.(Bir şekilde alta alınsa bile herhangi bir uygulama açılırsa kilit en üste çıkar)
-10 saniyede bir internet bağlantısı kontrol edilir ve ona göre ebaqr ya da normal qr gösterilir.
-Kilit uygulaması zaten açıksa tekrar açılamaz.
-Açılışta otomatik olarak başlatılır.
-Masaüstündeki simge ile kilit başlatılabilir.

