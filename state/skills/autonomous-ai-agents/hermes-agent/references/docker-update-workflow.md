# Docker Ortamında Hermes Agent Güncelleme İş Akışı

Hermes Agent bir Docker kapsayıcısı içinde çalışırken, `hermes update` komutu doğrudan çalışmayacaktır. Bunun nedeni, kapsayıcının bir git deposu olmaması ve güncelleme komutunun bir git çekme işlemi gerçekleştirmesidir.

Hermes Agent'ı bir Docker ortamında güncellemek için aşağıdaki adımları izlemelisiniz:

1.  **En Son Docker İmajını Çekin:**
    ```bash
    docker pull nousresearch/hermes-agent:latest
    ```
    Eğer belirli bir sürümü kullanıyorsanız (örneğin `:v0.14.0`), `latest` yerine o sürüm etiketini kullanmanız gerekebilir. Mevcut etiketleri [Docker Hub](https://hub.docker.com/r/nousresearch/hermes-agent/tags) adresinden kontrol edebilirsiniz.

2.  **Kapsayıcıyı Yeniden Başlatın:**
    İmajı çektikten sonra, kapsayıcınızı başlatan aracı kullanarak mevcut kapsayıcıyı durdurup yeni imajla yeniden başlatmanız gerekmektedir.

    *   `docker compose` kullanıyorsanız:
        ```bash
        docker compose up -d --force-recreate hermes-agent
        ```
    *   Tek başına `docker run` kullanıyorsanız, mevcut kapsayıcıdan çıkın ve yeni imajla `docker run` komutunu tekrar çalıştırın.

3.  **Yeni Sürümü Doğrulayın:**
    Yeniden başlatmanın ardından, aşağıdaki komutu kullanarak Hermes Agent'ın güncel sürümünü doğrulayabilirsiniz:
    ```bash
    docker run --rm nousresearch/hermes-agent:latest --version
    ```

**Önemli Notlar:**
*   Hermes'in yapılandırma ve oturum geçmişi (`$HERMES_HOME` altındaki `/opt/data` genellikle ana bilgisayardan bağlanır) imaj güncellemeleri arasında kalıcıdır; yeni bir imaj çekmek herhangi bir durumu kaybetmenize neden olmaz.
*   Bir fork kullanıyorsanız, bu deponun `Dockerfile`'ını kullanarak kendi imajınızı oluşturun ve `docker pull` adımını kendi derleme/gönderme hattınızla değiştirin.