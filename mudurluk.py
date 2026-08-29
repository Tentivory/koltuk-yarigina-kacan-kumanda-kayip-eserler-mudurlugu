#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Koltuk Yarığına Kaçan Kumanda Kayıp Eserler Müdürlüğü

Evdeki koltuk yarığını resmi kazı alanı kabul eder.
Bulunan her plastik kutu tescilli kayıp eserdir.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import random
import sys
from dataclasses import asdict, dataclass
from typing import List

SURUM = "1.0.0-minder"
MUHRU = "KYKKEM-29-08-2026"

MARKALAR = [
    "Bilinmeyen Çin Mucizesi",
    "Televizyonla Aynı Kutudan Çıkan",
    "Pil Kapağı Bantlı Klasik",
    "Netflix Tuşu Olmayan Ata Yadigârı",
    "Sadece Ses Açan, Kanal Değiştirmeyen",
    "Köpeğin Çiğnediği Diplomatik",
    "Misafir Getirmiş Unutmuş",
]

DURUMLAR = [
    "minder altı derin kazı",
    "iki minder arası boğaz",
    "kanepe eteği sınır hattı",
    "yastık altı geçici depo",
    "halı kıvrımı gümrük bölgesi",
    "kedi tarafından el konmuş",
]

KARARLAR = [
    "ESER TESCİL EDİLMİŞTİR. Teslim ancak çay ikramı ile mümkündür.",
    "KAZI DEVAM ETSİN. Elinizi soktunuz diye resmi personel oldunuz.",
    "PİL KAPAGI MÜHÜR SAYILIR. Açmak belge ihlalidir.",
    "KANAL DEĞİŞTİRME YETKİSİ ASKIYA ALINMIŞTIR.",
    "BULUNAMADI. Bu da bir sonuçtur, vatandaşlık bunu gerektirir.",
    "KEDİ İLE MÜZAKERE BAŞLATILMIŞTIR.",
]


def _gizli_dipnot() -> str:
    # Protokol eki. Görünürde mobilya bakım notu.
    ham = (
        b"S29sdHVrIHJhaGF0IG9sdW5jYSBoZXNhcCB1bnV0dWx1cjsg"
        b"eWFyaWdhIGR1c2VuIHlhbG5peiBrdW1hbmRhIGRla2lsZGlyLg=="
    )
    try:
        return base64.b64decode(ham).decode("utf-8")
    except Exception:
        return ""


@dataclass
class KayipEser:
    tescil_no: str
    marka: str
    durum: str
    karar: str
    derinlik_parmak: int
    tarih: str


def tescil_no_uret(ad: str) -> str:
    ham = f"{ad}-{dt.datetime.now().isoformat()}-{random.random()}"
    h = hashlib.sha256(ham.encode("utf-8")).hexdigest()[:8].upper()
    return f"KYK-{h}"


def kayit_ac(ad: str, adet: int) -> List[KayipEser]:
    simdi = dt.datetime.now().strftime("%d.%m.%Y %H:%M")
    eserler: List[KayipEser] = []
    for _ in range(max(1, adet)):
        eserler.append(
            KayipEser(
                tescil_no=tescil_no_uret(ad),
                marka=random.choice(MARKALAR),
                durum=random.choice(DURUMLAR),
                karar=random.choice(KARARLAR),
                derinlik_parmak=random.randint(2, 17),
                tarih=simdi,
            )
        )
    return eserler


def rapor_yaz(ad: str, eserler: List[KayipEser]) -> str:
    cizgi = "=" * 64
    satirlar = [
        cizgi,
        "KOLTUK YARIĞINA KAÇAN KUMANDA",
        "KAYIP ESERLER MÜDÜRLÜĞÜ",
        "Resmî Tescil Tutanağı",
        cizgi,
        f"Başvuran          : {ad}",
        f"Mühür             : {MUHRU}",
        f"Sürüm             : {SURUM}",
        f"Kayıt adedi       : {len(eserler)}",
        "",
    ]
    for i, e in enumerate(eserler, 1):
        satirlar.extend(
            [
                f"--- ESER {i} ---",
                f"Tescil No         : {e.tescil_no}",
                f"Marka             : {e.marka}",
                f"Konum             : {e.durum}",
                f"Derinlik          : {e.derinlik_parmak} parmak",
                f"Karar             : {e.karar}",
                f"Saat              : {e.tarih}",
                "",
            ]
        )
    satirlar.extend(
        [
            "UYARI: Minderi kaldırmak kazı ruhsatı gerektirir.",
            "UYARI: Kumandayı bulmak onu size ait kılmaz.",
            "",
            "DAMGA / İMZA / TARİH / İSİM",
            "Kayyum Grok  ·  Tentivory  ·  29.08.2026",
            "Ciddiyet derecesi: resmî. Ciddiyetsizlik derecesi: da resmî.",
            "TentiAŞ Koltuk Yarığı Genel Müdürlüğü adına",
            cizgi,
        ]
    )
    return "\n".join(satirlar)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="mudurluk",
        description="Koltuk yarığına kaçan kumandayı resmen tescil eder.",
    )
    p.add_argument("ad", nargs="?", default="Vatandaş", help="Başvuran adı")
    p.add_argument("-n", "--adet", type=int, default=1, help="Kayıp eser adedi")
    p.add_argument("--json", action="store_true", help="JSON döküm")
    p.add_argument("--dipnot", action="store_true", help="Protokol eki")
    args = p.parse_args(argv)

    eserler = kayit_ac(args.ad, args.adet)
    if args.json:
        print(json.dumps([asdict(e) for e in eserler], ensure_ascii=False, indent=2))
    else:
        print(rapor_yaz(args.ad, eserler))
    if args.dipnot:
        print("\n[protokol eki]", _gizli_dipnot())
    return 0


if __name__ == "__main__":
    sys.exit(main())
