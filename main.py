#!/usr/bin/env python3

import os
import requests
import time
import sys
from datetime import datetime

API_URL = "https://shopeenowatermark.com/api/extract"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "origin": "https://shopeenowatermark.com",
    "referer": "https://shopeenowatermark.com/",
    "x-requested-with": "mark.via.gp"
}

# Warna ANSI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def animate_loading(text, duration=1):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]} {text}{Colors.RESET}')
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write('\r' + ' ' * (len(text) + 2) + '\r')

def print_banner():
    banner = f"""
{Colors.BOLD}{Colors.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     ██████╗ ███████╗███╗   ██╗     ██╗ ██████╗ ████████╗            ║
║    ██╔════╝ ██╔════╝████╗  ██║     ██║██╔═══██╗╚══██╔══╝            ║
║    ██║  ███╗█████╗  ██╔██╗ ██║     ██║██║   ██║   ██║               ║
║    ██║   ██║██╔══╝  ██║╚██╗██║██   ██║██║   ██║   ██║               ║
║    ╚██████╔╝███████╗██║ ╚████║╚█████╔╝╚██████╔╝   ██║               ║
║     ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚════╝  ╚═════╝    ╚═╝               ║
║                                                                      ║
║              {Colors.WHITE}Premium Video Shopee Downloader{Colors.MAGENTA}                        ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}{Colors.WHITE}                              ©masjjoooo{Colors.RESET}
"""
    print(banner)

def print_progress_bar(current, total, width=50):
    percent = current / total
    filled = int(width * percent)
    bar = f"{Colors.GREEN}{'█' * filled}{Colors.DIM}{'░' * (width - filled)}{Colors.RESET}"
    sys.stdout.write(f'\r{Colors.CYAN}├─{Colors.RESET} Progress: {bar} {Colors.YELLOW}{percent*100:.1f}%{Colors.RESET}')
    sys.stdout.flush()

