"""Organiza a pasta Downloads: move arquivos antigos por tipo e apaga lixo.
Simulação por padrão; use --apply para executar."""
import argparse
import shutil
import time
from pathlib import Path

PASTAS = {
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Audios": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Instaladores": {".exe", ".msi"},
}
LIXO = {".tmp", ".crdownload", ".part"}


def livre(destino: Path) -> Path:
    """Nunca sobrescreve: acrescenta ' (1)', ' (2)'... se o nome já existe."""
    n = 1
    novo = destino
    while novo.exists():
        novo = destino.with_name(f"{destino.stem} ({n}){destino.suffix}")
        n += 1
    return novo


def limpar(pasta: Path, dias: int = 30, apply: bool = False) -> list[str]:
    limite = time.time() - dias * 86400
    log = []
    for f in sorted(pasta.iterdir()):
        if not f.is_file() or f.stat().st_mtime > limite:
            continue
        ext = f.suffix.lower()
        if ext in LIXO:
            log.append(f"apagar  {f.name}")
            if apply:
                f.unlink()
            continue
        destino = next((p for p, exts in PASTAS.items() if ext in exts), None)
        if destino:
            alvo = livre(pasta / destino / f.name)
            log.append(f"mover   {f.name} -> {destino}/{alvo.name}")
            if apply:
                alvo.parent.mkdir(exist_ok=True)
                shutil.move(f, alvo)
    return log


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=Path.home() / "Downloads")
    ap.add_argument("--days", type=int, default=30, help="idade mínima em dias")
    ap.add_argument("--apply", action="store_true", help="executa de verdade")
    a = ap.parse_args()
    linhas = limpar(a.dir, a.days, a.apply)
    print("\n".join(linhas) or "nada a fazer")
    if linhas and not a.apply:
        print("\n(simulação; rode com --apply para executar)")
