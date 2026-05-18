"""
Geolocalização de Imagens com EXIF + IA (Picarta)
Estudo integração bibliotecas picarta e exiftags
Nota-se que a a biblioteca API Picarta é paga
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os


# ==================== FUNÇÕES EXIF ====================
def dms_to_decimal(degrees, minutes, seconds, ref):
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal


def extrair_exif_completo(imagem_path):
    try:
        img = Image.open(imagem_path)
        exif_raw = img._getexif()

        if not exif_raw:
            return {}, img.size

        exif = {}
        gps_info = {}

        for tag_id, value in exif_raw.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif[tag_name] = value

            if tag_name == "GPSInfo":
                for gps_tag_id, gps_value in value.items():
                    gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_info[gps_tag_name] = gps_value

        if gps_info:
            exif["GPSInfo"] = gps_info

        return exif, img.size
    except Exception as e:
        print(f"Erro ao ler EXIF: {e}")
        return {}, None


def obter_coordenadas_gps(exif):
    if "GPSInfo" not in exif:
        return None, None
    gps = exif["GPSInfo"]
    try:
        lat = gps.get(2)
        lat_ref = gps.get(1)
        lon = gps.get(4)
        lon_ref = gps.get(3)

        if lat and lon and lat_ref and lon_ref:
            lat_dec = dms_to_decimal(lat[0], lat[1], lat[2], lat_ref)
            lon_dec = dms_to_decimal(lon[0], lon[1], lon[2], lon_ref)
            return lat_dec, lon_dec
    except:
        pass
    return None, None


def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="geolocalizacao_python_estudos")
    for _ in range(3):
        try:
            location = geolocator.reverse((lat, lon), language="pt-br", timeout=10)
            return location.address if location else "Endereço não encontrado"
        except GeocoderTimedOut:
            time.sleep(1)
        except:
            return "Erro ao buscar endereço"
    return "Timeout"


# ==================== PICARTA (IA) ====================
def geolocalizar_com_picarta(imagem_path):
    try:
        from picarta import Picarta
        import json

        TOKEN = "SEU_TOKEN"  # ← Cole seu token real aqui!

        if "SEU_TOKEN" in TOKEN or len(TOKEN) < 20:
            print("❌ Token do Picarta não configurado!")
            return None

        localizer = Picarta(TOKEN)
        result = localizer.localize(img_path=imagem_path, top_k=3)

        # Tratamento robusto do retorno
        if isinstance(result, str):
            result = json.loads(result)

        if not isinstance(result, dict):
            print("❌ Resultado inesperado do Picarta")
            return None

        print("\n🌍 === PICARTA AI - 3 LOCAIS POSSÍVEIS ===")
        predictions = result.get("topk_predictions_dict", {})

        for rank, pred in predictions.items():
            addr = pred.get("address", {})
            gps = pred.get("gps", [0, 0])
            conf = pred.get("confidence", 0)

            city = addr.get('city', '---')
            province = addr.get('province', '')
            country = addr.get('country', '')

            lat, lon = gps[0], gps[1]

            # Gera link do Google Maps
            maps_link = f"https://www.google.com/maps?q={lat:.6f},{lon:.6f}"

            print(f"{rank}. {city}, {province} - {country}")
            print(f"   📍 GPS: {lat:.6f}, {lon:.6f}")
            print(f"   🔗 Google Maps: {maps_link}")
            print(f"   Confiança: {conf:.1%}\n")

            # Opcional: abre automaticamente no navegador 
            # import webbrowser
            # webbrowser.open(maps_link)

        return result

    except Exception as e:
        print(f"❌ Erro no Picarta: {e}")
        import traceback
        traceback.print_exc()
    return None

# ==================== INTERFACE PRINCIPAL ====================
def selecionar_e_analisar():
    # Janela de seleção de arquivo
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(
        title="Selecione uma foto para analisar",
        filetypes=[
            ("Imagens", "*.jpg *.jpeg *.png *.heic *.tiff"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if not file_path:
        print("Nenhuma imagem selecionada.")
        return

    print(f"\n📸 Imagem selecionada: {os.path.basename(file_path)}")
    print("=" * 70)

    # 1. Extrair EXIF
    exif, tamanho = extrair_exif_completo(file_path)

    print("📋 METADADOS EXIF:")
    for chave, valor in list(exif.items())[:15]:  # limita para não poluir
        if chave != "GPSInfo":
            print(f"   • {chave}: {valor}")

    lat, lon = obter_coordenadas_gps(exif)
    if lat and lon:
        print(f"\n🌍 GPS embutido: {lat:.6f}, {lon:.6f}")
        endereco = reverse_geocode(lat, lon)
        print(f"   Endereço: {endereco}")

    # 2. Geolocalização por IA
    geolocalizar_com_picarta(file_path)

    print("\n✅ Análise finalizada!")
    messagebox.showinfo("Pronto!", f"Análise da imagem concluída!\n\n{os.path.basename(file_path)}")


# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    print("🖼️  Sistema de Geolocalização de Imagens")
    print("Clique em OK para selecionar a foto...\n")

    selecionar_e_analisar()