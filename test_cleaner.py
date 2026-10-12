import os
import time

from cleaner import limpar


def _arq(p, antigo=True):
    p.write_text("x")
    if antigo:
        t = time.time() - 60 * 86400
        os.utime(p, (t, t))


def test_limpar(tmp_path):
    _arq(tmp_path / "a.pdf")
    _arq(tmp_path / "novo.pdf", antigo=False)
    _arq(tmp_path / "lixo.crdownload")
    _arq(tmp_path / "foto.png")
    (tmp_path / "Imagens").mkdir()
    _arq(tmp_path / "Imagens" / "foto.png")

    assert len(limpar(tmp_path)) == 3  # simulação não mexe em nada
    assert (tmp_path / "a.pdf").exists()

    limpar(tmp_path, apply=True)
    assert (tmp_path / "Documentos" / "a.pdf").exists()
    assert (tmp_path / "novo.pdf").exists()
    assert not (tmp_path / "lixo.crdownload").exists()
    assert (tmp_path / "Imagens" / "foto (1).png").exists()  # sem sobrescrever
