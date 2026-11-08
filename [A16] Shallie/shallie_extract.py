#!/usr/bin/env python3

import argparse
import csv
import html.entities
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

LANGUAGE_FOLDERS = {
    "ja": "Saves",
    "en": "Saves_EN",
    "sc": "Saves_SC",
    "tc": "Saves_TC",
}

_CODEC_CANDIDATES = {
    "ja": ["utf-8-sig", "cp932", "shift_jis"],
    "en": ["utf-8-sig", "cp1252"],
    "sc": ["utf-8-sig", "gbk", "gb18030"],
    "tc": ["utf-8-sig", "cp950", "big5"],
}

_XML_DECL_RE = re.compile(r'^\s*<\?xml[^>]*\?>\s*', re.IGNORECASE)
_NAMED_ENTITY_RE = re.compile(r"&([A-Za-z][A-Za-z0-9]+);")
_XML_ENTITIES = {"amp", "apos", "gt", "lt", "quot"}

SCRIPT_DIR = Path(__file__).resolve().parent

DATASETS = {
    "itemData": {
        "xml_relative_path": Path("item") / "itemData.xml",
        "enum_path": SCRIPT_DIR / "enums" / "enums_items.txt",
        "tag": "itemData",
        "name_attr": "ItemName",
        "remove_keys": {"ImageNo", "AbcOrder"},
    },
    "item_status": {
        "xml_relative_path": Path("item") / "item_status.xml",
        "tag": "item_status",
        "remove_keys": {},
    },
    "item_book": {
        "xml_relative_path": Path("item") / "item_book.xml",
        "tag": "item_book",
        "name_attr": "BookName",
        "remove_keys": {},
    },
    "item_analyze": {
        "xml_relative_path": Path("item") / "item_analyze.xml",
        "tag": "item_analyze",
        "name_attr": "item_analyze",
        "remove_keys": {},
    },
    "item_effect": {
        "xml_relative_path": Path("item") / "item_effect.xml",
        "tag": "item_effect",
        "name_attr": "ItemEffectName",
        "remove_keys": {},
    },
    "item_potential": {
        "xml_relative_path": Path("item") / "item_potential.xml",
        "enum_path": SCRIPT_DIR / "enums" / "enums_properties.txt",
        "tag": "item_potential",
        "name_attr": "PotName",
        "remove_keys": {},
    },
    "ShopData": {
        "xml_relative_path": Path("shop") / "ShopData.xml",
        "tag": "ShopData",
        "remove_keys": {"itemName"},
    },
}


def _decode_bytes(raw: bytes, xml_path: Path, lang: str) -> str:
    candidates = _CODEC_CANDIDATES.get(lang, ["utf-8-sig"])
    for codec in candidates:
        try:
            return raw.decode(codec)
        except UnicodeDecodeError:
            continue

    try:
        raw.decode(candidates[0])
    except UnicodeDecodeError as exc:
        context = raw[max(0, exc.start - 20): exc.start + 20]
        print(
            f"[warn] {xml_path}: none of {candidates} decoded cleanly. "
            f"First failure at byte {exc.start} "
            f"(0x{raw[exc.start]:02x}). Context: {context!r}",
            file=sys.stderr,
        )
    print(f"[warn] {xml_path}: falling back to utf-8 with replacement characters.", file=sys.stderr)
    return raw.decode("utf-8", errors="replace")


def _read_xml_text(xml_path: Path, lang: str) -> str:
    text = _decode_bytes(xml_path.read_bytes(), xml_path, lang)
    text = _XML_DECL_RE.sub("", text, count=1)

    def replace_html_entity(match: re.Match) -> str:
        name = match.group(1)
        if name in _XML_ENTITIES:
            return match.group(0)
        return html.entities.html5.get(name + ";", match.group(0))

    return _NAMED_ENTITY_RE.sub(replace_html_entity, text)


def _coerce(value: str):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _load_enum_list(enum_path: Path) -> list[str]:
    with enum_path.open("r", encoding="utf-8-sig") as file:
        return [line.strip() for line in file if line.strip()]


def _parse_language_file(
    xml_path: Path, lang: str, tag: str, name_attr: str | None
) -> list[dict]:
    root = ET.fromstring(_read_xml_text(xml_path, lang))
    elements = root.findall(f".//{tag}")
    if not elements and root.tag == tag:
        elements = [root]

    records = []
    for element in elements:
        attrs = dict(element.attrib)
        name = attrs.pop(name_attr, None) if name_attr is not None else None
        records.append({"_name": name, "_attrs": attrs})
    return records