def get_streams(video_url):
    payload = {"url": video_url}
    
    animate_loading("Mengambil data video", 1.5)
    
    response = requests.post(API_URL, data=payload, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("success"):
        raise Exception("Gagal mengambil data video")
    
    return data

def download_video(url, filename):
    os.makedirs("downloads", exist_ok=True)
    filepath = os.path.join("downloads", filename)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        downloaded = 0
        
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        print_progress_bar(downloaded, total_size)
    
    print(f"\n\n{Colors.GREEN}✓ Download selesai!{Colors.RESET}")
    print(f"{Colors.CYAN}├─{Colors.RESET} Lokasi: {Colors.YELLOW}{filepath}{Colors.RESET}")
    print(f"{Colors.CYAN}├─{Colors.RESET} Ukuran: {Colors.WHITE}{total_size / (1024*1024):.2f} MB{Colors.RESET}")
    return True

def show_menu_after_download():
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}                      O P S I                         {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╠══════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[1]{Colors.RESET} Download video lagi                              {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.RED}[0]{Colors.RESET} Keluar / Hentikan script                         {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    while True:
        try:
            choice = input(f"\n{Colors.GREEN}➜{Colors.RESET} Pilihan Anda [1/0]: ").strip()
            if choice == "1":
                return True
            elif choice == "0":
                return False
            else:
                print(f"{Colors.RED}✗ Pilihan tidak valid! Masukkan 1 atau 0{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠ Dibatalkan oleh user{Colors.RESET}")
            return False

def process_download():
    clear_screen()
    print_banner()
    
    print(f"{Colors.BOLD}{Colors.WHITE}┌────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}│{Colors.RESET} {Colors.CYAN}Masukkan URL video Shopee{Colors.RESET}                                    {Colors.BOLD}{Colors.WHITE}│{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}└────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    video_url = input(f"\n{Colors.GREEN}➜{Colors.RESET} URL: ").strip()
    
    if not video_url:
        print(f"\n{Colors.RED}✗ URL tidak boleh kosong!{Colors.RESET}")
        return False
    
    try:
        print(f"\n{Colors.BLUE}⏳ Memproses video...{Colors.RESET}\n")
        data = get_streams(video_url)
        
        print(f"\n{Colors.GREEN}✓ Video ditemukan!{Colors.RESET}")
        print(f"{Colors.CYAN}├─{Colors.RESET} {Colors.BOLD}Username{Colors.RESET}: {Colors.WHITE}{data.get('username', 'Unknown')}{Colors.RESET}")
        print(f"{Colors.CYAN}├─{Colors.RESET} {Colors.BOLD}Preview{Colors.RESET}: {Colors.DIM}{data.get('preview', 'N/A')}{Colors.RESET}")
        print()
        
        streams = data.get("streams_array", [])
        
        if not streams:
            print(f"{Colors.RED}✗ Tidak ada stream ditemukan{Colors.RESET}")
            return False
        
        # Urutkan stream dengan Best Quality (V720P) di urutan pertama
        def quality_priority(q):
            if "V720P" in q.upper() or "720P" in q.upper():
                return (0, q)
            elif "V480P" in q.upper() or "480P" in q.upper():
                return (1, q)
            elif "V360P" in q.upper() or "360P" in q.upper():
                return (2, q)
            else:
                return (3, q)
        
        streams.sort(key=lambda x: quality_priority(x['quality']))
        
        print(f"{Colors.BOLD}{Colors.YELLOW}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}║{Colors.RESET}                    DAFTAR RESOLUSI                     {Colors.BOLD}{Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}╚══════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        for i, stream in enumerate(streams, start=1):
            is_best = "V720P" in stream['quality'].upper() or "720P" in stream['quality'].upper()
            best_tag = f"{Colors.GREEN}⭐ BEST QUALITY{Colors.RESET}" if is_best else ""
            
            print(f"{Colors.CYAN}[{i}]{Colors.RESET} {Colors.BOLD}{stream['quality']}{Colors.RESET} {best_tag}")
            print(f"    {Colors.DIM}├─ Codec: {stream.get('codec', 'N/A')}{Colors.RESET}")
            print(f"    {Colors.DIM}└─ Durasi: {stream.get('duration', 'N/A')} detik{Colors.RESET}")
            print()
        
        while True:
            try:
                choice = int(input(f"{Colors.GREEN}➜{Colors.RESET} Pilih nomor resolusi [1-{len(streams)}]: "))
                if 1 <= choice <= len(streams):
                    break
                else:
                    print(f"{Colors.RED}✗ Pilihan tidak valid!{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}✗ Masukkan angka yang valid!{Colors.RESET}")
        
        selected = streams[choice - 1]
        stream_url = selected["stream_url"]
        
        # Generate filename dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data.get('username', 'video')}_{selected['quality']}_{timestamp}.mp4"
        
        print(f"\n{Colors.BLUE}📥 Memulai download...{Colors.RESET}")
        print(f"{Colors.CYAN}├─{Colors.RESET} Kualitas: {Colors.WHITE}{selected['quality']}{Colors.RESET}")
        print(f"{Colors.CYAN}└─{Colors.RESET} Nama file: {Colors.DIM}{filename}{Colors.RESET}\n")
        
        download_video(stream_url, filename)
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.GREEN}║{Colors.RESET}                  {Colors.BOLD}DOWNLOAD BERHASIL!{Colors.RESET}                      {Colors.GREEN}║{Colors.RESET}")
        print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
        return True
        
    except requests.exceptions.Timeout:
        print(f"\n{Colors.RED}✗ Timeout! Cek koneksi internet Anda.{Colors.RESET}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n{Colors.RED}✗ Network error: {e}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}✗ Error: {e}{Colors.RESET}")
        return False

def main():
    while True:
        success = process_download()
        
        if success:
            # Jika download berhasil, tampilkan opsi
            if not show_menu_after_download():
                print(f"\n{Colors.YELLOW}👋 Terima kasih telah menggunakan Sopi Vidi!{Colors.RESET}")
                break
        else:
            # Jika download gagal, tetap kasih opsi untuk coba lagi
            print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.RED}║{Colors.RESET}                     DOWNLOAD GAGAL                        {Colors.RED}║{Colors.RESET}")
            print(f"{Colors.RED}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}                      O P S I                         {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}╠══════════════════════════════════════════════════════════╣{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.GREEN}[1]{Colors.RESET} Coba download lagi                              {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}  {Colors.RED}[0]{Colors.RESET} Keluar / Hentikan script                         {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
            
            while True:
                try:
                    choice = input(f"\n{Colors.GREEN}➜{Colors.RESET} Pilihan Anda [1/0]: ").strip()
                    if choice == "1":
                        break  # Lanjut ke loop berikutnya (coba lagi)
                    elif choice == "0":
                        print(f"\n{Colors.YELLOW}👋 Terima kasih telah menggunakan Sopi Vidi!{Colors.RESET}")
                        return
                    else:
                        print(f"{Colors.RED}✗ Pilihan tidak valid! Masukkan 1 atau 0{Colors.RESET}")
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}⚠ Dibatalkan oleh user{Colors.RESET}")
                    return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠ Script dihentikan oleh user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}✗ Terjadi kesalahan fatal: {e}{Colors.RESET}")
