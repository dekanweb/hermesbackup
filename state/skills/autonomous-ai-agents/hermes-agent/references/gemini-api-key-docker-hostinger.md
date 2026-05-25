# Gemini API key'i Docker içinde .env'ye ekleme (Hostinger HVPS Hermes Agent)

Bu not, Hermes Agent'ı Hostinger HVPS üzerinde Docker container olarak çalıştıran ortamlarda Gemini API key'i eklemek için pratik adımları özetler.

## Durum
- Sunucuya SSH ile (çoğunlukla `root`) giriş yapılır.
- Hermes'in dosyaları host FS'te değil, container içinde olur.
- `config.yaml` genelde container içinde `/opt/data/config.yaml`.
- Secrets `.env` dosyasında tutulur: `/opt/data/.env`.

## 1) Doğru container'ı bul
```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
```
Hostinger imajı tipik olarak:
`ghcr.io/hostinger/hvps-hermes-agent:latest`

## 2) Container içine gir
```bash
docker exec -it <CONTAINER_NAME> sh
# sh yoksa:
docker exec -it <CONTAINER_NAME> bash
```

## 3) .env yolunu doğrula
```sh
ls -la /opt/data
ls -la /opt/data/.env
```

## 4) Editör yoksa (nano yoksa) iki seçenek

### Seçenek A: vi ile düzenle
```sh
vi /opt/data/.env
```
- `i` (insert)
- `GOOGLE_API_KEY=...` satırını ekle veya değiştir
- `Esc` → `:wq` → Enter

### Seçenek B: editörsüz (varsa değiştir, yoksa ekle)
Key'i chat'e yazmadan, sadece kendi SSH terminalinde kullan:
```sh
KEY='PASTE_KEY_HERE'
if grep -q '^GOOGLE_API_KEY=' /opt/data/.env; then
  sed -i "s|^GOOGLE_API_KEY=.*|GOOGLE_API_KEY=$KEY|" /opt/data/.env
else
  printf "\nGOOGLE_API_KEY=%s\n" "$KEY" >> /opt/data/.env
fi
```

## 5) Key'i göstermeden doğrula
```sh
grep -n '^GOOGLE_API_KEY=' /opt/data/.env | sed 's/=.*/=***REDACTED***/'
```

## 6) Container'dan çık ve restart et
```sh
exit
```
Host'ta:
```bash
docker restart <CONTAINER_NAME>
```

## Notlar
- Gemini için env adı olarak `GOOGLE_API_KEY` önerilir (alternatif: `GEMINI_API_KEY`).
- Değişikliklerin kesin uygulanması için container restart genelde gerekir.
- Kullanıcıdan API key'i sohbet içinde istemekten kaçın; güvenli olan kullanıcıya SSH terminalinde düzenletmektir.