def build_dataset(data_root: Path, dataset_key: str) -> dict:
    config = DATASETS[dataset_key]
    remove_keys = config.get("remove_keys", set())
    per_lang_records: dict[str, list[dict]] = {}

    for lang, folder in LANGUAGE_FOLDERS.items():
        xml_path = data_root / folder / config["xml_relative_path"]
        if not xml_path.is_file():
            print(f"Warning: missing file for '{lang}': {xml_path}", file=sys.stderr)
            continue
        per_lang_records[lang] = _parse_language_file(
            xml_path, lang, config["tag"], config.get("name_attr")
        )

    if not per_lang_records:
        print(f"Warning: no language files found for '{dataset_key}'.", file=sys.stderr)
        return {}

    lengths = {lang: len(records) for lang, records in per_lang_records.items()}
    if len(set(lengths.values())) > 1:
        canonical_count = lengths.get("ja", max(lengths.values()))
        print(
            f"[warn] {dataset_key}: language files have mismatched entry counts: {lengths}. "
            f"Using {canonical_count} records from Japanese when available; "
            "check for missing/extra rows.",
            file=sys.stderr,
        )
    merge_len = lengths.get("ja", max(lengths.values()))

    merged = []
    for index in range(merge_len):
        entry = {}
        for lang, records in per_lang_records.items():
            if index >= len(records):
                continue
            record = records[index]
            if config.get("name_attr") is not None and record["_name"]:
                entry[f"name_{lang}"] = record["_name"]
            for key, value in record["_attrs"].items():
                if key in remove_keys:
                    continue
                entry.setdefault(key, _coerce(value))
        merged.append(entry)

    enum_path = config.get("enum_path")
    if enum_path is None:
        return dict(enumerate(merged))
    if not enum_path.is_file():
        print(
            f"Warning: enum file not found: {enum_path}. Returning a plain list instead.",
            file=sys.stderr,
        )
        return dict(enumerate(merged))

    enum_list = _load_enum_list(enum_path)
    if len(enum_list) != len(merged):
        print(
            f"[warn] {dataset_key}: enum count ({len(enum_list)}) does not match "
            f"merged entry count ({len(merged)}). Zipping to the shorter of the two; "
            f"check enums/{enum_path.name} against the XML for a mismatch.",
            file=sys.stderr,
        )

    final = {}
    for index, entry in enumerate(merged):
        if index >= len(enum_list):
            final[index] = entry
            continue

        enum_name = enum_list[index]
        entry["enum"] = enum_name
        key = enum_name
        if key in final:
            print(f"[warn] {dataset_key}: duplicate enum {enum_name!r} at record {index}.", file=sys.stderr)
            key = index
        final[key] = entry
    return final


def write_tsv(dataset: dict, out_path: Path) -> None:
    preferred = ["enum", "name_ja", "name_en", "name_sc", "name_tc"]
    available = {key for entry in dataset.values() for key in entry}
    fieldnames = [key for key in preferred if key in available]
    seen = set(fieldnames)
    for entry in dataset.values():
        for key in entry:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(dataset.values())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build TSV files from the four language copies of Shallie XML files."
    )
    parser.add_argument("data_root", type=Path, help="Root directory containing the Saves* folders")
    args = parser.parse_args()

    output_dir = SCRIPT_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    data = {
        dataset_key: build_dataset(args.data_root, dataset_key)
        for dataset_key in DATASETS
    }

    item_entries = list(data["itemData"].values())
    status_entries = list(data["item_status"].values())
    if len(item_entries) != len(status_entries):
        print(
            f"[warn] itemData and item_status have different entry counts "
            f"({len(item_entries)} and {len(status_entries)}); merging by position "
            "up to the shorter dataset.",
            file=sys.stderr,
        )
    for item_entry, status_entry in zip(item_entries, status_entries):
        for key, value in status_entry.items():
            item_entry.setdefault(key, value)

    for dataset_key, dataset in data.items():
        if dataset_key == "item_status":
            continue
        write_tsv(dataset, output_dir / f"{dataset_key}.tsv")


if __name__ == "__main__":
    main()