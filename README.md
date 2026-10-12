# downloads-cleaner

Organiza a pasta Downloads: move arquivos com mais de 30 dias para subpastas por tipo (Documentos, Imagens, Videos, Audios, Compactados, Instaladores) e apaga lixo (`.tmp`, `.crdownload`, `.part`). Só Python 3, sem dependências.

```
python cleaner.py                 # simulação: só mostra o que faria
python cleaner.py --apply         # executa
python cleaner.py --days 7 --dir D:\Outra
```

Nunca sobrescreve: nomes repetidos viram `arquivo (1).pdf`.

## Rodar em segundo plano (Windows)

```
schtasks /create /tn "downloads-cleaner" /sc daily /st 12:00 /tr "python C:\caminho\cleaner.py --apply"
```

## Teste

```
python -m pytest test_cleaner.py
```
