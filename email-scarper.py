# Import library yang diperlukan
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

# Masukan URL Target
target_url = str(input('[+] Masukan URL Target : '))

# Membuat queue dari URL Target
urls = deque([target_url])

# Membuat set untuk menyimpan URL yang sudah diproses
scraped_urls = set()

# Membuat set untuk menyimpan email
emails = set()

# Menghitung jumlah URL yang akan diproses
count = 0

try:
    # Looping untuk memproses URL
    while len(urls):
        count += 1
        # custom
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        # Mengambil bagian URL dari URL Target
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        # Mengambil bagian path dari URL
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        # Menampilkan informasi sedang memproses URL
        print('[%d] Sedang Memprosess %s' % (count, url))
        try:
            # Mengirim GET request ke URL
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        # Mencari email dengan menggunakan regex
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        # Function untuk membuka semua hyperlink dari target
        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Good Byee!')

# Menampilkan email yang ditemukan
for mail in emails:
    print(mail)