import csv

from models.venue import Venue


# def is_duplicate_venue(venue_name: str, seen_names: set) -> bool:
#     return venue_name in seen_names

# def is_duplicate_venue(venue: dict, seen_ids: set) -> bool:
#             # Gunakan 'image_url' sebagai pengidentifikasi unik.
#             # Jika 'image_url' juga tidak selalu unik, Anda harus mencari ID lain di HTML.
#             # Atau gabungkan beberapa kunci seperti 'brand-model-year'
#             unique_id = venue.get("listing_id")
            
#             # Jika 'image_url' mungkin kosong atau tidak cukup unik,
#             # Anda bisa menggunakan fallback ke kombinasi title atau brand-model
#             if not unique_id:
#                 unique_id = venue.get("title") # Fallback ke title
#             if not unique_id:
#                 unique_id = f"{venue.get('brand', '')}-{venue.get('model', '')}-{venue.get('year', '')}"

#             if unique_id in seen_ids:
#                 return True
#             seen_ids.add(unique_id)
#             return False

def is_duplicate_venue(venue: dict, seen_ids: set) -> bool:
    # Prioritas 1: Gunakan 'listing_id' yang baru diekstrak dari data-list-no
    unique_id = venue.get("listing_id")

    # Prioritas 2: Jika 'listing_id' tidak ada atau kosong, coba ekstrak dari 'image_url'
    # Pastikan ini hanya dieksekusi jika 'unique_id' dari listing_id tidak ditemukan
    if not unique_id and venue.get("image_url") and "oto.com/2021/images/1x1.png" not in venue["image_url"]:
        image_url_parts = venue["image_url"].split('/')
        if image_url_parts and '.' in image_url_parts[-1]:
            unique_id = image_url_parts[-1].split('.')[0]
        # Jika image_url tidak memiliki ID unik yang jelas, pastikan unique_id tetap None
        if not unique_id: # Pastikan unique_id adalah string jika diekstrak
            unique_id = None # Set kembali ke None jika ekstraksi dari URL gambar tidak berhasil

    # Prioritas 3: Jika tidak ada ID unik yang jelas, buat kombinasi dari beberapa field
    if not unique_id:
        title_part = venue.get("title", "")
        brand_part = venue.get("brand", "")
        model_part = venue.get("model", "")
        year_part = str(venue.get("year", ""))
        km_part = str(venue.get("km", ""))
        
        # Gabungkan beberapa field untuk menciptakan ID komposit yang lebih unik
        unique_id = f"{title_part}|{brand_part}|{model_part}|{year_part}|{km_part}"
        unique_id = unique_id.replace(" ", "").lower() # Normalisasi untuk konsistensi

    # Jika unique_id masih kosong setelah semua upaya, ini adalah masalah,
    # gunakan representasi string dari seluruh venue sebagai fallback terakhir.
    if not unique_id:
        print(f"Warning: Could not determine strong unique ID for venue: {venue.get('title', 'N/A')}. Using full venue string as ID.")
        unique_id = str(venue)

    # Periksa duplikasi dan tambahkan ke set jika unik
    if unique_id in seen_ids:
        return True # Venue adalah duplikat
    else:
        seen_ids.add(unique_id) # Tambahkan ID unik ke set
        return False # Venue bukan duplikat


def is_complete_venue(venue: dict, required_keys: list) -> bool:
    return all(key in venue for key in required_keys)


def save_venues_to_csv(venues: list, filename: str):
    if not venues:
        print("No venues to save.")
        return

    # Use field names from the Venue model
    fieldnames = Venue.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} venues to '{filename}'.")
