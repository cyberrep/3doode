#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GENERATE_USB - PREPARA O CARTAO/PENDRIVE PARA O BOOT 3DO ODE / PREPARES THE CARD FOR THE 3DO ODE BOOT

1. Procura as ISOs/CUEs do cartao (raiz e subpastas).
2. Para cada jogo, pega a capa e a tela do jogo:
     - primeiro em cover/ e screenshot/ (as suas imagens tem prioridade)
     - se nao tiver, BAIXA do libretro-thumbnails (so dos jogos que voce tem)
       e guarda em cover/ e screenshot/ para a proxima vez funcionar sem internet
3. Pega o texto em txt/Jogo.txt, ou no gamelist.txt (um bloco por jogo);
   se tiver um gamelist.xml (Batocera/EmulationStation/Skyscraper) ele so
   completa os campos que faltarem
4. Grava as capas e as telas em CEL (formato do boot 3DO ODE), SEMPRE na raiz do cartao:
     covers/small e covers/large (56x78 e 100x140) e screenshots/medium e screenshots/large (120x90 e 304x228),
     com o preparo "TEXTO" (luz linear, nitidez, pontilhado so fora das letras).
   NAO apaga suas pastas cover/ e screenshot/ (padrao seguro).

uso / usage:
    python generate_usb.py E:\            gera / builds
    python generate_usb.py E:\ --teste    so mostra o que faria / dry run
    python generate_usb.py E:\ --forcar   refaz todos / rebuilds all
    python generate_usb.py E:\ --somente-lista gera SO os textos (3dogamesdetails.ode), SEM capas/telas/videos / texts only
    python generate_usb.py E:\ --pular-gamelist  NAO gera o 3dogamesdetails.ode (mantem o atual) / skip the gamelist file
    python generate_usb.py E:\ --video-faltantes gera .cvd SO dos que faltam / only missing videos
    python generate_usb.py E:\ --refazer-capas | --refazer-telas | --refazer-videos   refaz todos daquele tipo
    python generate_usb.py E:\ --pular-capas | --capas-faltantes   nao gera capas | so as que faltam no cartao
    python generate_usb.py E:\ --pular-telas | --telas-faltantes   nao gera telas | so as que faltam no cartao
    python generate_usb.py E:\ --tamanho small    video: mini 80x60 | box 128x96 | small 160x120 (padrao) | medium 240x180 | large 320x240
    python generate_usb.py E:\ --video-fps 15 --video-seg 20 --video-q 4   quadros/s, segundos, qualidade (1 melhor ... 31 menor)
    Os videos de previa saem em Cinepak (videos/<jogo>.cvd), SEMPRE convertidos dos videos-fonte da pasta
        videos/ (mp4/avi/mkv...).
    python generate_usb.py E:\ --organizar    move os jogos da raiz p/ pastas A..Z (lancamento rapido) / letter folders
    python generate_usb.py E:\ --offline  nao baixa nada / no downloads
    python generate_usb.py E:\ --relatorio gera o cover.txt / writes the cover.txt report
    python generate_usb.py E:\ --iso2bin  converte .iso em .bin/.cue estilo Redump (precisa numpy) / iso -> bin/cue
    python generate_usb.py E:\ --idioma en  usa gamelist.en.txt nos textos / text language (pt|en|es)
    python generate_usb.py E:\ --copiar-boot  copia o boot.iso (o menu) p/ a raiz do cartao / copy boot.iso to the card root
    python generate_usb.py E:\ --capa-preparo suave preparo: texto (padrao) | nitida | suave | sempontos | corfiel
                                                (mudou o preparo -> refaz todas as capas sozinho)
    python generate_usb.py               SEM opcoes = ASSISTENTE passo a passo / no options = interactive wizard
requer / needs:  pip install pillow   (e numpy p/ --iso2bin)
Nunca apaga nada seu (sem opcao de limpar). / never deletes your files
"""
import os, re, sys, json, struct, zlib, base64, difflib, unicodedata, shutil, urllib.request, urllib.parse
import sys as _sys_out
# Cada linha aparece na hora (no .bat, na janela e quando a saida vai para arquivo).
try:
    _sys_out.stdout.reconfigure(line_buffering=True)
    _sys_out.stderr.reconfigure(line_buffering=True)
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# FFmpeg: procura tambem na PASTA DESTE SCRIPT e na pasta atual. O Python 3.12+ parou de olhar a pasta
# atual no shutil.which, entao bastava por ffmpeg.exe ao lado e mesmo assim nao achava. Aqui garantimos
# que ambas entram no PATH do processo. / also look next to the script and in cwd for ffmpeg.exe
for _d in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
    if _d and _d not in os.environ.get('PATH', '').split(os.pathsep):
        os.environ['PATH'] = _d + os.pathsep + os.environ.get('PATH', '')
# ====== MODULOS EMBUTIDOS (arquivo unico) ======
# converte_video / iso2bincue / midia_download viram modulos em memoria,
# para o generate_usb rodar SOZINHO, sem .py ao lado. A logica abaixo nao muda.
import types as _types
_HELPER_SRC = {
  'converte_video': r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
converte_video - videos de previa do boot 3DO ODE em Cinepak (.cvd).

O 3DO nao decodifica mp4/h264: o video e convertido antes, pelo ffmpeg, para
Cinepak (o codec dos videos do proprio 3DO) no tamanho pedido, e guardado num
arquivo simples (.cvd) que o boot le do comeco ao fim: cabecalho, tabela com
o tamanho de cada quadro e os quadros.
"""
import os, sys, struct, subprocess, shutil

# Tamanho do video (o generate_usb troca conforme --tamanho).
VID_W, VID_H = 160, 120


def ffmpeg_ok():
    return shutil.which('ffmpeg') is not None


# ====== CINEPAK (videos de previa .cvd) ======
# Qualidade do Cinepak do ffmpeg (-q:v): 1 = melhor e maior ... 31 = pior e menor.
CVD_Q = 4


def cinepak_ok():
    """True se o ffmpeg deste PC tem o codificador Cinepak."""
    try:
        out = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return b'cinepak' in out.stdout
    except Exception:
        return False


def _avi_frames(data):
    """Tira de um AVI os quadros de video (pedacos '00dc') e diz quais sao quadros-chave (pelo idx1).
    Devolve a lista [(bytes do quadro, chave)]."""
    frames = []
    keys = []
    pos = 12
    movi = None

    def walk(start, end):
        nonlocal movi
        p = start
        while p + 8 <= end:
            cid = data[p:p + 4]
            size = struct.unpack_from('<I', data, p + 4)[0]
            body = p + 8
            if cid in (b'RIFF', b'LIST'):
                kind = data[body:body + 4]
                if kind == b'movi':
                    movi = body
                walk(body + 4, min(end, body + size))
            elif cid[2:4] in (b'dc', b'db') and cid[:2].isdigit():
                if size:
                    frames.append((body - 4 - (movi or 0), data[body:body + size]))
            elif cid == b'idx1':
                for k in range(0, size, 16):
                    c, fl, off, sz = struct.unpack_from('<4sIII', data, body + k)
                    if c[2:4] in (b'dc', b'db') and sz:
                        keys.append(bool(fl & 0x10))
            p = body + size + (size & 1)

    walk(pos, len(data))
    out = []
    for i, (off, fr) in enumerate(frames):
        # sem idx1: o bit 0 do 1o byte do quadro Cinepak = 0 quer dizer quadro-chave
        key = keys[i] if i < len(keys) else not (fr[0] & 1)
        out.append((fr, key))
    return out


def encode_cinepak(path, w, h, fps, seg, inicio, q=None):
    """Converte o video-fonte em Cinepak w x h (multiplos de 4) com o ffmpeg e devolve [(quadro, chave)].
    Mantem a proporcao do video (faixas pretas se nao for 4:3). Um quadro-chave a cada 2 segundos."""
    import tempfile
    q = CVD_Q if q is None else q
    # Faixas por quadro: 1 no 160x120 (arquivo ~35% menor, quase a mesma imagem), 2 no 240x180, 3 no 320x240.
    # Numero fixo = bem mais rapido de converter. / strips per frame by size (fixed count = much faster)
    _strips = 1 if w * h <= 160 * 120 else (2 if w * h <= 240 * 180 else 3)
    tmp = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    tmp.close()
    try:
        cmd = ['ffmpeg', '-v', 'error', '-y']
        if inicio > 0:
            cmd += ['-ss', str(inicio)]
        vf = ('scale=%d:%d:force_original_aspect_ratio=decrease:flags=lanczos,'
              'pad=%d:%d:(ow-iw)/2:(oh-ih)/2,fps=%d' % (w, h, w, h, fps))
        cmd += ['-i', path, '-t', str(seg), '-an', '-sn', '-vf', vf,
                '-c:v', 'cinepak', '-q:v', str(q), '-g', str(max(1, int(fps) * 2)),
                # faixas fixas e sem repasses extras dos livros de cores: ~2,3x mais rapido, mesma qualidade
                # medida. / fixed strip count, no extra codebook passes: ~2.3x faster
                '-min_strips', str(_strips), '-max_strips', str(_strips), '-max_extra_cb_iterations', '0',
                '-threads', '1', '-f', 'avi', tmp.name]
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out.returncode != 0:
            raise RuntimeError(out.stderr.decode('utf-8', 'ignore').strip() or 'ffmpeg falhou')
        return _avi_frames(open(tmp.name, 'rb').read())
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
            pass


def build_cvd(frames, w, h, fps):
    """Arquivo .cvd do 3DO ODE (video Cinepak, sem som). Tudo big-endian:
         0  "3DCV"
         4  u16 versao (1)        6  u16 flags (0; bit 0 = tem som, ainda nao usado)
         8  u16 largura          10  u16 altura
        12  u16 quadros/segundo  14  u16 numero de quadros
        16  u32 maior quadro (bytes, ja arredondado para 4)
        20  u32 onde comeca o 1o quadro
        24  u32 soma dos quadros (bytes)
        28  u32 0 (reservado)
        32  tabela: 1 u32 por quadro = tamanho arredondado para 4; bit 31 ligado = quadro-chave
        ..  os quadros Cinepak, um atras do outro, cada um completado com zeros ate multiplo de 4
       O boot le do comeco ao fim, sem voltar (o firmware nao tem busca no arquivo)."""
    table = bytearray()
    body = bytearray()
    biggest = 0
    for fr, key in frames:
        pad = (-len(fr)) % 4
        size = len(fr) + pad
        biggest = max(biggest, size)
        table += struct.pack('>I', size | (0x80000000 if key else 0))
        body += fr + b'\0' * pad
    head = bytearray(32)
    head[0:4] = b'3DCV'
    struct.pack_into('>HHHHHH', head, 4, 1, 0, w, h, fps, len(frames))
    struct.pack_into('>IIII', head, 16, biggest, 32 + len(table), len(body), 0)
    return bytes(head) + bytes(table) + bytes(body)
''',
  'iso2bincue': r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iso2bincue.py - converte .iso (setores de 2048 bytes, Mode 1) em .bin/.cue (setores RAW de 2352 bytes),
                reconstruindo sync, cabecalho MSF, EDC e ECC exatamente como numa prensagem. E o formato
                do Redump: o .bin resultante bate em tamanho e CRC com o .dat (se o disco era Mode 1
                de faixa unica, que e o caso de praticamente todo jogo de 3DO).
                converts a 2048-byte-sector .iso into a Redump-style MODE1/2352 .bin + .cue

Uso / usage:
    python iso2bincue.py Jogo.iso             -> Jogo.bin + Jogo.cue (o .iso fica)
    python iso2bincue.py Jogo.iso --apagar    -> apaga o .iso depois de conferir
    python iso2bincue.py <pasta>              -> converte todos os .iso da pasta

Precisa de numpy (pip install numpy): o calculo de ECC de ~300 mil setores e vetorizado por lote;
em Python puro levaria horas. / needs numpy
"""
import os, sys, zlib

try:
    import numpy as np
except ImportError:      # pragma: no cover
    np = None

SECTOR_RAW = 2352
SECTOR_DATA = 2048
BATCH = 1024             # setores por lote / sectors per batch

# ---------- tabelas (algoritmo classico do ecm.c de Neill Corlett) / lookup tables ----------
def _tables():
    f = [0] * 256; b = [0] * 256; edc = [0] * 256
    for i in range(256):
        j = (i << 1) ^ (0x11D if i & 0x80 else 0)
        f[i] = j & 0xFF
        b[(i ^ j) & 0xFF] = i
        e = i
        for _ in range(8):
            e = (e >> 1) ^ (0xD8018001 if e & 1 else 0)
        edc[i] = e & 0xFFFFFFFF
    return f, b, edc

ECC_F, ECC_B, EDC_LUT = _tables()


def _headers(first_lba, n):
    """cabecalhos MSF (min, seg, frame em BCD) + modo 1 para n setores a partir de first_lba"""
    h = np.zeros((n, 4), dtype=np.uint8)
    a = np.arange(first_lba, first_lba + n) + 150
    m = a // 4500; s = (a // 75) % 60; f = a % 75
    h[:, 0] = ((m // 10) << 4) | (m % 10)
    h[:, 1] = ((s // 10) << 4) | (s % 10)
    h[:, 2] = ((f // 10) << 4) | (f % 10)
    h[:, 3] = 1
    return h


def _edc_batch(sec):
    """EDC sobre os bytes 0..2063 de cada setor (vetorizado nos setores) / EDC over bytes 0..2063"""
    lut = np.array(EDC_LUT, dtype=np.uint32)
    edc = np.zeros(sec.shape[0], dtype=np.uint32)
    for i in range(0, 2064):
        edc = (edc >> 8) ^ lut[(edc ^ sec[:, i]) & 0xFF]
    return edc


def _ecc_block(src, major_count, minor_count, major_mult, minor_inc, dst, dst_off):
    """P/Q de um lote: src = setores[:, 12:12+2064+8] (cabecalho+dados+EDC+zeros) / one parity block"""
    f = np.array(ECC_F, dtype=np.uint8); b = np.array(ECC_B, dtype=np.uint8)
    size = major_count * minor_count
    n = src.shape[0]
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        ecc_a = np.zeros(n, dtype=np.uint8); ecc_b = np.zeros(n, dtype=np.uint8)
        for minor in range(minor_count):
            temp = src[:, index]
            index += minor_inc
            if index >= size:
                index -= size
            ecc_a ^= temp; ecc_b ^= temp
            ecc_a = f[ecc_a]
        ecc_a = b[f[ecc_a] ^ ecc_b]
        dst[:, dst_off + major] = ecc_a
        dst[:, dst_off + major + major_count] = ecc_a ^ ecc_b


def raw_sectors(data, first_lba):
    """data = n*2048 bytes -> n*2352 bytes (Mode 1 RAW) / builds the raw sectors of a batch"""
    n = len(data) // SECTOR_DATA
    sec = np.zeros((n, SECTOR_RAW), dtype=np.uint8)
    sec[:, 1:11] = 0xFF                                  # sync 00 FF*10 00
    sec[:, 12:16] = _headers(first_lba, n)
    sec[:, 16:16 + SECTOR_DATA] = np.frombuffer(data, dtype=np.uint8).reshape(n, SECTOR_DATA)
    edc = _edc_batch(sec)
    for k in range(4):
        sec[:, 2064 + k] = (edc >> (8 * k)) & 0xFF      # EDC little-endian
    # bytes 2068..2075 = 0 (intermediate). P cobre [12..2076); Q cobre [12..2248) (inclui a paridade P)
    src = sec[:, 12:2248]                                # view: a paridade P escrita entra no calculo de Q
    _ecc_block(src, 86, 24, 2, 86, sec, 2076)            # P: 172 bytes
    _ecc_block(src, 52, 43, 86, 88, sec, 2248)           # Q: 104 bytes
    return sec.tobytes()


def convert(iso_path, delete=False, progress=None):
    """Devolve (bin_path, crc_hex, n_setores) ou lanca excecao. / returns (bin, crc, sectors)"""
    global np
    if np is None:
        np = _ensure_pkg('numpy', 'numpy')   # Instala o numpy sozinho se faltar
    if np is None:
        raise RuntimeError('numpy nao instalado: pip install numpy')
    size = os.path.getsize(iso_path)
    if size % SECTOR_DATA:
        raise RuntimeError('tamanho nao e multiplo de 2048 (%d): nao parece um .iso Mode 1' % size)
    base = os.path.splitext(iso_path)[0]
    bin_path, cue_path = base + '.bin', base + '.cue'
    if os.path.exists(bin_path):
        raise RuntimeError('ja existe %s' % os.path.basename(bin_path))
    # Um .cue ORFAO (sem .bin) NAO bloqueia - ele sera sobrescrito pela conversao. / orphan .cue overwritten
    total = size // SECTOR_DATA
    crc = 0
    done = 0
    with open(iso_path, 'rb') as fi, open(bin_path + '.part', 'wb') as fo:
        while True:
            chunk = fi.read(BATCH * SECTOR_DATA)
            if not chunk:
                break
            raw = raw_sectors(chunk, done)
            fo.write(raw)
            crc = zlib.crc32(raw, crc)
            done += len(chunk) // SECTOR_DATA
            if progress:
                progress(done, total)
    os.replace(bin_path + '.part', bin_path)
    with open(cue_path, 'w', encoding='utf-8', newline='\r\n') as fc:
        fc.write('FILE "%s" BINARY\n  TRACK 01 MODE1/2352\n    INDEX 01 00:00:00\n' % os.path.basename(bin_path))
    if delete:
        os.remove(iso_path)
    return bin_path, format(crc & 0xFFFFFFFF, '08x'), total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    delete = '--apagar' in sys.argv or '--delete' in sys.argv
    if not args:
        print(__doc__); return 1
    targets = []
    for a in args:
        if os.path.isdir(a):
            targets += [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.lower().endswith('.iso') and 'boot' not in f.lower()]
        else:
            targets.append(a)
    for t in targets:
        def prog(d, n, _t=t):
            sys.stdout.write('\r  %s  %d%%' % (os.path.basename(_t), d * 100 // n)); sys.stdout.flush()
        try:
            b, crc, n = convert(t, delete, prog)
            print('\r  %s -> %s  (%d setores, CRC %s)' % (os.path.basename(t), os.path.basename(b), n, crc))
        except Exception as ex:
            print('\r  %s: %s' % (os.path.basename(t), ex))
    return 0


if __name__ == '__main__':
    sys.exit(main())
''',
  'midia_download': r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
midia_download.py - baixa capas e screenshots do 3DO (libretro-thumbnails) e
organiza em <destino>/cover e <destino>/screenshots.

Uso:
    python midia_download.py <pasta_dos_roms> [--destino "C:\\caminho"] [opções]

Para cada jogo (.iso/.cue/.chd/.zip) na pasta, procura a melhor capa e o melhor
screenshot no repositório do libretro e salva com o MESMO nome do ROM, em:
    <destino>/cover/<nome do jogo>.png
    <destino>/screenshots/<nome do jogo>.png

Destino padrão:
    C:\\Users\\rpasetchny\\Downloads\\3do\\Game List e Midias

Opções:
    --destino "<pasta>"   onde criar cover/ e screenshots/ (padrão acima)
    --com-subpastas       varre subpastas da pasta dos ROMs também
    --tudo                baixa TODAS as capas/screenshots do 3DO (ignora a pasta),
                          nomeadas como no libretro
    --refazer             rebaixa mesmo se o arquivo já existir
"""
import os, re, sys, json, difflib, unicodedata
import urllib.request, urllib.parse

REPO = 'libretro-thumbnails/The_3DO_Company_-_3DO'
RAW = 'https://raw.githubusercontent.com/' + REPO + '/master/'
API = 'https://api.github.com/repos/' + REPO + '/git/trees/master?recursive=1'
UA = {'User-Agent': 'midia_download/1 (3DO ODE)'}
GAME_EXT = ('.iso', '.cue', '.chd', '.zip')
DEST_PADRAO = r'C:\Users\rpasetchny\Downloads\3do\Game List e Midias'
KINDS = [('cover', 'Named_Boxarts'), ('screenshots', 'Named_Snaps'), ('titles', 'Named_Titles')]


def norm(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    s = s.replace('_', ' ').replace('&', ' and ')
    s = re.sub(r'[\(\[][^\)\]]*[\)\]]', ' ', s)
    s = re.sub(r'^(.*), (the|a|o)\s*$', r'\2 \1', s.strip())
    return re.sub(r'[^a-z0-9]+', '', s)


def region(name):
    t = ' '.join(re.findall(r'\(([^)]*)\)', name)).lower()
    if re.search(r'\b(usa|us)\b', t): return 'usa'
    if re.search(r'\b(europe|eu|pal)\b', t): return 'europe'
    if re.search(r'\b(japan|jp|jpn)\b', t): return 'japan'
    if 'korea' in t: return 'korea'
    return ''


def pick(cands, want):
    order = [want, 'usa', 'europe', 'japan', 'korea', '']
    return sorted(cands, key=lambda b: (order.index(region(b)) if region(b) in order else 9, len(b)))[0]


def _names_from_repo():
    """Lista 'Named_Boxarts/x.png' etc. pela API do GitHub."""
    try:
        tree = json.load(urllib.request.urlopen(urllib.request.Request(API, headers=UA), timeout=30))
        names = [t.get('path', '') for t in tree.get('tree', [])]
        print('  lista via GitHub API: %d arquivos' % len(names))
        return names
    except Exception as e:
        print('  (não consegui listar o repositório:', e, '- vou tentar pelo nome direto)')
        return None


def fetch_index():
    """Retorna {folder: {norm: [bases]}} ou None."""
    names = _names_from_repo()
    if not names:
        return None
    idx = {f: {} for _, f in KINDS}
    for p in names:
        for _, folder in KINDS:
            if p.startswith(folder + '/') and p.lower().endswith('.png'):
                base = p[len(folder) + 1:-4]
                idx[folder].setdefault(norm(base), []).append(base)
    return idx


def best_name(idx, folder, rombase):
    """Melhor nome no repo para esse ROM, via índice (exato/aproximado)."""
    table = idx[folder]
    key = norm(rombase)
    if key in table:
        return pick(table[key], region(rombase))
    close = difflib.get_close_matches(key, list(table), n=1, cutoff=0.88)
    return pick(table[close[0]], region(rombase)) if close else None


def baixa(folder, base, dest):
    url = RAW + folder + '/' + urllib.parse.quote(base + '.png')
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'wb').write(data)
    return len(data)


def roms_da_pasta(root, subpastas):
    out = []
    for dp, dirs, files in os.walk(root):
        for f in files:
            low = f.lower()
            if any(low.endswith(e) for e in GAME_EXT):
                out.append(os.path.splitext(f)[0])
        if not subpastas:
            break
    return sorted(set(out))


def main(root, destino, subpastas, tudo, refazer):
    print('Conectando ao libretro-thumbnails...')
    idx = fetch_index()

    dest_by = {}
    for kind, _ in KINDS:
        d = os.path.join(destino, kind)
        os.makedirs(d, exist_ok=True)
        dest_by[kind] = d

    # modo --tudo: baixa todos, nomeados como no libretro
    if tudo:
        if not idx:
            print('Preciso da lista do repositório para --tudo. Tente de novo mais tarde.')
            return 2
        ok = miss = 0
        for kind, folder in KINDS:
            names = sorted({b for lst in idx[folder].values() for b in lst})
            print('%s: %d arquivos' % (kind, len(names)))
            for b in names:
                dest = os.path.join(dest_by[kind], b + '.png')
                if os.path.exists(dest) and not refazer:
                    ok += 1; continue
                try:
                    baixa(folder, b, dest); ok += 1
                except Exception as e:
                    miss += 1; print('   falhou:', b, e)
        print('Prontos: %d | falhas: %d' % (ok, miss))
        print('Em:', destino)
        return 0

    # modo por pasta de ROMs
    if not os.path.isdir(root):
        print('Pasta dos ROMs não encontrada:', root)
        return 2
    roms = roms_da_pasta(root, subpastas)
    print('Jogos encontrados:', len(roms))
    got = {k: 0 for k, _ in KINDS}
    miss = {k: [] for k, _ in KINDS}
    for rb in roms:
        for kind, folder in KINDS:
            dest = os.path.join(dest_by[kind], rb + '.png')
            if os.path.exists(dest) and not refazer:
                got[kind] += 1; continue
            # tenta o índice; se não achar (ex.: Named_Titles não está na lista embutida), usa o nome direto
            name = (best_name(idx, folder, rb) if idx else None) or rb
            try:
                baixa(folder, name, dest); got[kind] += 1
            except Exception:
                # fallback: tenta o próprio nome do ROM
                try:
                    baixa(folder, rb, dest); got[kind] += 1
                except Exception:
                    miss[kind].append(rb)
    for kind, _ in KINDS:
        print('%-11s baixados: %d | sem imagem: %d' % (kind, got[kind], len(miss[kind])))
        for rb in miss[kind][:20]:
            print('   - ' + rb)
        if len(miss[kind]) > 20:
            print('   ... e mais %d' % (len(miss[kind]) - 20))
    print('Salvo em:', destino)
    return 0


if __name__ == '__main__':
    argv = sys.argv[1:]
    opts = [a for a in argv if a.startswith('--')]
    pos = [a for a in argv if not a.startswith('--')]
    destino = DEST_PADRAO
    if '--destino' in argv:
        i = argv.index('--destino')
        if i + 1 < len(argv):
            destino = argv[i + 1]
            if destino in pos:
                pos.remove(destino)
    root = pos[0] if pos else ''
    tudo = '--tudo' in opts
    if not root and not tudo:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(root, destino,
                  subpastas='--com-subpastas' in opts,
                  tudo=tudo,
                  refazer='--refazer' in opts))
''',
}
for _hn, _hs in _HELPER_SRC.items():
    try:
        _hm = _types.ModuleType(_hn)
        exec(compile(_hs, _hn + '.py', 'exec'), _hm.__dict__)
        sys.modules[_hn] = _hm
    except Exception:
        pass
# ====== FIM DOS MODULOS EMBUTIDOS ======
try:
    import converte_video as vconv   # conversor de video Cinepak / video converter
except Exception:
    vconv = None
def _ensure_pkg(pip_name, import_name):
    """importa import_name; se faltar, INSTALA pip_name sozinho (uma vez) e tenta de novo. / auto-install."""
    import importlib, subprocess
    try:
        return importlib.import_module(import_name)
    except ImportError:
        pass
    print("\n  Instalando %s (uma vez so)... / installing %s (once)..." % (pip_name, pip_name))
    # Python sem o pip (raro): poe o pip primeiro. / no pip yet: bootstrap it
    try:
        importlib.import_module("pip")
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        except Exception:
            pass
    for extra in ([], ["--user"], ["--break-system-packages"]):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name] + extra)
        except Exception:
            continue
        try:
            return importlib.import_module(import_name)
        except ImportError:
            continue
    return None

if _ensure_pkg("pillow", "PIL") is None:
    print("\n  Nao consegui instalar o Pillow automaticamente.")
    print("  Tente manualmente e rode de novo:  py -m pip install pillow\n")
    sys.exit(1)
from PIL import Image, ImageFilter

BG = (12, 4, 20)
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')
VIDEO_EXT = ('.mp4', '.avi', '.mkv', '.mov', '.webm', '.m4v', '.mpg', '.mpeg', '.flv')
GAME_EXT = ('.iso', '.cue', '.bin')   # so jogo de verdade (nao .img de imagem, nem .chd/.zip) / real games only
SKIP_DIRS = {'_capas_originais', 'cover', 'covers', 'capas', 'screenshot', 'screenshots', 'telas',
             'video', 'videos', 'txt', 'info', 'system volume information'}
REPO = 'libretro-thumbnails/The_3DO_Company_-_3DO'
RAW = 'https://raw.githubusercontent.com/' + REPO + '/master/'
UA = {'User-Agent': 'generate_usb (3DO ODE)'}

NAMES_FALLBACK = (
    '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'
)


def norm(name):
    """Titulo comparavel / comparable title: sem acento, sem (tags), so letras e numeros."""
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    s = s.replace('_', ' ').replace('&', ' and ')
    s = re.sub(r'[\(\[][^\)\]]*[\)\]]', ' ', s)
    s = re.sub(r'^(.*), (the|a|o)\s*$', r'\2 \1', s.strip())
    return re.sub(r'[^a-z0-9]+', '', s)


def region(name):
    t = ' '.join(re.findall(r'\(([^)]*)\)', name)).lower()
    if re.search(r'\b(usa|us|en-us|eu-us)\b', t): return 'usa'
    if re.search(r'\b(europe|eu|uk|germany|france|spain|italy)\b', t): return 'europe'
    if re.search(r'\b(japan|jp|jpn|j)\b', t): return 'japan'
    if 'korea' in t: return 'korea'
    return ''


def pretty(base):
    s = re.sub(r'\s*[\(\[][^\)\]]*[\)\]]', '', base.replace('_', ' ')).strip()
    m = re.match(r'^(.*), (The|A|O)$', s)
    return f'{m.group(2)} {m.group(1)}' if m else (s or base)


# ---------------- LISTA DE IMAGENS DO LIBRETRO / LIBRETRO IMAGE LIST ----------------
def remote_names():
    """Lista atual do GitHub; se falhar, usa a lista embutida no script."""
    try:
        req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/trees/master?recursive=1', headers=UA)
        tree = json.load(urllib.request.urlopen(req, timeout=20))
        names = [t['path'] for t in tree.get('tree', []) if t['path'].startswith(('Named_Boxarts/', 'Named_Snaps/'))]
        if names:
            return names, 'GitHub'
    except Exception:
        pass
    return zlib.decompress(base64.b64decode(''.join(NAMES_FALLBACK))).decode().splitlines(), 'lista embutida'


def index_remote(names):
    idx = {'Named_Boxarts': {}, 'Named_Snaps': {}}
    for p in names:
        folder, f = p.split('/', 1)
        base = f[:-4]
        idx[folder].setdefault(norm(base), []).append(base)
    return idx


def pick(cands, want_region):
    """Escolhe a melhor regiao / picks the best region: a da ISO, depois USA, Europa, qualquer."""
    order = [want_region, 'usa', 'europe', 'japan', 'korea', '']
    def score(b):
        r = region(b)
        return (order.index(r) if r in order else 9, len(b))
    return sorted(cands, key=score)[0]


def find_remote(idx, folder, isobase):
    table = idx[folder]
    key = norm(isobase)
    if key in table:
        return pick(table[key], region(isobase))
    close = difflib.get_close_matches(key, list(table), n=1, cutoff=0.88)
    return pick(table[close[0]], region(isobase)) if close else None


def download(folder, base, dest):
    url = RAW + folder + '/' + urllib.parse.quote(base + '.png')
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=30).read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'wb').write(data)


# ---------------- TEXTOS / TEXTS ----------------
def read_txt(path):
    raw = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'cp1252', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode('latin-1', 'ignore')


def load_gamelist(paths):
    """gamelist.txt: blocos [Titulo] seguidos de Chave=Valor / [Title] blocks followed by Key=Value.
    Varias linhas [Nome] seguidas = apelidos do mesmo jogo / several [Name] lines in a row = aliases."""
    db = {}
    for path in paths:
        if not os.path.isfile(path):
            continue
        heads, body = [], None
        def flush():
            if heads and body:
                for h in heads:
                    db.setdefault(h, body)
        for line in read_txt(path).splitlines():
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            m = re.match(r'^\[(.+)\]$', s)
            if m:
                if body is not None:
                    flush(); heads, body = [], None
                heads.append(norm(m.group(1))); continue
            if heads and '=' in s:
                k, v = s.split('=', 1)
                if v.strip():                      # campo vazio = ignorado / empty field = skipped
                    body = (body or '') + k.strip() + '=' + v.strip() + '\n'
                elif body is None:
                    body = ''
        flush()
    return {k: v for k, v in db.items() if v}


def find_text(gamelist, isobase):
    """Acha o bloco do jogo: nome exato, depois parecido (mesmos numeros, p/ nao trocar 1 por 2)."""
    key = norm(isobase)
    if key in gamelist:
        return gamelist[key]
    pre = [k for k in gamelist if len(key) >= 8 and k.startswith(key)]
    if len(pre) == 1:                      # "Wing Commander III" -> "... - Heart of the Tiger"
        return gamelist[pre[0]]
    digits = re.findall(r'\d+', key)
    for c in difflib.get_close_matches(key, list(gamelist), n=5, cutoff=0.9):
        if re.findall(r'\d+', c) == digits:
            return gamelist[c]
    return None


# ---- gamelist.xml (Batocera / EmulationStation / Skyscraper / ARRM) ----
GENRE_PT = [('survival horror', 'Survival horror'), ('point and click', 'Aventura'), ('1st person', 'Tiro em 1ª pessoa'),
            ('lightgun', 'Tiro com pistola'), ("shoot'em up", 'Tiro'), ('shooter', 'Tiro'), ('fight', 'Luta'),
            ('golf', 'Golfe'), ('soccer', 'Futebol'), ('football', 'Futebol americano'), ('basketball', 'Basquete'),
            ('baseball', 'Beisebol'), ('boxing', 'Boxe'), ('horse', 'Turfe'), ('motorcycle', 'Corrida de motos'),
            ('race', 'Corrida'), ('driving', 'Corrida'), ('mahjong', 'Mahjong'), ('pinball', 'Pinball'),
            ('casino', 'Cassino'), ('cards', 'Cartas'), ('board', 'Tabuleiro'), ('quiz', 'Quiz'),
            ('role playing', 'RPG'), ('platform', 'Plataforma'), ('puzzle', 'Puzzle'), ('build and management', 'Gerenciamento'),
            ('strategy', 'Estratégia'), ('simulation', 'Simulação'), ('educational', 'Educativo'), ('sports', 'Esporte'),
            ('adventure', 'Aventura'), ('action', 'Ação')]
PUBLISHERS = {'panasonic', '3do', 'electronicarts', 'easports', 'eagames', 'interplay', 'mindscape', 'psygnosis'}


def short_desc(d, limit=1000):
    # O boot rola o texto todo: so corta (num fim de frase) acima de 1000 letras.
    d = re.sub(r'\s+', ' ', d or '').strip()
    if len(d) <= limit:
        return d
    cut = d[:limit]
    end = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    return cut[:end + 1] if end > 80 else cut[:cut.rfind(' ')] + '...'


def load_gamelist_xml(paths):
    """Le gamelist.xml e devolve {titulo: {Year,Developer,Genre,Description}} / reads gamelist.xml."""
    import xml.etree.ElementTree as ET
    db = {}
    for path in paths:
        if not os.path.isfile(path):
            continue
        try:
            root = ET.parse(path).getroot()
        except Exception as ex:
            print('  gamelist.xml invalido / invalid:', path, ex); continue
        for e in root.iter('game'):
            if (e.findtext('hidden') or '') == 'true':
                continue
            f = {}
            y = (e.findtext('releasedate') or '')[:4]
            if y.isdigit() and 1993 <= int(y) <= 2030: f['Year'] = y
            d = (e.findtext('developer') or '').strip()
            if d and norm(d) not in PUBLISHERS: f['Developer'] = d[:40]
            gl = (e.findtext('genre') or '').lower()
            for en, pt in GENRE_PT:
                if en in gl: f['Genre'] = pt; break
            if e.findtext('desc'): f['Description'] = short_desc(e.findtext('desc'))
            for t in (os.path.splitext(os.path.basename(e.findtext('path') or ''))[0], e.findtext('name') or ''):
                if t: db.setdefault(norm(t), f)
    return db


def merge_xml(text, xmlf):
    """Completa so os campos que faltam / fills only missing fields."""
    have = {m.lower() for m in re.findall(r'^\s*(\w+)\s*=\s*\S', text, re.M)}
    alias = {'year': {'year', 'ano'}, 'developer': {'developer', 'dev', 'desenvolvedor'},
             'genre': {'genre', 'genero', 'gênero'}, 'description': {'description', 'desc', 'descricao', 'descrição'}}
    for k, v in xmlf.items():
        if not (alias[k.lower()] & have):
            text += f'{k}={v}\n'
    return text


# ---------------- IMAGENS / IMAGES ----------------
# Dithering ordenado (Bayer 4x4): espalha o erro do RGB555 em vez de truncar,
# tirando o "banding" (degraus de cor) - de graca, mesmo tamanho de arquivo.
# Ordered (Bayer 4x4) dithering: spreads the RGB555 error instead of truncating,
# removing colour banding at no extra size.
_BAYER = (0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5)
_DOFF = tuple(int(round((c + 0.5) / 16.0 * 8 - 4)) for c in range(16))   # passo do 5-bit = 8


def _img_ok(path):
    """True se a imagem abre de verdade (pega .png corrompido/incompleto). / valid image?"""
    try:
        _im = Image.open(path); _im.load(); return True
    except Exception:
        return False


# ================= CAPAS E TELAS EM CEL (preparo "TEXTO") =================
# O boot 3DO ODE le CEL 16 bits RGB555 sem compressao direto para o cache e desenha pelo motor de
# CELs, sem conversao no console. Formato: bloco "CCB " de 80 bytes + bloco "PDAT" com as linhas
# alinhadas a 4 bytes (minimo 8), tudo big-endian.
#   covers/<jogo>.cel        capa, TODAS 88x122 (preenche: corta ate 12%, estica o resto), cantos transparentes, so imagem (dados no 3dogamesdetails.ode)
#   screenshots/<jogo>.cel   tela, ENCAIXADA em 240x180 (4:3), para a tela de detalhes
# As pastas covers/ e screenshots/ ficam SEMPRE na raiz do cartao, para todos os jogos (raiz e pastas).
# Preparo "TEXTO": reducao em luz linear, nitidez, arredondamento pelo nivel real de 5 bits do 3DO
# e pontilhado Floyd-Steinberg so fora dos contornos (letras ficam nitidas).
# TAMANHO DA CAPA: a capa INTEIRA (sem cortar nada) e esticada para a caixa, com os cantos
# arredondados transparentes.
CEL_COVER_SIZES = {'f': (100, 140)}
CEL_COVER_SIZE = 'f'
CEL_COVER_BOX = CEL_COVER_SIZES[CEL_COVER_SIZE]
CEL_COVER_CROP = 0.0             # quanto pode cortar (de cada eixo) antes de esticar: 0 = mostra a capa inteira
# DOIS TAMANHOS, cada um na sua subpasta, sempre na raiz do cartao:
#   covers/small/<jogo>.cel        56x78   grade CAPAS e a capa pequena da tela de inicio (~9 KB)
#   covers/large/<jogo>.cel        100x140 lista, carrossel e descricao (~28 KB)
#   screenshots/medium/<jogo>.cel  cabe em 120x90: a caixa da descricao e a da lista (~22 KB)
#   screenshots/large/<jogo>.cel   cabe em 304x228: tela cheia no X (~139 KB)
CEL_COVER_SMALL = (56, 78)
CEL_SHOT_MEDIUM = (120, 90)
CEL_SHOT_LARGE = (304, 228)
CEL_EXT_COVER = '.cel'           # extensao da capa em covers/
CEL_EXT_SHOT = '.cel'            # extensao da tela em screenshots/
CEL_FILE_LIMIT = 160 * 1024      # maior CEL aceito (a tela grande 304x228 tem ~139 KB)
CEL_SHARPEN, CEL_STRENGTH, CEL_EDGE_LIMIT = 1.1, 0.85, 32

# PREPAROS DA IMAGEM (--capa-preparo / assistente): (nitidez, forca do pontilhado, so fora dos contornos?, explicacao)
# Pontilhado = espalha o erro das cores de 15 bits do 3DO (tira as faixas dos degrades, mas granula).
CEL_PRESETS = {
    # Boot 1.4 em diante so existe UM jeito de converter (imagem limpa: media de area + nitidez leve, sem
    # pontilhado). Os outros nomes ficam so para o .ini antigo continuar valendo; o resultado e o mesmo.
    'limpa':     (0.0,  0.0,  False, 'LIMPA (padrao): media de area + nitidez leve, sem pontilhado'),
    'texto':     (1.1,  0.85, True,  'TEXTO (padrao): nitidez forte + pontilhado so fora das letras; letras mais legiveis'),
    'nitida':    (0.7,  0.7,  True,  'NITIDA: nitidez media + pontilhado medio; meio-termo'),
    'suave':     (0.35, 0.5,  True,  'SUAVE: pouca nitidez + pontilhado leve; imagem mais lisa, letras mais moles'),
    'sempontos': (0.35, 0.0,  False, 'SEM PONTOS: sem pontilhado nenhum; cores lisas, mas degrades podem ter faixas'),
    'corfiel':   (0.6,  0.85, False, 'COR FIEL: pontilhado em tudo; cor mais fiel, porem mais granulada e letras menos nitidas'),
}
CEL_PRESET = 'limpa'


def cel_set_options(preset=None, size=None):
    """Escolhe o preparo das capas e telas (texto/nitida/suave/sempontos/corfiel) e o tamanho da capa (p/m)."""
    global CEL_PRESET, CEL_COVER_SIZE, CEL_COVER_BOX
    if size:
        size = size.strip().lower()[:1]
        if size not in CEL_COVER_SIZES:
            return    # tamanho desconhecido: fica o padrao
        CEL_COVER_SIZE = size
        CEL_COVER_BOX = CEL_COVER_SIZES[size]
    if preset:
        preset = preset.lower().replace('-', '').replace(' ', '').replace('_', '')
        if preset not in CEL_PRESETS:
            raise ValueError('preparo invalido: %s (use texto, nitida, suave, sempontos ou corfiel)' % preset)
        CEL_PRESET = preset


def cel_existing_size(covers_dir):
    """Tamanho (largura, altura) das capas que ja estao em covers/, lido do cabecalho do primeiro .cel
    valido (o mesmo que o boot faz); None se nao tem nenhuma."""
    try:
        names = sorted(n for n in os.listdir(covers_dir) if n.lower().endswith(CEL_EXT_COVER))
    except OSError:
        return None
    for n in names[:20]:
        try:
            with open(os.path.join(covers_dir, n), 'rb') as f:
                h = f.read(80)
            if len(h) == 80 and h[:4] == b'CCB ':
                return struct.unpack('>II', h[72:80])
        except OSError:
            pass
    return None

# flags do CCB iguais ao InitCel do Portfolio (ponteiros absolutos, preambulos no CCB)
CEL_CCB_FLAGS = (0x40000000 | 0x20000000 | 0x10000000 | 0x08000000 |
                 0x04000000 | 0x02000000 | 0x01000000 | 0x00400000 |
                 0x00200000 | 0x00000400 | 0x00000010 | 0x00004000 |
                 0x00040000 | 0x00020000 | 0x00000020)
CEL_PIXC_OPAQUE = 0x1F001F00
# luz linear de cada valor sRGB 0..255
_CEL_TO_LINEAR = [((v / 255.0) / 12.92) if v / 255.0 <= 0.04045 else (((v / 255.0) + 0.055) / 1.055) ** 2.4
                  for v in range(256)]
# como o 3DO expande 5 bits para 8 na saida de video (v<<3 | v>>2)
_CEL_LEVEL8 = [(v << 3) | (v >> 2) for v in range(32)]


def _cel_to_srgb(x):
    """Luz linear 0..1 -> sRGB 0..255."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 255.0
    s = x * 12.92 if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055
    return s * 255.0


def _cel_nearest5(x):
    """Nivel de 5 bits cujo valor mostrado pelo 3DO e o mais proximo de x (0..255)."""
    v = int(x * 31.0 / 255.0 + 0.5)
    v = 0 if v < 0 else (31 if v > 31 else v)
    best = v
    for c in (v - 1, v + 1):
        if 0 <= c <= 31 and abs(_CEL_LEVEL8[c] - x) < abs(_CEL_LEVEL8[best] - x):
            best = c
    return best


def _cel_resize_area(image, size):
    """Reduz pela MEDIA DE AREA em luz linear (cada pixel de destino = media de toda a area de origem que cai
    nele; sem serrilha e sem halo) e devolve RGB 8 bits. Ampliando, usa bicubica. Igual ao index.html."""
    filt = Image.BOX if (size[0] <= image.size[0] and size[1] <= image.size[1]) else Image.BICUBIC
    bands = []
    for band in image.split():
        f = Image.new('F', band.size)
        f.putdata([_CEL_TO_LINEAR[v] for v in band.tobytes()])
        f = f.resize(size, filt)
        out = Image.new('L', size)
        vals = struct.unpack('=%df' % (size[0] * size[1]), f.tobytes())
        out.putdata([max(0, min(255, int(_cel_to_srgb(max(0.0, min(1.0, v))) + 0.5))) for v in vals])
        bands.append(out)
    return Image.merge('RGB', bands)


def _cel_clean(image):
    """Nitidez leve (c + (4c - vizinhos) / 5) e arredondamento para RGB555, SEM pontilhado. Devolve as cores."""
    image = image.convert('RGB').filter(ImageFilter.Kernel((3, 3), [0, -1, 0, -1, 9, -1, 0, -1, 0], 5))
    raw = image.tobytes()
    return [(((raw[i] * 31 + 127) // 255) << 10) | (((raw[i + 1] * 31 + 127) // 255) << 5) | ((raw[i + 2] * 31 + 127) // 255)
            for i in range(0, len(raw), 3)]


def _cel_resize_linear(image, size):
    """Reduz em luz linear (gamma correto) e devolve RGB 8 bits."""
    bands = []
    for band in image.split():
        f = Image.new('F', band.size)
        f.putdata([_CEL_TO_LINEAR[v] for v in band.tobytes()])
        f = f.resize(size, Image.LANCZOS)
        out = Image.new('L', size)
        vals = struct.unpack('=%df' % (size[0] * size[1]), f.tobytes())
        out.putdata([int(_cel_to_srgb(v) + 0.5) for v in vals])
        bands.append(out)
    return Image.merge('RGB', bands)


def _cel_trim_borders(img, tol=24):
    """Tira margens de cor lisa (moldura da foto) presentes em 3 ou mais lados."""
    from PIL import ImageChops
    corner = img.getpixel((0, 0))
    bg = Image.new('RGB', img.size, corner)
    diff = ImageChops.difference(img, bg).convert('L').point(lambda v: 255 if v > tol else 0)
    box = diff.getbbox()
    if not box:
        return img
    l, t, r, b = box
    if (r - l) < img.width * 0.5 or (b - t) < img.height * 0.5:
        return img
    m = 2   # moldura de verdade aparece em pelo menos 3 lados; ceu liso so no topo nao conta
    if (l >= m) + (t >= m) + (img.width - r >= m) + (img.height - b >= m) < 3:
        return img
    return img.crop(box)


def _cel_edge_mask(image, limit=40):
    """True onde ha contorno forte (letras): ali nao entra pontilhado."""
    lum = image.convert('L')
    w, h = lum.size
    hi = lum.filter(ImageFilter.MaxFilter(3)).tobytes()
    lo = lum.filter(ImageFilter.MinFilter(3)).tobytes()
    return [hi[i] - lo[i] >= limit for i in range(w * h)]


def _cel_quantize(image, strength=0.85, edges=None):
    """Cores RGB555 linha a linha: Floyd-Steinberg serpentina; nos contornos so arredonda."""
    image = image.convert('RGB')
    w, h = image.size
    raw = image.tobytes()
    px = [raw[i:i + 3] for i in range(0, len(raw), 3)]
    out = [0] * (w * h)
    cur = [[float(c) for c in p] for p in px[0:w]]
    for y in range(h):
        nxt = [[float(c) for c in p] for p in px[(y + 1) * w:(y + 2) * w]] if y + 1 < h else None
        rev = y & 1
        xs = range(w - 1, -1, -1) if rev else range(w)
        d = -1 if rev else 1
        for x in xs:
            pix = cur[x]
            if edges is not None and edges[y * w + x]:
                q = [_cel_nearest5(c) for c in px[y * w + x]]
                out[y * w + x] = (q[0] << 10) | (q[1] << 5) | q[2]
                continue
            q = [_cel_nearest5(c) for c in pix]
            out[y * w + x] = (q[0] << 10) | (q[1] << 5) | q[2]
            for k in range(3):
                e = (pix[k] - _CEL_LEVEL8[q[k]]) * strength
                if e == 0:
                    continue
                xn = x + d
                if 0 <= xn < w:
                    cur[xn][k] += e * 7 / 16
                if nxt is not None:
                    xp = x - d
                    if 0 <= xp < w:
                        nxt[xp][k] += e * 3 / 16
                    nxt[x][k] += e * 5 / 16
                    if 0 <= xn < w:
                        nxt[xn][k] += e * 1 / 16
        cur = nxt
    return out


def cel_encode(colors, width, height):
    """Grava o CEL: CCB (80 bytes) + PDAT com as linhas alinhadas a 32 bits."""
    if not (1 <= width <= 2047 and 1 <= height <= 1024):
        raise ValueError('CEL maior que 2047 x 1024')
    row_bytes = max(8, (width * 2 + 3) & ~3)
    if 88 + row_bytes * height > CEL_FILE_LIMIT:
        raise ValueError('CEL maior que o limite (96 KB)')
    preamble0 = ((height - 1) << 6) | 0x10 | 6
    preamble1 = ((row_bytes // 4 - 2) << 16) | 0x1000 | (width - 1)
    words = [0, CEL_CCB_FLAGS, 0, 0, 0, 0, 0, 1 << 20, 0, 0, 1 << 16,
             0, 0, CEL_PIXC_OPAQUE, preamble0, preamble1, width, height]
    control = struct.pack('>4sI18I', b'CCB ', 80, *words)
    pixels = bytearray(row_bytes * height)
    for i, c in enumerate(colors):
        row, column = divmod(i, width)
        struct.pack_into('>H', pixels, row * row_bytes + column * 2, c)
    return control + struct.pack('>4sI', b'PDAT', len(pixels) + 8) + pixels


def _cel_fit(size, box):
    """Maior tamanho que cabe na caixa mantendo a proporcao (nunca amplia)."""
    w, h = size
    scale = min(box[0] / w, box[1] / h, 1.0)
    return max(1, round(w * scale)), max(1, round(h * scale))


def cel_image_size(path, box):
    """Tamanho (w, h) que cel_image(path, box, fill=True) daria, sem codificar o CEL."""
    im = Image.open(path)
    im.load()
    try:
        from PIL import ImageOps
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass
    im = im.convert('RGBA')
    canvas = Image.new('RGBA', im.size, (0, 0, 0, 255))
    canvas.alpha_composite(im)
    fw, fh = _cel_trim_borders(canvas.convert('RGB')).size
    tw, th = box
    k = min(tw / fw, th / fh)
    w, h = tw, th
    if os.environ.get('CAPAS_ESTICADAS') != '1':
        if fw * k < tw * 0.96:
            w = max(8, int(round(fw * k / 2)) * 2)
        if fh * k < th * 0.96:
            h = max(8, int(round(fh * k)))
    return (w, h)


def cel_image(path, box, fill=False):
    """Imagem -> CEL encaixado na caixa com o preparo escolhido (CEL_PRESET, padrao TEXTO).
    fill=False: cabe inteira na caixa (sem cortar, sem ampliar). fill=True (capas): na proporcao da propria
    capa, encostada na caixa (amplia se preciso), com os cantos arredondados; long box ~76x140, caixa de CD
    ~100x87. Nunca estica nem corta. Devolve (bytes do CEL, largura, altura)."""
    im = Image.open(path)
    im.load()
    try:
        from PIL import ImageOps
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass
    im = im.convert('RGBA')
    canvas = Image.new('RGBA', im.size, (0, 0, 0, 255))
    canvas.alpha_composite(im)
    flat = _cel_trim_borders(canvas.convert('RGB'))
    sharpen, strength, mask, _ = CEL_PRESETS[CEL_PRESET]
    if fill:
        # CAPA NA PROPORCAO DELA, sem esticar e sem cortar (boot 1.3.1 em diante): encosta na caixa
        # (long box fica mais estreita, caixa de CD mais baixa). Largura par. Quase a proporcao da caixa
        # (ate 4%): ocupa a caixa inteira. O menu escolhe como mostrar a sobra (Opcoes > Formato das capas).
        fw, fh = flat.size
        tw, th = box
        k = min(tw / fw, th / fh)
        w, h = tw, th
        # TESTE: CAPAS_ESTICADAS=1 no ambiente volta a capa esticada na caixa inteira (formato antigo).
        if os.environ.get('CAPAS_ESTICADAS') != '1':
            if fw * k < tw * 0.96:
                w = max(8, int(round(fw * k / 2)) * 2)
            if fh * k < th * 0.96:
                h = max(8, int(round(fh * k)))
        size = (w, h)
    else:
        size = _cel_fit(flat.size, box)
    # Imagem LIMPA (boot 1.3.1 em diante): media de area + nitidez leve + sem pontilhado. Os preparos antigos
    # (texto, nitida, suave...) nao mudam mais nada; ficam so para o .ini antigo continuar valendo.
    img = _cel_resize_area(flat, size) if size != flat.size else flat
    colors = _cel_clean(img)
    if fill:
        colors = _cel_round_corners(colors, img.width, img.height)
    return cel_encode(colors, img.width, img.height), img.width, img.height


# Cantos da capa: pixels 0x0000 = transparentes no boot (o CEL da capa e desenhado sem o fundo), entao a
# borda arredondada aparece por tras e "come" os cantos. Linha 0 perde 2 pixels de cada lado, linha 1 perde 1.
CEL_CORNER = (2, 1)


def _cel_round_corners(colors, w, h):
    """Nenhum pixel preto puro (0x0000 vira 0x0001, igual a olho) e os cantos ficam 0x0000 (transparentes)."""
    out = [c if c else 1 for c in colors]
    for r, n in enumerate(CEL_CORNER):
        for y in (r, h - 1 - r):
            for x in list(range(n)) + list(range(w - n, w)):
                out[y * w + x] = 0
    return out


def cel_to_png(cel_path, png_path):
    """CEL de 16 bits sem compressao (o das capas e telas) -> PNG, para refazer outro tamanho a partir dele
    quando a imagem original nao esta mais na pasta de midias. False se o arquivo nao serve."""
    try:
        d = open(cel_path, 'rb').read()
        if len(d) < 88 or d[:4] != b'CCB ' or d[80:84] != b'PDAT':
            return False
        w, h = struct.unpack('>II', d[72:80])
        rb = max(8, (w * 2 + 3) & ~3)
        if not (0 < w <= 320 and 0 < h <= 240) or len(d) < 88 + rb * h:
            return False
        # 16 bits (5-5-5, byte alto primeiro) -> 24 bits, de uma vez por linha
        rgb = bytearray(w * h * 3)
        lv = _CEL_LEVEL8
        for y in range(h):
            row = struct.unpack('>%dH' % w, d[88 + y * rb:88 + y * rb + w * 2])
            o = y * w * 3
            rgb[o:o + w * 3:3] = bytes(lv[(v >> 10) & 31] for v in row)
            rgb[o + 1:o + w * 3:3] = bytes(lv[(v >> 5) & 31] for v in row)
            rgb[o + 2:o + w * 3:3] = bytes(lv[v & 31] for v in row)
        Image.frombytes('RGB', (w, h), bytes(rgb)).save(png_path)
        return True
    except Exception:
        return False


def _cfield(text, *names):
    """Valor do 1o campo Chave=Valor encontrado no bloco de texto (aceita PT e EN)."""
    low = [n.lower() for n in names]
    for line in (text or '').splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            if k.strip().lower() in low:
                return re.sub(r'\s+', ' ', v).strip()
    return ''


def disc_num(name):
    """Numero do disco no nome (Disc 2, Disk 3, CD2...); 1 se nao houver."""
    m = re.search(r'\b(?:disc|disk|cd)\s*([0-9]+)', name, re.I)
    return int(m.group(1)) if m else 1


def detail_line(isobase, text, genre, maxdesc=1000):
    """Monta a linha do 3dogamesdetails.ode:
    nome<TAB>ano<TAB>genero<TAB>produtora<TAB>descricao<TAB>publicadora
    A publicadora (Publisher=) vai no fim para o boot antigo continuar lendo os 5 primeiros campos.
    short_desc so corta a descricao num fim de frase acima de maxdesc letras."""
    yr = _cfield(text, 'year', 'ano')[:6]
    gn = (genre or _cfield(text, 'genre', 'genero', 'gênero'))[:24]
    dv = _cfield(text, 'developer', 'desenvolvedor', 'produtora')[:40]
    pb = _cfield(text, 'publisher', 'publicadora', 'distribuidora', 'editora')[:40]
    ds = short_desc(_cfield(text, 'description', 'descricao', 'descrição', 'desc'), maxdesc)
    # nada de TAB dentro dos campos
    f = lambda s: s.replace('\t', ' ')
    return '%s\t%s\t%s\t%s\t%s\t%s' % (f(isobase), f(yr), f(gn), f(dv), f(ds), f(pb))


def find_dir(root, names, create):
    for d in os.listdir(root):
        if d.lower() in names and os.path.isdir(os.path.join(root, d)):
            return os.path.join(root, d)
    return os.path.join(root, create) if create is not None else None   # None = nao achou (nao quebra)


def local_images(d):
    out, outn = {}, {}
    if os.path.isdir(d):
        for f in os.listdir(d):
            b, e = os.path.splitext(f)
            if e.lower() in IMG_EXT and not f.startswith('._'):
                p = os.path.join(d, f)
                out.setdefault(b.lower(), p)
                outn.setdefault(norm(b), []).append((b, p))
    return out, outn


def local_find(exact, loose, isobase):
    p = exact.get(isobase.lower())
    if p:
        return p
    c = loose.get(norm(isobase))
    if c:
        return sorted(c, key=lambda bp: (region(bp[0]) != region(isobase), len(bp[0])))[0][1]
    return None


def local_videos(d):
    """Mapa dos videos-fonte (mp4/avi/...) por nome, igual ao local_images."""
    out, outn = {}, {}
    if os.path.isdir(d):
        for f in os.listdir(d):
            b, e = os.path.splitext(f)
            if e.lower() in VIDEO_EXT and not f.startswith('._'):
                p = os.path.join(d, f)
                out.setdefault(b.lower(), p)
                outn.setdefault(norm(b), []).append((b, p))
    return out, outn


# ================= IDENTIFICACAO / RENOMEACAO PELO .dat (Redump) =================
# Nomes de arquivo genericos que nao dizem nada / generic file names that say nothing
GENERIC = {'image', 'disc', 'disk', 'game', 'games', 'cdrom', 'cd', 'default',
           'untitled', 'dump', 'iso', 'rom', 'data', 'track', 'disco', 'jogo', '0', '00', '1', '01'}


def is_generic(b):
    s = b.strip().lower()
    if s in GENERIC:
        return True
    return re.fullmatch(r'(disc|disk|track|cd|game|disco|jogo)[ _\-]*\d*', s) is not None


def sanitize_name(name):
    # tira os caracteres proibidos em nome de arquivo no Windows
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name).strip().rstrip('. ')
    return name or 'jogo'


def file_crc(path):
    crc = 0
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            crc = zlib.crc32(chunk, crc)
    return format(crc & 0xffffffff, '08x')


def load_dat(root, txt_dir, midias=None):
    """Procura qualquer .dat na pasta das ISOs, na pasta de mídias e em txt/; {crc: nome do jogo}."""
    import xml.etree.ElementTree as ET
    paths = []
    dirs = [root, txt_dir] + ([midias] if midias and midias not in (root, txt_dir) else [])
    # Tambem procura o .dat numa subpasta gamelist/ (onde ele costuma ficar) / also look inside gamelist/
    for _base in (midias, root):
        if _base:
            _gl = find_dir(_base, {'gamelist', 'gamelists'}, None)
            if _gl and _gl not in dirs:
                dirs.append(_gl)
    for d in dirs:
        try:
            for f in sorted(os.listdir(d)):
                if f.lower().endswith('.dat'):
                    paths.append(os.path.join(d, f))
        except OSError:
            pass
    m = {}
    for p in paths:
        try:
            n = 0
            for g in ET.parse(p).getroot().iter('game'):
                nm = g.get('name')
                for r in g.findall('rom'):
                    c = (r.get('crc') or '').lower()
                    if c and nm:
                        m[c] = nm
                        n += 1
            if n:
                print('DAT: %d checksums de %s' % (n, os.path.basename(p)))
        except Exception as e:
            print('DAT ignorado (invalido):', os.path.basename(p), e)
    return m


def resolve_name(folder, isobase, ext, dat, idall, root, known_crc=None):
    """Nome correto: CRC do DAT (canonico) > nome da pasta (se generico) > nome atual.
       known_crc = CRC do .bin ja calculado (na conversao iso2bin) -> casa com o .dat sem recalcular."""
    # 1) CRC casando no .dat. Para .cue o CRC do Redump e o do .bin (NAO do .cue de texto).
    if dat and (idall or is_generic(isobase) or known_crc):
        try:
            crc = known_crc
            if crc is None:
                crc_path = os.path.join(folder, isobase + ext)
                if ext.lower() == '.cue':
                    _binp = os.path.join(folder, isobase + '.bin')
                    if os.path.isfile(_binp):
                        crc_path = _binp          # Usa o CRC do .bin, nao o do .cue
                crc = file_crc(crc_path)
            nm = dat.get(crc)
            if nm:
                return nm
        except OSError:
            pass
    # 2) nome generico -> usa o nome da PASTA
    if is_generic(isobase):
        parent = os.path.basename(folder.rstrip('/\\'))
        rootname = os.path.basename(os.path.abspath(root).rstrip('/\\'))
        if parent and parent.lower() != rootname.lower() and not is_generic(parent):
            return parent
    return isobase


def rename_game(folder, oldbase, ext, newname):
    """Renomeia o jogo (e, no caso de .cue, o .bin apontado + corrige o .cue).
       Renomeia tambem os arquivos irmaos (.png/_ss.png/.txt/.ode antigos)."""
    nb = sanitize_name(newname)
    if nb == oldbase:
        return None
    if os.path.exists(os.path.join(folder, nb + ext)):
        return None   # ja existe um com esse nome: nao mexe
    try:
        if ext.lower() == '.cue':
            cue = os.path.join(folder, oldbase + ext)
            data = open(cue, 'r', encoding='utf-8', errors='replace').read()

            def repl(mm):
                oldf = mm.group(2)
                _, be = os.path.splitext(oldf)
                bp = os.path.join(folder, oldf)
                if os.path.isfile(bp):
                    os.rename(bp, os.path.join(folder, nb + be))
                return mm.group(1) + nb + be + mm.group(3)
            data = re.sub(r'(FILE\s+")([^"]+)(")', repl, data)
            open(cue, 'w', encoding='utf-8', newline='\n').write(data)
            os.rename(cue, os.path.join(folder, nb + ext))
        else:
            os.rename(os.path.join(folder, oldbase + ext), os.path.join(folder, nb + ext))
        # arquivos irmaos com o nome antigo
        for suf in ('.png', '_ss.png', '_ss2.png', '.txt', '.ode'):
            cp = os.path.join(folder, oldbase + suf)
            if os.path.isfile(cp):
                os.rename(cp, os.path.join(folder, nb + suf))
        return nb
    except OSError as ex:
        print('  falha ao renomear / rename failed:', oldbase + ext, ex)
        return None


def flatten_folder(folder, isobase, ext, root):
    """Pasta com 1 jogo so: move o jogo (e irmaos) pro nivel de cima e apaga a pasta.
       Assim ele aparece no menu com a capa, sem pasta. Devolve a nova pasta."""
    folder = folder.rstrip('/\\')
    parent = os.path.dirname(folder)
    if not parent or os.path.abspath(folder) == os.path.abspath(root):
        return folder   # ja esta na raiz
    try:
        if any(os.path.isdir(os.path.join(folder, n)) for n in os.listdir(folder)):
            return folder   # tem subpasta: nao mexe
    except OSError:
        return folder
    if os.path.exists(os.path.join(parent, isobase + ext)):
        return folder   # ja existe um com esse nome la em cima
    try:
        for suf in (ext, '.cue', '.bin', '.png', '_ss.png', '_ss2.png', '.txt', '.ode'):
            sp = os.path.join(folder, isobase + suf)
            if os.path.isfile(sp):
                shutil.move(sp, os.path.join(parent, isobase + suf))
        if not os.listdir(folder):
            os.rmdir(folder)
        print('  tirado da pasta / unwrapped:', os.path.basename(folder), '->', isobase + ext)
        return parent
    except OSError as ex:
        print('  falha ao achatar / flatten failed:', folder, ex)
        return folder


# ============ PASTAS-LETRA (--organizar) ============
# No firmware de fabrica, abrir a janela do TOC na posicao N custa O(N) e cresce com o tamanho do
# diretorio: num cartao de 220 jogos na raiz, lancar um jogo do meio leva ~27 s. Em pastas de ~10
# jogos o custo some. --organizar move cada jogo da raiz para a pasta da sua 1a letra (A..Z, 0..9,
# "#") com todos os irmaos (.bin/.cue/.png/.txt) e reescreve o .cue: o firmware procura o
# .bin A PARTIR DA RAIZ, entao FILE "x.bin" vira FILE "L/x.bin". / letter folders: O(10) launch instead of O(220)
def letter_of(isobase):
    for ch in isobase:
        if ch.isalnum():
            u = ch.upper()
            if 'A' <= u <= 'Z': return u
            if '0' <= u <= '9': return '0'
            return '#'
    return '#'


def cue_bins(cue_path):
    """arquivos referenciados pelo .cue (FILE "x" BINARY) / files referenced by the cue"""
    out = []
    try:
        for ln in open(cue_path, 'r', encoding='utf-8', errors='replace'):
            m = re.match(r'\s*FILE\s+"([^"]+)"', ln, re.I)
            if m: out.append(m.group(1))
    except OSError:
        pass
    return out


def cue_rewrite(cue_path, letter, dry):
    """FILE "x.bin" -> FILE "L/x.bin" (so quando nao tem barra) / prefix bare FILE paths with the letter"""
    try:
        raw = open(cue_path, 'rb').read()
    except OSError:
        return False
    txt = raw.decode('utf-8', errors='replace')
    nl = '\r\n' if '\r\n' in txt else '\n'
    out, changed = [], False
    for ln in txt.splitlines():
        m = re.match(r'(\s*FILE\s+")([^"]+)(".*)$', ln, re.I)
        if m and '/' not in m.group(2) and '\\' not in m.group(2):
            ln = m.group(1) + letter + '/' + os.path.basename(m.group(2)) + m.group(3); changed = True
        out.append(ln)
    if changed and not dry:
        open(cue_path, 'w', encoding='utf-8', newline='').write(nl.join(out) + nl)
    return changed


def cue_strip(cue_path, dry=False):
    """FILE "L/x.bin" -> FILE "x.bin": tira o prefixo de pasta (usado no modo 'raiz') / strip folder prefix"""
    try:
        raw = open(cue_path, 'rb').read()
    except OSError:
        return False
    txt = raw.decode('utf-8', errors='replace')
    nl = '\r\n' if '\r\n' in txt else '\n'
    out, changed = [], False
    for ln in txt.splitlines():
        m = re.match(r'(\s*FILE\s+")([^"]+)(".*)$', ln, re.I)
        if m and ('/' in m.group(2) or '\\' in m.group(2)):
            ln = m.group(1) + os.path.basename(m.group(2).replace('\\', '/')) + m.group(3); changed = True
        out.append(ln)
    if changed and not dry:
        open(cue_path, 'w', encoding='utf-8', newline='').write(nl.join(out) + nl)
    return changed


def move_to_root(folder, isobase, ext, root, dry):
    """Modo 'raiz': move o jogo (e irmaos .bin/.cue/.png/.txt) da pasta pra RAIZ. Devolve a nova pasta."""
    folder = folder.rstrip('/\\')
    if os.path.abspath(folder) == os.path.abspath(root):
        return folder
    if os.path.exists(os.path.join(root, isobase + ext)):
        print('  ja existe na raiz, pulando / already at root:', isobase + ext)
        return folder
    moved = False
    for suf in (ext, '.cue', '.bin', '.png', '_ss.png', '_ss2.png', '.txt'):
        sp = os.path.join(folder, isobase + suf)
        if os.path.isfile(sp):
            if dry:
                print('  [teste] moveria p/ raiz / would move to root:', os.path.relpath(sp, root))
            else:
                shutil.move(sp, os.path.join(root, isobase + suf)); moved = True
    if moved:
        print('  movido p/ raiz / moved to root:', isobase + ext)
    return root if (moved or dry) else folder


def cleanup_empty_dirs(root, dry=False):
    """Apaga subpastas da raiz que ficaram VAZIAS (modo 'raiz', depois de mover tudo). / remove empty subdirs"""
    n = 0
    try:
        entries = list(os.listdir(root))
    except OSError:
        return 0
    for d in entries:
        p = os.path.join(root, d)
        if not os.path.isdir(p):
            continue
        try:
            rest = os.listdir(p)
        except OSError:
            continue
        # ignora restos invisiveis do sistema / ignore hidden system leftovers
        if all(x in ('Thumbs.db', '.DS_Store') or x.startswith('._') for x in rest):
            if dry:
                print('  [teste] apagaria pasta vazia / would remove empty folder:', d)
            else:
                try:
                    for x in rest: os.remove(os.path.join(p, x))
                    os.rmdir(p); n += 1
                    print('  pasta vazia apagada / removed empty folder:', d)
                except OSError:
                    pass
    return n


ORG_DIRS = set()   # pastas-letra conhecidas / known flattened folders


def org_folder_name(mode, isobase, genre):
    """nome da pasta de destino: letra (A..Z/0/#) ou genero ("Outros" sem genero) / target folder name"""
    return letter_of(isobase)


def organize_game(folder, isobase, ext, root, dry, mode='letra', genre=''):
    """move o jogo da raiz p/ a pasta (letra ou genero) e ajusta o .cue; devolve a pasta final / move + fix cue"""
    if os.path.abspath(folder) != os.path.abspath(root):
        return folder
    letter = org_folder_name(mode, isobase, genre)
    ORG_DIRS.add(letter.lower())
    dest = os.path.join(root, letter)
    files = [isobase + suf for suf in (ext, '.bin', '.png', '_ss.png', '_ss2.png', '.txt')]
    if ext.lower() == '.cue':
        files += cue_bins(os.path.join(folder, isobase + ext))
    files = [f for f in dict.fromkeys(files) if os.path.isfile(os.path.join(folder, f))]
    if dry:
        print('  [teste] moveria / would move:', isobase + ext, '->', letter + '/'); return folder
    try:
        os.makedirs(dest, exist_ok=True)
        for f in files:
            if not os.path.exists(os.path.join(dest, f)):
                shutil.move(os.path.join(folder, f), os.path.join(dest, f))
        if ext.lower() == '.cue':
            cue_rewrite(os.path.join(dest, isobase + ext), letter, False)
        print('  organizado / moved:', isobase + ext, '->', letter + '/')
        return dest
    except OSError as ex:
        print('  falha ao organizar / move failed:', isobase, ex)
        return folder


def is_letter_dir(folder, root):
    """Pasta-letra: nome de 1 caractere na raiz, ou pasta criada pelo --organizar."""
    b = os.path.basename(folder.rstrip('/\\'))
    if os.path.abspath(os.path.dirname(folder.rstrip('/\\'))) != os.path.abspath(root) or b == '.':
        return False
    return len(b) == 1 or b.lower() in ORG_DIRS


# ============ COPIA DO BOOT ============
def find_boot_iso(root, midias=None, explicit=None):
    """acha um boot.iso p/ copiar (caminho informado, ao lado do script, repo boot/, midias, raiz). / locate boot.iso"""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = []
    if explicit:
        cands += [explicit, os.path.join(explicit, 'boot.iso')]
    for base in (here, os.path.join(here, '..'), midias, root):
        if base:
            cands += [os.path.join(base, 'boot.iso'), os.path.join(base, 'boot', 'boot.iso')]
    seen = set()
    for c in cands:
        try:
            cp = os.path.abspath(c)
        except Exception:
            continue
        if cp in seen:
            continue
        seen.add(cp)
        if os.path.isfile(cp):
            return cp
    return None


BOOT_URLS = ['https://raw.githubusercontent.com/cyberrep/3doode/main/boot/boot.iso',
             'https://raw.githubusercontent.com/cyberrep/3doode/master/boot/boot.iso',
             'https://github.com/cyberrep/3doode/releases/latest/download/boot.iso']

def download_boot_iso(dest_path):
    """baixa o boot.iso (o menu) do repo p/ dest_path. retorna o caminho ou None. / download boot.iso."""
    import urllib.request
    for url in BOOT_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=120).read()
            if data and len(data) > 100000:        # boot.iso tem alguns MB
                with open(dest_path, 'wb') as f:
                    f.write(data)
                return dest_path
        except Exception:
            continue
    return None


def copy_boot_to(root, src):
    """copia o boot.iso p/ a raiz do cartao. retorna (destino, copiou?) / copy boot.iso to card root"""
    dst = os.path.join(root, 'boot.iso')
    if os.path.abspath(src) == os.path.abspath(dst):
        return dst, False                 # ja esta la / already there
    shutil.copy2(src, dst)
    return dst, True


# ---- CHD -> .bin/.cue (via chdman, a ferramenta oficial; lossless, bate os hashes do dump) ----
def find_chdman():
    """acha o chdman no PATH, ao lado do script, ou numa pasta tools/. / locate chdman."""
    import shutil as _sh
    w = _sh.which('chdman') or _sh.which('chdman.exe')
    if w:
        return w
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (here, os.path.join(here, 'tools'), os.path.join(here, '..')):
        for nm in ('chdman.exe', 'chdman'):
            p = os.path.join(base, nm)
            if os.path.isfile(p):
                return p
    return None


def chd_extract(chd_path, chdman):
    """roda 'chdman extractcd' -> <base>.bin + <base>.cue (sem perda). Retorna (bin, cue) ou lanca. / extract CHD."""
    import subprocess
    base = os.path.splitext(chd_path)[0]
    cue, binf = base + '.cue', base + '.bin'
    r = subprocess.run([chdman, 'extractcd', '-i', chd_path, '-o', cue, '-ob', binf],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        tail = (r.stdout.decode('utf-8', 'ignore')[-200:] if r.stdout else '?')
        raise RuntimeError('chdman falhou: ' + tail)
    return binf, cue


def rename_only(root, midias=None):
    """SO RENOMEIA os jogos pelo .dat (Redump): confere o CRC de cada .bin (ou .iso) e poe o nome oficial.
       NAO gera capas/gamelist/videos - rapido, aponta direto p/ a pasta. / rename-only pass (CRC vs .dat)."""
    midias = os.path.abspath(midias) if midias else root
    txt_dir = find_dir(midias, {'txt', 'info'}, 'txt')
    dat = load_dat(root, txt_dir, midias)
    if not dat:
        print('Nenhum .dat (Redump) encontrado (procurei na pasta dos jogos, nas midias e em gamelist/).')
        return
    games = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d.lower() not in SKIP_DIRS and not d.startswith('.')]
        for f in sorted(fn):
            b, e = os.path.splitext(f); el = e.lower()
            if el not in ('.iso', '.cue', '.bin') or 'boot' in f.lower():
                continue
            if el == '.bin' and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.cue', '.CUE')):
                continue
            if el == '.iso' and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.bin', '.BIN')):
                continue
            if el == '.cue' and not any(os.path.exists(os.path.join(dp, b + x)) for x in ('.bin', '.BIN')) \
                    and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.iso', '.ISO')):
                continue
            games.append((dp, b, e))
    print('%d jogo(s); conferindo o CRC de cada um no .dat... / checking CRC vs .dat' % len(games))
    nren = 0
    for folder, b, e in games:
        sys.stdout.write('\r  %-48s' % (b[:46] + '..' if len(b) > 46 else b)); sys.stdout.flush()
        new = resolve_name(folder, b, e, dat, True, root)      # idall=True: confere TODOS pelo CRC
        if new != b:
            nb = rename_game(folder, b, e, new)
            if nb:
                print('\r  %s%s  ->  %s%s' % (b, e, nb, e))
                nren += 1
    print('\nPronto: %d renomeado(s) de %d jogo(s). / %d renamed.' % (nren, len(games), nren))


def main(root, dry, force, offline, report_on, rename=True, idall=False, flatten=True, midias=None,
         video=True, vfps=15, vseg=10, onlyvideo=False, vtam='small', organize=False,
         iso2bin=False, iso2bin_delete=False, lang=None, vmissing=False, redown=False, boot=None,
         no_covers=False, gen_list=True, chd=True, chd_delete=False, vq=4,
         do_cov=True, do_sht=True, cov_missing=False, sht_missing=False,
         cov_force=False, sht_force=False, vid_force=False):
    # no_covers: gera so os textos (3dogamesdetails.ode), sem capas, telas nem videos.
    # gen_list:  gera o .config/3dogamesdetails.ode (os textos dos jogos).
    # boot:      caminho do boot.iso a copiar para a raiz do cartao (None = nao copia).
    # vmissing:  gera video so para quem ainda nao tem.
    # organize:  False/'' = nao mexe; 'raiz' = tudo na raiz; 'letra' = pastas A..Z.
    ORG_DIRS.clear()
    if no_covers:
        offline = True; video = False    # so os textos: sem rede, sem capas, telas nem videos
    root = os.path.abspath(root)
    # pasta com cover/screenshots/gamelist; pode ser separada da pasta das ISOs (--midias)
    # folder with cover/screenshots/gamelist; can be separate from the ISO folder (--midias)
    midias = os.path.abspath(midias) if midias else root
    cover_dir = find_dir(midias, {'cover', 'covers', 'capa', 'capas'}, 'cover')
    shot_dir = find_dir(midias, {'screenshot', 'screenshots', 'tela', 'telas'}, 'screenshot')
    video_dir = find_dir(midias, {'video', 'videos'}, 'video')
    txt_dir = find_dir(midias, {'txt', 'info'}, 'txt')
    cov_x, cov_l = local_images(cover_dir)
    sht_x, sht_l = local_images(shot_dir)
    vid_x, vid_l = local_videos(video_dir)
    # --idioma xx: gamelist.xx.txt tem prioridade; senao gamelist.pt.txt, depois gamelist.txt / text language
    # procura o gamelist em VARIAS pastas: raiz da midia, txt/, gamelist/ e a pasta dos jogos.
    _gl_dirs = [midias, txt_dir, find_dir(midias, {'gamelist', 'gamelists'}, 'gamelist'), root]
    _gl_dirs = [d for d in dict.fromkeys(_gl_dirs) if d and os.path.isdir(d)]
    _gl_names = (['gamelist.%s.txt' % lang] if lang else []) + ['gamelist.pt.txt', 'gamelist.txt']
    gl_paths = [os.path.join(d, n) for n in _gl_names for d in _gl_dirs]
    # O gamelist.pt.txt tambem e procurado na pasta txt/, mesmo sem --idioma.
    # / also look for gamelist.pt.txt inside txt/ without --idioma
    gamelist = load_gamelist(gl_paths)
    xml_paths = [os.path.join(d, n) for d in (midias, txt_dir) for n in ('gamelist.xml', '3do-gamelist.xml')]
    if midias != root:
        print(f'ISOs            : {root}')
        print(f'Midias/gamelist : {midias}')
        print(f'  cover={os.path.basename(cover_dir)}  screenshots={os.path.basename(shot_dir)}  ({len(cov_x)+len(cov_l)} capas, {len(sht_x)+len(sht_l)} telas locais)')
    gamexml = load_gamelist_xml(xml_paths)
    if gamexml:
        print(f'gamelist.xml: {len(gamexml)} nomes / names')

    # 1) AS ISOS QUE VOCE TEM / THE ISOS YOU HAVE
    games = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d.lower() not in SKIP_DIRS and not d.startswith('.')]
        for f in sorted(fn):
            b, e = os.path.splitext(f)
            if e.lower() not in GAME_EXT or 'boot' in f.lower():
                continue
            el = e.lower()
            # Dedup do mesmo jogo em varias extensoes (evita listar GEX 2x: .iso + .cue orfao)
            if el == '.bin' and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.cue', '.CUE')):
                continue                                  # o .cue ja representa este .bin
            if el == '.iso' and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.bin', '.BIN')):
                continue                                  # ja convertido (tem .bin) -> ignora o .iso
            if el == '.cue' and not any(os.path.exists(os.path.join(dp, b + x)) for x in ('.bin', '.BIN')) \
                    and any(os.path.exists(os.path.join(dp, b + x)) for x in ('.iso', '.ISO')):
                continue                                  # .cue ORFAO (sem .bin) + ha .iso -> usa o .iso, ignora o .cue
            games.append((dp, b, e))
    print(f'{len(games)} jogos encontrados / games found')
    conv_crc = {}   # CRC do .bin calculado na conversao iso2bin -> casa com o .dat (Redump) sem recalcular

    # 0) ISO -> BIN/CUE (estilo Redump: setores 2352 com EDC/ECC reconstruidos; tamanho e CRC batem com o .dat)
    # CHD -> .bin/.cue (via chdman): o leitor do 3DO NAO le .chd, entao convertemos antes. / CHD must be converted
    if chd and not dry:
        chds = []
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d.lower() not in SKIP_DIRS and not d.startswith('.')]
            for f in fn:
                if f.lower().endswith('.chd') and not f.startswith('._'):
                    chds.append((dp, os.path.splitext(f)[0]))
        if chds:
            chdman = find_chdman()
            if not chdman:
                print('  CHD: achei %d arquivo(s) .chd, mas o chdman nao foi encontrado - pulando.' % len(chds))
                print('       Baixe o chdman (vem com o MAME) e ponha no PATH ou numa pasta tools/ ao lado do script:')
                print('       https://www.mamedev.org/release.html')
            else:
                for folder, b in chds:
                    chdp = os.path.join(folder, b + '.chd')
                    cue = os.path.join(folder, b + '.cue')
                    try:
                        if os.path.exists(cue) or os.path.exists(os.path.join(folder, b + '.bin')):
                            print('  CHD: %s ja convertido (.bin/.cue existe) - pulando' % b)
                        else:
                            print('  convertendo CHD: %s.chd ... / converting' % b)
                            chd_extract(chdp, chdman)
                            print('  convertido / converted: %s.chd -> %s.bin/.cue' % (b, b))
                            if is_letter_dir(folder, root):     # pasta-letra: o .cue precisa do prefixo "L/"
                                cue_rewrite(cue, os.path.basename(folder), False)
                            if chd_delete:
                                os.remove(chdp); print('    .chd apagado / removed')
                        if not any(g[0] == folder and g[1] == b for g in games):
                            games.append((folder, b, '.cue'))
                    except Exception as ex:
                        print('  %s.chd: nao convertido (%s)' % (b, ex))

    if iso2bin and not dry:
        try:
            import iso2bincue
        except ImportError:
            iso2bincue = None
        if iso2bincue is None or iso2bincue.np is None:
            print('  --iso2bin precisa do numpy:  py -m pip install numpy   (pulando a conversao)')
        else:
            newgames = []
            for folder, b, e in games:
                if e.lower() != '.iso':
                    newgames.append((folder, b, e)); continue
                src = os.path.join(folder, b + e)
                def prog(d, n, _b=b):
                    sys.stdout.write('\r  convertendo %s  %d%%' % (_b + '.iso', d * 100 // n)); sys.stdout.flush()
                try:
                    binp, crc, n = iso2bincue.convert(src, False, prog)
                    conv_crc[(folder, b)] = crc        # Guarda o CRC do .bin p/ casar com o .dat (Redump)
                    print('\r  convertido / converted: %s -> %s.bin/.cue  (%d setores, CRC %s)' % (b + e, b, n, crc))
                    if is_letter_dir(folder, root):   # dentro de pasta-letra o FILE precisa do "L/" / letter-folder prefix
                        cue_rewrite(os.path.join(folder, b + '.cue'), os.path.basename(folder), False)
                    if iso2bin_delete:
                        os.remove(src); print('    .iso apagado / removed')
                    newgames.append((folder, b, '.cue'))
                except Exception as ex:
                    print('\r  %s: nao convertido (%s)' % (b + e, ex)); newgames.append((folder, b, e))
            games = newgames

    # DAT (Redump) na pasta -> renomeia pelo CRC / nome da pasta
    dat = load_dat(root, txt_dir, midias) if rename else {}
    # quantos jogos por pasta (p/ achatar as pastas de 1 jogo so) / games per folder (to flatten 1-game folders)
    fcount = {}
    for fo, _, _ in games:
        fcount[fo] = fcount.get(fo, 0) + 1
    processed = []   # (folder, isobase, ext) final de cada jogo / final per-game info

    idx = None
    if not offline:
        names, src = remote_names()
        idx = index_remote(names)
        print(f'Imagens do libretro: {len(names)} ({src})')

    made = skipped = dl = vmade = 0
    # Tamanho do video: mini 80x60 | box 128x96 | small 160x120 | medium 240x180 | large 320x240
    vconv.VID_W, vconv.VID_H = {'mini': (80, 60), 'box': (128, 96), 'small': (160, 120), 'medium': (240, 180), 'large': (320, 240)}.get(vtam, (160, 120))
    vconv.CVD_Q = vq
    do_video = video and vconv is not None and vconv.ffmpeg_ok() and (len(vid_x) + len(vid_l) > 0)
    if do_video and not vconv.cinepak_ok():
        print('  (este ffmpeg nao tem o codificador Cinepak: pulando os videos / ffmpeg without cinepak: skipping)')
        do_video = False
    if do_video:
        print('Video Cinepak (.cvd): %s %dx%d, %d fps, %gs, qualidade %d%s' % (vtam, vconv.VID_W, vconv.VID_H, vfps, vseg, vq,
                                                  ' (so video / video only)' if onlyvideo else ''))
    if video and (len(vid_x) + len(vid_l) > 0) and not do_video:
        print('  (videos encontrados mas ffmpeg indisponivel: pulando os videos / ffmpeg missing: skipping videos)')
    # VIDEOS EM PARALELO: o codificador Cinepak usa 1 nucleo so; aqui vai um ffmpeg por nucleo do PC.
    # Os videos entram na fila durante a passada pelos jogos e sao esperados no fim. / one ffmpeg per CPU core
    import concurrent.futures as _cf
    _vworkers = max(1, (os.cpu_count() or 2) - 1)
    _vpool = _cf.ThreadPoolExecutor(max_workers=_vworkers) if do_video and not dry else None
    _vfut = []
    _vfps, _vseg, _vW, _vH = vfps, vseg, vconv.VID_W, vconv.VID_H

    def _vjob(vsrc, vout):
        frames = vconv.encode_cinepak(vsrc, _vW, _vH, _vfps, _vseg, 0)
        if not frames:
            return None
        data = vconv.build_cvd(frames, _vW, _vH, _vfps)
        with open(vout, 'wb') as fh:
            fh.write(data)
        return (len(frames), len(data) / 1024, len(data) / 1024 * _vfps / len(frames))
    if _vpool:
        print('  (convertendo %d video(s) ao mesmo tempo / %d at a time)' % (_vworkers, _vworkers))
    report = []
    miss_cov, miss_sht, miss_vid = [], [], []   # listas do que falta p/ voce cacar / missing-media lists
    # PROJETO NOVO: saida em pastas separadas (OAR8) + 1 arquivo de textos
    covers_out = os.path.join(root, 'covers')
    shots_out = os.path.join(root, 'screenshots')
    videos_out = os.path.join(root, 'videos')
    covers_small, covers_large = os.path.join(covers_out, 'small'), os.path.join(covers_out, 'large')
    shots_medium, shots_large = os.path.join(shots_out, 'medium'), os.path.join(shots_out, 'large')
    if not dry:
        for _d in (covers_out, shots_out, videos_out, covers_small, covers_large, shots_medium, shots_large):
            os.makedirs(_d, exist_ok=True)
    details = []   # linhas do 3dogamesdetails.ode
    ncov = nsht = 0
    # TAMANHO/PREPARO DAS CAPAS: se mudou desde a ultima vez, refaz todas as capas (e as telas, se o
    # preparo mudou). SEM arquivo de controle no cartao: o tamanho sai do cabecalho de uma capa que ja
    # esta em covers/, e o preparo usado fica no generate_usb.ini (feito_preparo).
    _old_size = cel_existing_size(covers_large)
    _old_prep = _ini_load().get('feito_preparo', 'texto')   # sem registro = imagens antigas: refaz uma vez
    redo_cov = (_old_size is not None and _old_size != CEL_COVER_BOX) or _old_prep != CEL_PRESET
    redo_sht = _old_prep != CEL_PRESET
    print('Capas  : %s %dx%d em covers/large + %dx%d em covers/small, preparo %s%s' % (
          (CEL_COVER_SIZE.upper(),) + CEL_COVER_BOX + CEL_COVER_SMALL + (CEL_PRESET.upper(), ' (mudou: refazendo todas)' if redo_cov else '',)))
    for folder, isobase, ext in games:
        # IDENTIFICA/RENOMEIA: CRC do DAT > nome da pasta > nome atual
        if rename:
            newname = resolve_name(folder, isobase, ext, dat, idall, root,
                                   known_crc=conv_crc.get((folder, isobase)))
            if newname != isobase:
                if dry:
                    print('  [teste] renomearia / would rename:', isobase + ext, '->', sanitize_name(newname) + ext)
                    isobase = sanitize_name(newname)
                else:
                    nb = rename_game(folder, isobase, ext, newname)
                    if nb:
                        print('  renomeado / renamed:', isobase + ext, '->', nb + ext)
                        isobase = nb
        # --organizar letra: jogo solto na raiz vai p/ a pasta da 1a letra (pastas pequenas = jogo abre
        # rapido no firmware de fabrica). / letter folders
        if organize == 'letra':
            if fcount.get(folder, 0) == 1 and os.path.abspath(folder) != os.path.abspath(root) and flatten and not dry:
                folder = flatten_folder(folder, isobase, ext, root)   # tira da pasta de 1 jogo antes / unwrap first
            folder = organize_game(folder, isobase, ext, root, dry, 'letra', '')
            if is_letter_dir(folder, root) and ext.lower() == '.cue':
                cue_rewrite(os.path.join(folder, isobase + ext), os.path.basename(folder), dry)   # garante o "L/" / ensure prefix
        elif organize == 'raiz':
            # DEIXAR TUDO NO RAIZ: move o jogo (e irmaos) pra raiz e tira o prefixo do .cue. Pastas vazias
            # sao apagadas no fim (cleanup_empty_dirs). / move everything back to root, strip cue prefix
            folder = move_to_root(folder, isobase, ext, root, dry)
            if ext.lower() == '.cue' and not dry:
                cue_strip(os.path.join(folder, isobase + ext))   # FILE "L/x.bin" -> FILE "x.bin"
        processed.append((folder, isobase, ext))
        # DISCO 2+: nao gera capa/tela/video/detalhe (esse jogo fica ESCONDIDO no menu; o disco 1 toca todos)
        # DISC 2+: no cover/screenshot/video/details (hidden in the menu; disc 1 queues them all)
        if disc_num(isobase) >= 2:
            print('  disco 2+ (sem midia / no media):', isobase)
            continue
        # --so-video: so converte o video, sem baixar capa/tela nem mexer nos textos
        # --so-video: only convert the video, no cover/screenshot downloads, no text rewrite
        if onlyvideo:
            if do_video:
                vsrc = local_find(vid_x, vid_l, isobase)
                if vsrc:
                    vout = os.path.join(videos_out, isobase + '.cvd')
                    if (not os.path.exists(vout)) or (not vmissing and (force or vid_force or os.path.getmtime(vout) < os.path.getmtime(vsrc))):
                        if dry:
                            print('  [teste] video:', os.path.relpath(vout, root))
                        else:
                            _vfut.append((isobase, vout, _vpool.submit(_vjob, vsrc, vout)))
                            print('  video na fila / queued:', isobase)
            continue
        rel = os.path.relpath(os.path.join(folder, isobase), root)
        # --somente-lista (no_covers) pula capas/telas/videos; so monta o texto (details + genero)
        cover = None if no_covers else local_find(cov_x, cov_l, isobase)
        shot = None if no_covers else local_find(sht_x, sht_l, isobase)
        src_c = 'sua' if cover else '-'
        src_s = 'sua' if shot else '-'
        # 2) BAIXA SO O QUE FALTA / DOWNLOADS ONLY WHAT IS MISSING
        if not no_covers and idx is not None:
            for kind, folder_r, ddir in (('cover', 'Named_Boxarts', cover_dir), ('shot', 'Named_Snaps', shot_dir)):
                if not redown and ((kind == 'cover' and cover) or (kind == 'shot' and shot)):
                    continue
                if (kind == 'cover' and not do_cov) or (kind == 'shot' and not do_sht):
                    continue      # este tipo nao vai ser gerado: nao baixa / type switched off
                rb = find_remote(idx, folder_r, isobase)
                if not rb:
                    continue
                dest = os.path.join(ddir, isobase + '.png')
                if dry:
                    print('  [teste] baixar / download:', folder_r + '/' + rb + '.png')
                    continue
                try:
                    download(folder_r, rb, dest)
                    dl += 1
                    if kind == 'cover': cover, src_c = dest, 'baixada'
                    else: shot, src_s = dest, 'baixada'
                except Exception as ex:
                    print('  falha ao baixar / download failed:', rb, ex)
        # 3) TEXTO / TEXT
        txt = None
        for cand in (os.path.join(folder, isobase + '.txt'), os.path.join(txt_dir, isobase + '.txt')):
            if os.path.isfile(cand):
                txt = cand; break
        text, src_t = '', '-'
        if txt:
            text, src_t = read_txt(txt), 'txt'
        elif find_text(gamelist, isobase):
            text, src_t = find_text(gamelist, isobase), 'gamelist'
        xf = gamexml.get(norm(isobase)) or (find_text(gamexml, isobase) if gamexml else None)
        if xf:
            text = merge_xml(text, xf)
            if src_t == '-': src_t = 'xml'
        if not re.search(r'^\s*(name|nome|title|titulo)\s*[=:]', text, re.I | re.M):
            text = f'Name={pretty(isobase)}\n' + text
        mg = re.search(r'^\s*(genero|g[eê]nero|genre)\s*[=:]\s*(.+)$', text, re.I | re.M)
        gv = mg.group(2).strip() if mg else ''
        if gv:
            pass
        src_v = 'sua' if local_find(vid_x, vid_l, isobase) else '-'
        # O relatorio tambem diz se falta ANO / GENERO / DESCRICAO no texto do jogo
        has_year = bool(re.search(r'^\s*(year|ano)\s*[=:]\s*\S', text, re.I | re.M))
        has_desc = bool(re.search(r'^\s*(description|descri[cç][aã]o|desc)\s*[=:]\s*\S', text, re.I | re.M))
        report.append((rel, src_c, src_s, src_v, src_t, bool(gv), has_year, has_desc))
        # LISTAS DO QUE FALTA (p/ voce cacar depois) / missing-media lists to hunt later
        if not cover: miss_cov.append(rel)
        if not shot: miss_sht.append(rel)
        if not local_find(vid_x, vid_l, isobase): miss_vid.append(rel)
        # 4) VIDEO: videos/<jogo>.cvd, convertido do video-fonte da pasta de midias.
        if not no_covers and video and do_video:
            vout = os.path.join(videos_out, isobase + '.cvd')
            if do_video:
                vsrc = local_find(vid_x, vid_l, isobase)
                if vsrc:
                    # --video-faltantes (vmissing): gera so o video de quem ainda nao tem
                    if (not os.path.exists(vout)) or (not vmissing and (force or vid_force or os.path.getmtime(vout) < os.path.getmtime(vsrc))):
                        if dry:
                            print('  [teste] video / would convert:', os.path.relpath(vout, root))
                        else:
                            _vfut.append((isobase, vout, _vpool.submit(_vjob, vsrc, vout)))
        if cover and not _img_ok(cover):
            print('  capa invalida, ignorada / bad cover skipped:', os.path.relpath(cover, root)); cover = None; src_c = '-'
        if shot and not _img_ok(shot):
            print('  tela invalida, ignorada / bad screenshot skipped:', os.path.relpath(shot, root)); shot = None; src_s = '-'
        # 1 linha de texto no 3dogamesdetails.ode; capa e tela em arquivos CEL separados.
        dl_line = detail_line(isobase, text, gv)
        has_meta = dl_line.split('\t', 1)[1].replace('\t', '').strip() != ''
        if not cover and not shot and not has_meta:
            continue   # nada util pra esse jogo / nothing useful for this game
        details.append(dl_line)
        if dry:
            print('  [teste] detalhes + CEL:', rel)
        else:
            # CEL: covers/ e screenshots/, sempre na raiz do cartao.
            # Refaz so se a imagem for mais nova que o CEL (ou --forcar).
            if cover:
                cout = os.path.join(covers_large, isobase + CEL_EXT_COVER)
                csml = os.path.join(covers_small, isobase + CEL_EXT_COVER)
                # do_cov = gerar capas; cov_missing = so as que ainda nao existem no cartao
                _redo = force or cov_force or redo_cov
                for _out, _box in ((cout, CEL_COVER_BOX), (csml, CEL_COVER_SMALL)):
                    if do_cov and (not os.path.exists(_out) or (not cov_missing and (_redo or os.path.getmtime(_out) < os.path.getmtime(cover)))):
                        try:
                            data, cw, ch = cel_image(cover, _box, fill=True)
                            open(_out, 'wb').write(data); ncov += 1
                            print('  capa / cover:', os.path.relpath(_out, root), '%dx%d' % (cw, ch))
                        except Exception as ex:
                            print('  ERRO capa / cover error:', isobase, str(ex)[:60])
            if shot:
                smed = os.path.join(shots_medium, isobase + CEL_EXT_SHOT)
                slrg = os.path.join(shots_large, isobase + CEL_EXT_SHOT)
                # do_sht = gerar telas; sht_missing = so as que ainda nao existem no cartao
                _redo = force or sht_force or redo_sht
                for _out, _box in ((smed, CEL_SHOT_MEDIUM), (slrg, CEL_SHOT_LARGE)):
                    if do_sht and (not os.path.exists(_out) or (not sht_missing and (_redo or os.path.getmtime(_out) < os.path.getmtime(shot)))):
                        try:
                            data, sw, sh = cel_image(shot, _box)
                            open(_out, 'wb').write(data); nsht += 1
                            print('  tela / shot:', os.path.relpath(_out, root), '%dx%d' % (sw, sh))
                        except Exception as ex:
                            print('  ERRO tela / shot error:', isobase, str(ex)[:60])
        made += 1
    if not dry and os.path.isdir(covers_out):
        _d = _ini_load()                      # lembra o preparo usado (o tamanho fica nas proprias capas)
        if _d.get('feito_preparo') != CEL_PRESET:
            _d['feito_preparo'] = CEL_PRESET
            _ini_save(_d)

    # ACHATA PASTAS COM 1 JOGO SO: tira o jogo da pasta p/ ele aparecer com a capa no menu
    # FLATTEN 1-GAME FOLDERS: pull the game out so it shows with its cover in the menu
    if flatten and not dry:
        for folder, isobase, ext in processed:
            if fcount.get(folder, 0) == 1 and os.path.abspath(folder) != os.path.abspath(root) and not is_letter_dir(folder, root):
                flatten_folder(folder, isobase, ext, root)   # (pastas-letra nunca sao achatadas / letter folders are never flattened)

    # Grava o .config/3dogamesdetails.ode (os textos de todos os jogos; o boot le uma vez ao ligar).
    # Grava sempre, mesmo sem dados de nenhum jogo, para a pasta .config existir.
    if not dry and gen_list:
        details.sort(key=lambda l: l.split('\t', 1)[0].lower())
        body = '#3DOGAMES2\ttotal=%d\n' % len(details) + '\n'.join(details) + '\n# fim\n'
        try:
            # Os arquivos que o boot le ficam na pasta .config do cartao.
            os.makedirs(os.path.join(root, '.config'), exist_ok=True)
            open(os.path.join(root, '.config', '3dogamesdetails.ode'), 'w', encoding='utf-8').write(body)
            nmeta = sum(1 for l in details if l.split('\t', 1)[1].replace('\t', '').strip())
            print('3dogamesdetails.ode: %d jogos (%d com dados), %d capas .cel, %d telas .cel, %d bytes'
                  % (len(details), nmeta, ncov, nsht, len(body.encode('utf-8'))))
        except Exception as ex:
            print('  ERRO 3dogamesdetails.ode:', str(ex)[:80])

    lines = ['COVER.TXT - gerado por generate_usb.py', '',
             'capa/tela/video: sua = da sua pasta, baixada = do libretro, - = nao tem',
             'texto: txt = txt/Jogo.txt, gamelist = gamelist.txt, xml = gamelist.xml, - = so o nome', '',
             'ano/genero/desc: ok = tem, FALTA = nao tem', '',
             'Jogo (nome da ISO)'.ljust(60) + 'capa'.ljust(7) + 'tela'.ljust(7) + 'video'.ljust(7) +
             'texto'.ljust(10) + 'ano'.ljust(7) + 'genero'.ljust(8) + 'desc', '-' * 110]
    for rel, c, s, v, t, hg, hy, hd in report:
        lines.append(rel.ljust(60) + c.ljust(7) + s.ljust(7) + v.ljust(7) + t.ljust(10) +
                     ('ok' if hy else 'FALTA').ljust(7) + ('ok' if hg else 'FALTA').ljust(8) +
                     ('ok' if hd else 'FALTA'))
    sem = [r[0] for r in report if r[1] == '-']
    if sem:
        lines += ['', 'Sem capa (coloque uma imagem com o MESMO nome em cover/):', '-' * 100] + sem
    # Resumo do que falta de metadata (ano/genero/descricao)
    for what, idx in (('ano', 6), ('genero', 5), ('descricao', 7)):
        falta = [r[0] for r in report if not r[idx]]
        if falta:
            lines += ['', 'Sem %s (%d):' % (what, len(falta)), '-' * 100] + falta
    if report_on and not dry:
        open(os.path.join(root, 'cover.txt'), 'w', encoding='utf-8-sig', newline='\r\n').write('\n'.join(lines) + '\n')
    # LISTAS DO QUE FALTA (missing_cover/screenshot/video.txt na pasta de midias) p/ voce cacar
    # MISSING-MEDIA LISTS in the midias folder, so you can go hunt what's missing
    if not dry:
        for fn, lst, what in (('missing_cover.txt', miss_cov, 'capa'),
                              ('missing_screenshot.txt', miss_sht, 'screenshot'),
                              ('missing_video.txt', miss_vid, 'video')):
            p = os.path.join(midias, fn)
            if lst:
                open(p, 'w', encoding='utf-8-sig', newline='\r\n').write(
                    '# %d jogo(s) sem %s (nomeie o arquivo igual ao jogo):\r\n' % (len(lst), what) +
                    '\r\n'.join(sorted(lst)) + '\r\n')
            elif os.path.isfile(p):
                os.remove(p)   # nada faltando: remove a lista antiga / nothing missing: drop stale list
    # MODO 'raiz': depois de mover tudo pra raiz, apaga as pastas que ficaram vazias / remove now-empty folders
    if organize == 'raiz':
        rm = cleanup_empty_dirs(root, dry)
        if rm: print('Pastas vazias removidas / empty folders removed: %d' % rm)
    # Espera os videos que ficaram convertendo. / wait for the queued video conversions
    if _vfut:
        print('Convertendo %d video(s), %d de cada vez; cada um aparece quando termina... / converting' % (len(_vfut), _vworkers))
        _vby = {_f: (_nm, _vo) for _nm, _vo, _f in _vfut}
        for _k, _f in enumerate(_cf.as_completed(list(_vby)), 1):
            _nm, _vo = _vby[_f]
            try:
                _r = _f.result()
                if _r:
                    vmade += 1
                    print('  video %d/%d: %s (%d quadros, %.0f KB, %.0f KB/s)' % (_k, len(_vfut), os.path.relpath(_vo, root), _r[0], _r[1], _r[2]))
                else:
                    print('  video %d/%d: %s sem quadros (video vazio?)' % (_k, len(_vfut), _nm))
            except Exception as ex:
                print('  ERRO video %d/%d: %s %s' % (_k, len(_vfut), _nm, str(ex)[:80]))
    if _vpool:
        _vpool.shutdown()
    # CONFIG DO BOOT: se o cartao ainda nao tem .config/3doconfig.ode, cria so com o idioma escolhido, do
    # jeito que o boot le (chave=valor entre #3DOREBORN-CONFIG# e #END#). Se ja existe, nao mexe.
    _cfgp = os.path.join(root, '.config', '3doconfig.ode')
    if not os.path.exists(_cfgp):
        _lv = {'pt': 'Português', 'es': 'Español', 'en': 'English'}.get((lang or 'pt')[:2].lower(), 'Português')
        if dry:
            print('[teste] criaria .config/3doconfig.ode com idioma=%s' % _lv)
        else:
            try:
                os.makedirs(os.path.dirname(_cfgp), exist_ok=True)
                with open(_cfgp, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write('#3DOREBORN-CONFIG#\nidioma=%s\n#END#\n' % _lv)
                print('Config : .config/3doconfig.ode criado com idioma=%s (as outras opcoes ficam no padrao do boot)' % _lv)
            except OSError as e:
                print('Config : nao consegui criar o .config/3doconfig.ode (%s)' % e)
    print()
    print(f'Jogos: {len(report)}   jogos preparados: {made}   ja atualizados: {skipped}   '
          f'imagens baixadas: {dl}   videos .cvd: {vmade}   sem capa: {len(sem)}')
    print(f'Faltam -> capa: {len(miss_cov)}   tela: {len(miss_sht)}   video: {len(miss_vid)}   (listas em {midias})')
    if report_on and not dry:
        print('Relatorio em / report in: cover.txt')
    if boot:
        src = boot if os.path.isfile(boot) else find_boot_iso(root, midias, boot if os.path.isdir(str(boot)) else None)
        downloaded = False
        if not src and not offline and not dry:          # Nao achou local -> BAIXA do repo
            print('Boot   : boot.iso nao achado localmente - baixando o menu do repo...')
            got = download_boot_iso(os.path.join(root, 'boot.iso'))
            if got:
                src = got; downloaded = True
        if not src:
            print('Boot   : boot.iso nao encontrado (sem internet? informe o caminho) - pulando')
        elif dry:
            print('[teste] copiaria %s p/ a raiz do cartao' % src)
        elif downloaded:
            print('Boot   : boot.iso baixado do repo p/ a raiz do cartao')
        else:
            try:
                dst, copied = copy_boot_to(root, src)
                print('Boot   : %s' % ('boot.iso copiado p/ a raiz do cartao'
                                       if copied else 'boot.iso ja esta na raiz (nada a copiar)'))
            except OSError as e:
                print('Boot   : nao consegui copiar o boot.iso (%s)' % e)
    # NUNCA APAGA NADA DO USUARIO (sem opcao de limpar). / never deletes the user's files


# ============ ASSISTENTE (sem opcoes na linha de comando) / INTERACTIVE WIZARD ============
# As respostas do assistente ficam em generate_usb.ini, AO LADO do programa (do .py, ou do .exe quando
# empacotado: no .exe o __file__ aponta p/ uma pasta temporaria que some ao fechar).
INI_DIR = (os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False)
           else os.path.dirname(os.path.abspath(__file__)))
INI_PATH = os.path.join(INI_DIR, 'generate_usb.ini')


def _ini_load():
    d = {}
    try:
        for ln in open(INI_PATH, 'r', encoding='utf-8'):
            if '=' in ln and not ln.startswith('#'):
                k, v = ln.split('=', 1); d[k.strip()] = v.strip()
    except OSError:
        pass
    return d


def _ini_save(d):
    try:
        with open(INI_PATH, 'w', encoding='utf-8') as f:
            f.write('# generate_usb.ini - respostas do assistente do generate_usb (apague p/ voltar ao padrao)\n')
            for k, v in d.items(): f.write('%s=%s\n' % (k, v))
    except OSError:
        pass


def _ask(txt, default=''):
    try:
        r = input('%s%s: ' % (txt, (' [%s]' % default) if default else ''))
    except EOFError:
        return default
    r = r.strip()
    return r if r else default


def _yn(txt, default):
    """pergunta sim/nao; default True/False / yes-no question"""
    while True:
        r = _ask(txt + ('  (Y/n)' if default else '  (y/N)'), '').lower()
        if not r: return default
        if r in ('s', 'sim', 'y', 'yes'): return True
        if r in ('n', 'nao', 'não', 'no'): return False


def _pick(txt, options, default):
    """escolha numerada; options = [(valor, rotulo)] / numbered choice"""
    print(txt)
    for i, (v, lab) in enumerate(options, 1):
        print('   %d) %s%s' % (i, lab, '   <- atual' if v == default else ''))
    di = next((i for i, (v, _) in enumerate(options, 1) if v == default), 1)
    while True:
        r = _ask('   escolha', str(di))
        if r.isdigit() and 1 <= int(r) <= len(options):
            return options[int(r) - 1][0]


_WIZ_T = {
 'pt': {
  'hdr':'generate_usb - assistente passo a passo (Enter aceita o valor entre [ ])',
  'tip':'Dica: com qualquer opcao na linha de comando ele roda direto, sem perguntas.',
  's_folders':'PASTAS - seus jogos e suas midias',
  'q_games':'Pasta ONDE ESTAO OS SEUS JOGOS (.iso ou .cue/.bin) - o pendrive/USB ou uma pasta no PC',
  'notfound':'pasta nao encontrada',
  'q_media':'Pasta das MIDIAS (capas, telas, videos, gamelist)  [Enter = mesma pasta dos jogos; da p/ BAIXAR online nos proximos passos]',
  'media_nf':'(pasta de midias nao encontrada: usando a mesma dos jogos)',
  'found':'encontrado: %d capas, %d telas, %d videos, %s',
  'dat_yes':'.dat: ','dat_no':'nenhum .dat (Redump)',
  's_fix':'ARRUMAR OS ARQUIVOS DO CARTAO (antes de gerar)',
  'iso_exp':'Ha %d jogo(s) em .iso. Converter p/ .bin/.cue (Redump) bate tamanho/CRC com o .dat e permite renomear. ~30s por disco, precisa de numpy.',
  'q_iso2bin':'Converter .iso -> .bin/.cue?',
  'q_isodel':'Apagar o .iso depois de converter? (o .bin/.cue novos ficam)',
  'q_rename':'Renomear jogos de nome generico (disc.iso, game.cue...) pelo .dat ou pela pasta?',
  'q_idall':'Conferir TODOS os jogos no .dat pelo CRC (nome oficial Redump)? (lento)',
  'q_flatten':'Tirar jogos de pastas com 1 jogo so (aparecer com capa, sem pasta)?',
  'fold_exp':'Organizar em pastas deixa o menu numa lista so e acelera o lancamento em cartoes grandes.',
  'q_organize':'Organizar os jogos em pastas?',
  'org_keep':'deixar do jeito que esta','org_root':'deixar tudo na raiz (tira das pastas e apaga as vazias)',
  'org_letter':'por letra (A..Z, 0, #)',
  's_art':'CAPAS, TELAS E TEXTOS',
  'q_cprep':'Preparo da imagem (vale p/ capas e telas):',
  'cp_texto':'TEXTO - PADRAO: nitidez forte, pontilhado so fora das letras; letras mais legiveis',
  'cp_nitida':'NITIDA - nitidez media, pontilhado medio; meio-termo',
  'cp_suave':'SUAVE - pouca nitidez, pontilhado leve; imagem lisa, letras mais moles',
  'cp_sempontos':'SEM PONTOS - sem pontilhado; cores lisas, degrades podem ficar com faixas',
  'cp_corfiel':'COR FIEL - pontilhado em tudo; cor mais fiel, mais granulada',
  'q_covers':'Gerar capas e telas - de onde pegar:','cov_local':'usar so as da minha pasta (sem internet)','cov_online':'usar as minhas e BAIXAR as que faltarem','cov_all':'baixar TUDO da internet (ignora as minhas)',
  'q_genlist':'Gerar o gamelist (ano/genero/produtora/descricao de cada jogo)?',
  's_video':'VIDEOS (previa animada nos detalhes)',
  'vid_none':'nenhum video em %s - pulando (ponha os .mp4 na pasta videos/)',
  'vid_noff':'ffmpeg nao encontrado - pulando os videos (ponha o ffmpeg.exe ao lado deste programa)',
  'q_vgen':'Gerar os videos de previa em Cinepak (.cvd)? (%d video(s))',
  'q_vsize':'Tamanho:','v_mini':'mini 80x60 - o mais rapido de todos; imagem em blocos (teste de velocidade)','v_box':'caixa 128x96 - quase o tamanho da caixa da descricao; bem leve','v_small':'pequeno 160x120 - o mais leve; a caixa da descricao e menor que isso (recomendado)','v_med':'medio 240x180 - mais nitido em tela cheia, mais pesado','v_large':'grande 320x240 - tela cheia, o mais pesado',
  'q_vfps':'Quadros por segundo:','q_vseg':'Duracao:','q_vmissing':'Videos: gerar SO os que faltam no cartao? (N = refaz todos)',
  's_cfg':'BOOT (copia para o cartao)',
  'q_boot':'Copiar o boot.iso (o menu) para a raiz do cartao?',
  'q_boot_dl':'Baixar o boot.iso (o menu) do repositorio e por na raiz do cartao?',
  'boot_found':'boot.iso encontrado: %s',
  'boot_path':'Caminho do boot.iso  [Enter = pular]',
  'boot_none':'nenhum boot.iso por perto - informe o caminho ou deixe em branco p/ pular',
  's_extras':'EXTRAS','q_report':'Gerar o relatorio cover.txt (jogo x capa x tela x texto)?','q_dry':'So simular (mostra o que faria, nao grava nada)?',
  'cmd_equiv':'Comando equivalente (para a proxima vez, sem perguntas):','q_start':'Comecar agora?','cancelled':'cancelado','done':'Concluido. Enter para fechar.',
 },
 'en': {
  'hdr':'generate_usb - step-by-step wizard (Enter accepts the value in [ ])',
  'tip':'Tip: pass any option on the command line and it runs straight away, no questions.',
  's_folders':'FOLDERS - your games and your media',
  'q_games':'Folder WHERE YOUR GAMES ARE (.iso or .cue/.bin) - the USB drive or a folder on the PC',
  'notfound':'folder not found',
  'q_media':'MEDIA folder (covers, screenshots, videos, gamelist)  [Enter = same folder as the games; you can DOWNLOAD online in the next steps]',
  'media_nf':'(media folder not found: using the same as the games)',
  'found':'found: %d covers, %d screenshots, %d videos, %s',
  'dat_yes':'.dat: ','dat_no':'no .dat (Redump)',
  's_fix':'TIDY UP THE CARD FILES (before generating anything)',
  'iso_exp':'%d game(s) are .iso. Converting to .bin/.cue (Redump) matches size/CRC with the .dat and allows renaming. ~30s per disc, needs numpy.',
  'q_iso2bin':'Convert .iso -> .bin/.cue?',
  'q_isodel':'Delete the .iso after converting? (the new .bin/.cue stay)',
  'q_rename':'Rename games with generic names (disc.iso, game.cue...) using the .dat or the folder?',
  'q_idall':'Check ALL games against the .dat by CRC (official Redump name)? (slow)',
  'q_flatten':'Pull games out of single-game folders (show with box art, no folder)?',
  'fold_exp':'Organizing into folders keeps the menu as one list and speeds up launching on big cards.',
  'q_organize':'Organize games into folders?',
  'org_keep':'leave as is','org_root':'move everything to the root (out of folders, remove empty ones)',
  'org_letter':'by letter (A..Z, 0, #)',
  's_art':'COVERS, SCREENSHOTS AND TEXT',
  'q_cprep':'Image preparation (covers and screenshots):',
  'cp_texto':'TEXT - DEFAULT: strong sharpening, dithering only off the letters; most readable text',
  'cp_nitida':'SHARP - medium sharpening and dithering; middle ground',
  'cp_suave':'SOFT - light sharpening and dithering; smooth image, softer text',
  'cp_sempontos':'NO DOTS - no dithering; flat colors, gradients may show bands',
  'cp_corfiel':'TRUE COLOR - dithering everywhere; truest color, grainier',
  'q_covers':'Generate covers and screenshots - where from:','cov_local':'use only the ones in my folder (offline)','cov_online':'use mine and DOWNLOAD the missing ones','cov_all':'download EVERYTHING from the internet (ignore mine)',
  'q_genlist':'Generate the gamelist (year/genre/publisher/description per game)?',
  's_video':'VIDEOS (animated preview in the details)',
  'vid_none':'no video in %s - skipping (put .mp4 in videos/)',
  'vid_noff':'ffmpeg not found - skipping videos (put ffmpeg next to this program)',
  'q_vgen':'Generate the Cinepak video previews (.cvd)? (%d video(s))',
  'q_vsize':'Size:','v_mini':'mini 80x60 - fastest of all; blocky picture (speed test)','v_box':'box 128x96 - about the size of the description box; very light','v_small':'small 160x120 - lightest; the description box is smaller than this (recommended)','v_med':'medium 240x180 - sharper fullscreen, heavier','v_large':'large 320x240 - fullscreen, heaviest',
  'q_vfps':'Frames per second:','q_vseg':'Duration:','q_vmissing':'Videos: ONLY the ones missing on the card? (N = redo all)',
  's_cfg':'BOOT (copied to the card)',
  'q_boot':'Copy boot.iso (the menu) to the card root?',
  'q_boot_dl':'Download boot.iso (the menu) from the repository and put it at the card root?',
  'boot_found':'boot.iso found: %s',
  'boot_path':'Path to boot.iso  [Enter = skip]',
  'boot_none':'no boot.iso nearby - type a path or leave blank to skip',
  's_extras':'EXTRAS','q_report':'Generate the cover.txt report (game x cover x screenshot x text)?','q_dry':'Dry run only (show what it would do, write nothing)?',
  'cmd_equiv':'Equivalent command (for next time, no questions):','q_start':'Start now?','cancelled':'cancelled','done':'Done. Press Enter to close.',
 },
 'es': {
  'hdr':'generate_usb - asistente paso a paso (Enter acepta el valor entre [ ])',
  'tip':'Consejo: pasa cualquier opcion en la linea de comandos y se ejecuta directo, sin preguntas.',
  's_folders':'CARPETAS - tus juegos y tus medios',
  'q_games':'Carpeta DONDE ESTAN TUS JUEGOS (.iso o .cue/.bin) - la USB o una carpeta en el PC',
  'notfound':'carpeta no encontrada',
  'q_media':'Carpeta de MEDIOS (caratulas, capturas, videos, gamelist)  [Enter = la misma de los juegos; puedes DESCARGAR online en los proximos pasos]',
  'media_nf':'(carpeta de medios no encontrada: usando la misma de los juegos)',
  'found':'encontrado: %d caratulas, %d capturas, %d videos, %s',
  'dat_yes':'.dat: ','dat_no':'sin .dat (Redump)',
  's_fix':'ORDENAR LOS ARCHIVOS DE LA TARJETA (antes de generar)',
  'iso_exp':'%d juego(s) en .iso. Convertir a .bin/.cue (Redump) coincide tamano/CRC con el .dat y permite renombrar. ~30s por disco, necesita numpy.',
  'q_iso2bin':'Convertir .iso -> .bin/.cue?',
  'q_isodel':'Borrar el .iso despues de convertir? (los nuevos .bin/.cue quedan)',
  'q_rename':'Renombrar juegos con nombre generico (disc.iso, game.cue...) por el .dat o la carpeta?',
  'q_idall':'Comprobar TODOS los juegos en el .dat por CRC (nombre oficial Redump)? (lento)',
  'q_flatten':'Sacar juegos de carpetas con un solo juego (aparecer con caratula, sin carpeta)?',
  'fold_exp':'Organizar en carpetas mantiene el menu en una sola lista y acelera el arranque en tarjetas grandes.',
  'q_organize':'Organizar los juegos en carpetas?',
  'org_keep':'dejar como esta','org_root':'mover todo a la raiz (sacar de carpetas y borrar las vacias)',
  'org_letter':'por letra (A..Z, 0, #)',
  's_art':'CARATULAS, CAPTURAS Y TEXTO',
  'q_cprep':'Preparacion de la imagen (caratulas y capturas):',
  'cp_texto':'TEXTO - POR DEFECTO: nitidez fuerte, punteado solo fuera de las letras; letras mas legibles',
  'cp_nitida':'NITIDA - nitidez y punteado medios; termino medio',
  'cp_suave':'SUAVE - poca nitidez, punteado leve; imagen lisa, letras mas blandas',
  'cp_sempontos':'SIN PUNTOS - sin punteado; colores lisos, los degradados pueden tener franjas',
  'cp_corfiel':'COLOR FIEL - punteado en todo; color mas fiel, mas granulado',
  'q_covers':'Generar caratulas y capturas - de donde:','cov_local':'usar solo las de mi carpeta (sin internet)','cov_online':'usar las mias y DESCARGAR las que falten','cov_all':'descargar TODO de internet (ignora las mias)',
  'q_genlist':'Generar el gamelist (ano/genero/editor/descripcion de cada juego)?',
  's_video':'VIDEOS (vista previa animada en los detalles)',
  'vid_none':'sin video en %s - omitiendo (pon .mp4 en videos/)',
  'vid_noff':'ffmpeg no encontrado - omitiendo videos (pon ffmpeg junto a este programa)',
  'q_vgen':'Generar las vistas previas en Cinepak (.cvd)? (%d video(s))',
  'q_vsize':'Tamano:','v_mini':'mini 80x60 - el mas rapido; imagen en bloques (prueba de velocidad)','v_box':'caja 128x96 - casi el tamano de la caja de la descripcion; muy ligero','v_small':'pequeno 160x120 - el mas ligero; la caja de la descripcion es menor (recomendado)','v_med':'mediano 240x180 - mas nitido a pantalla completa, mas pesado','v_large':'grande 320x240 - pantalla completa, el mas pesado',
  'q_vfps':'Cuadros por segundo:','q_vseg':'Duracion:','q_vmissing':'Videos: SOLO los que faltan en la tarjeta? (N = rehace todos)',
  's_cfg':'BOOT (se copia a la tarjeta)',
  'q_boot':'Copiar boot.iso (el menu) a la raiz de la tarjeta?',
  'q_boot_dl':'Descargar boot.iso (el menu) del repositorio y ponerlo en la raiz de la tarjeta?',
  'boot_found':'boot.iso encontrado: %s',
  'boot_path':'Ruta del boot.iso  [Enter = omitir]',
  'boot_none':'no hay boot.iso cerca - escribe una ruta o deja en blanco para omitir',
  's_extras':'EXTRAS','q_report':'Generar el informe cover.txt (juego x caratula x captura x texto)?','q_dry':'Solo simular (muestra lo que haria, no graba nada)?',
  'cmd_equiv':'Comando equivalente (para la proxima vez, sin preguntas):','q_start':'Empezar ahora?','cancelled':'cancelado','done':'Hecho. Pulsa Enter para cerrar.',
 },
}


# ===================== FIRMWARE TADEU (setup rapido pelo cartao) =====================
# Baixa o .u2f do repo e grava firmware/update.3do (UF2 + trailer FX3D com CRC32,
# com CRC32) -> o boot valida o CRC antes de gravar.
FW_REPO    = 'cyberrep/3doode'
FW_VERSION = '1.0.7'
# Um arquivo para cada tipo de placa (o chip de direcao dos dados): DIR-LOW = original
# Waveshare (74HC245); DIR-HIGH = clones tzmwx / TaiHu (74LVC4245).
FW_FILES   = {'usb': 'TADEU_%s_DIR-LOW.uf2' % FW_VERSION,
              'dual': 'TADEU_%s_DIR-HIGH.uf2' % FW_VERSION}
FW_URLS    = ['https://raw.githubusercontent.com/' + FW_REPO + '/main/firmware/%s',
              'https://raw.githubusercontent.com/' + FW_REPO + '/master/firmware/%s',
              'https://github.com/' + FW_REPO + '/releases/latest/download/%s']

def _fw_uf2_to_3do(data):
    """UF2 -> update.3do (UF2 + trailer FX3D 512B com CRC32). Igual tools/make_update.py."""
    import struct, zlib
    UF2_M0 = 0x0A324655; UF2_ME = 0x0AB16F30; XIP = 0x10000000; FXL = 0x44335846
    if not data or len(data) % 512 != 0:
        return None
    nblk = len(data) // 512; chunks = {}; maxoff = 0
    for i in range(nblk):
        b = data[i*512:(i+1)*512]
        m0, = struct.unpack('<I', b[0:4]); me, = struct.unpack('<I', b[508:512])
        if m0 != UF2_M0 or me != UF2_ME:
            return None
        addr, plen = struct.unpack('<II', b[12:20]); off = addr - XIP
        if off < 0:
            return None
        chunks[off] = b[32:32+plen]; maxoff = max(maxoff, off + plen)
    img = bytearray(b'\xff' * maxoff)
    for off, pay in chunks.items():
        img[off:off+len(pay)] = pay
    crc = zlib.crc32(bytes(img)) & 0xFFFFFFFF
    tr = bytearray(b'\xff' * 512)
    struct.pack_into('<III', tr, 0, FXL, crc, maxoff)
    lab = b'Fixel 3DO ODE firmware update'; tr[16:16+len(lab)] = lab
    return bytes(data) + bytes(tr)

def _fw_download(name):
    """baixa o firmware; tenta o nome dado E a extensão alternativa (.uf2 <-> .u2f). / download fw, try both exts."""
    import urllib.request, os as _os
    base, ext = _os.path.splitext(name)
    names = [name]
    if ext.lower() == '.uf2':
        names.append(base + '.u2f')
    elif ext.lower() == '.u2f':
        names.append(base + '.uf2')
    for nm in names:
        for tmpl in FW_URLS:
            try:
                req = urllib.request.Request(tmpl % nm, headers={'User-Agent': 'Mozilla/5.0'})
                d = urllib.request.urlopen(req, timeout=60).read()
                if d and len(d) > 2048:
                    return d
            except Exception:
                continue
    return None

_FWT = {
 'pt': {'sec':'FIRMWARE DA ODE (opcional - preparar no cartao)',
   'ask':'Quer preparar a firmware TADEU neste cartao agora?',
   'path':'Pasta do cartao/USB (onde fica a pasta firmware/)',
   'cur':'Qual firmware esta na sua ODE agora?','off':'Oficial (de fabrica / Fixel)','tadeu':'TADEU (a nossa)',
   'model':'Qual a sua placa?','m_usb':'DIR-LOW: original Waveshare (chip 74HC245)','m_dual':'DIR-HIGH: clone tzmwx / TaiHu (chip 74LVC4245)',
   'dl':'baixando %s ...','dlfail':'nao consegui baixar (sem internet?): %s',
   'badu2f':'o arquivo baixado nao e um .u2f valido - abortei (nada foi gravado).',
   'ok3do':'pronto: firmware/update.3do gravado (%d KB). No console: X -> FIRMWARE -> Atualizar Firmware.',
   'okuf2':'pronto: firmware/%s copiado (para o metodo BOOTSEL).',
   'steps':'Como instalar pelo BOOTSEL (firmware oficial):',
   's1':'1) Desligue o 3DO e acesse a placa RP2040 da ODE.',
   's2':'2) Segure BOOTSEL e ligue o RP2040 no PC pelo USB -> aparece o drive RPI-RP2.',
   's3':'3) Arraste o .u2f para dentro do RPI-RP2. A placa reinicia sozinha com o TADEU.',
   'skip':'ok, pulei a firmware.'},
 'en': {'sec':'ODE FIRMWARE (optional - prepare on the card)',
   'ask':'Prepare the TADEU firmware on this card now?',
   'path':'Card/USB folder (where the firmware/ folder lives)',
   'cur':'Which firmware is on your ODE right now?','off':'Official (stock / Fixel)','tadeu':'TADEU (ours)',
   'model':'Which board do you have?','m_usb':'DIR-LOW: original Waveshare (74HC245 chip)','m_dual':'DIR-HIGH: tzmwx / TaiHu clone (74LVC4245 chip)',
   'dl':'downloading %s ...','dlfail':'could not download (no internet?): %s',
   'badu2f':'the downloaded file is not a valid .u2f - aborted (nothing written).',
   'ok3do':'done: firmware/update.3do written (%d KB). On the console: X -> FIRMWARE -> Update Firmware.',
   'okuf2':'done: firmware/%s copied (for the BOOTSEL method).',
   'steps':'How to install via BOOTSEL (official firmware):',
   's1':'1) Power the 3DO off and reach the ODE RP2040 board.',
   's2':'2) Hold BOOTSEL and plug the RP2040 into the PC by USB -> the RPI-RP2 drive shows up.',
   's3':'3) Drag the .u2f onto RPI-RP2. The board reboots into TADEU by itself.',
   'skip':'ok, skipped the firmware.'},
 'es': {'sec':'FIRMWARE DE LA ODE (opcional - preparar en la tarjeta)',
   'ask':'Quieres preparar el firmware TADEU en esta tarjeta ahora?',
   'path':'Carpeta de la tarjeta/USB (donde esta la carpeta firmware/)',
   'cur':'Que firmware tiene tu ODE ahora?','off':'Oficial (de fabrica / Fixel)','tadeu':'TADEU (el nuestro)',
   'model':'Cual es tu placa?','m_usb':'DIR-LOW: original Waveshare (chip 74HC245)','m_dual':'DIR-HIGH: clon tzmwx / TaiHu (chip 74LVC4245)',
   'dl':'descargando %s ...','dlfail':'no pude descargar (sin internet?): %s',
   'badu2f':'el archivo descargado no es un .u2f valido - aborte (no se grabo nada).',
   'ok3do':'listo: firmware/update.3do grabado (%d KB). En la consola: X -> FIRMWARE -> Actualizar Firmware.',
   'okuf2':'listo: firmware/%s copiado (para el metodo BOOTSEL).',
   'steps':'Como instalar por BOOTSEL (firmware oficial):',
   's1':'1) Apaga el 3DO y accede a la placa RP2040 de la ODE.',
   's2':'2) Manten BOOTSEL y conecta el RP2040 al PC por USB -> aparece la unidad RPI-RP2.',
   's3':'3) Arrastra el .u2f dentro de RPI-RP2. La placa reinicia sola con TADEU.',
   'skip':'ok, salte el firmware.'}}

def _cfg_set(root, key, val):
    """Grava/troca a linha key=val em .config/3doconfig.ode (so se o arquivo ja existe: quem cria e o menu)."""
    path = os.path.join(root, '.config', '3doconfig.ode')
    try:
        with open(path, 'rb') as f: lines = f.read().decode('utf-8', 'replace').splitlines()
    except Exception:
        return
    lines = [l for l in lines if not l.startswith(key + '=')] + ['%s=%s' % (key, val)]
    with open(path, 'wb') as f: f.write(('\n'.join(lines) + '\n').encode('utf-8'))

# ============ PACOTES (.pak): capas e telas num arquivo so por pasta ============
# O menu 1.6, com o firmware TADEU 1.0.7 ou mais novo, abre o pacote e vai direto a
# imagem (busca dentro do arquivo), em vez de procurar cada arquivo numa pasta cheia.
# Formato (big-endian): "3DPK", 1, 0, quantas (2 bytes); quantas x {hash, posicao};
# as imagens. hash = FNV-1a 32 do nome do arquivo do jogo sem extensao, A-Z em minusculas.
PAK_DIRS = [(('covers', 'small'), 'small.pak'), (('covers', 'large'), 'large.pak'), (('screenshots', 'medium'), 'medium.pak'), (('screenshots', 'large'), 'large.pak')]
PAK_MAX = 2000

def _pak_hash(name):
    h = 2166136261
    for c in name.encode('utf-8'):
        if 65 <= c <= 90: c += 32
        h = ((h ^ c) * 16777619) & 0xffffffff
    return h

def make_paks(root, remove=False):
    """Monta os 3 pacotes com os .cel que estao no cartao (os arquivos soltos continuam).
    remove=True: apaga os pacotes (formato individual)."""
    import struct
    for parts, name in PAK_DIRS:
        src = os.path.join(root, *parts); out = os.path.join(root, parts[0], name)
        if remove or not os.path.isdir(src):
            if os.path.isfile(out) and remove:
                os.remove(out); print('Pacote : %s/%s apagado' % (parts[0], name))
            continue
        items = {}
        for f in sorted(os.listdir(src)):
            if f.lower().endswith('.cel'): items.setdefault(_pak_hash(f[:-4]), f)
        if not items: continue
        if len(items) > PAK_MAX:
            if os.path.isfile(out): os.remove(out)
            print('Pacote : %s/%s NAO gerado: %d imagens (o limite e %d)' % (parts[0], name, len(items), PAK_MAX)); continue
        keys = sorted(items); pos = 8 + 8 * len(keys); tab = []; body = []
        for k in keys:
            with open(os.path.join(src, items[k]), 'rb') as f: d = f.read()
            d += b'\0' * (-len(d) % 4)
            tab.append(struct.pack('>II', k, pos)); body.append(d); pos += len(d)
        with open(out, 'wb') as f:
            f.write(b'3DPK' + bytes([1, 0]) + struct.pack('>H', len(keys)) + b''.join(tab) + b''.join(body))
        print('Pacote : %s/%s (%d imagens)' % (parts[0], name, len(keys)))

def fw_firstrun(lang, default_root='', forced=False):
    t = _FWT.get(lang, _FWT['pt'])
    print('\n* ' + t['sec'])
    if not forced and not _yn('   ' + t['ask'], False):
        print('   ' + t['skip']); return
    while True:
        root = _ask('   ' + t['path'], default_root)
        if root and os.path.isdir(root): break
        if not root: print('   ' + t['skip']); return
        print('   ' + _WIZ_T[lang]['notfound'])
    cur   = _pick('   ' + t['cur'], [('tadeu', t['tadeu']), ('off', t['off'])], 'tadeu')
    model = _pick('   ' + t['model'], [('usb', t['m_usb']), ('dual', t['m_dual'])], 'usb')
    name  = FW_FILES[model]
    print('   ' + t['dl'] % name)
    data = _fw_download(name)
    if not data:
        print('   ' + t['dlfail'] % name); return
    u3do = _fw_uf2_to_3do(data)
    if not u3do:
        print('   ' + t['badu2f']); return
    fwdir = os.path.join(root, 'firmware')
    try: os.makedirs(fwdir, exist_ok=True)
    except Exception: pass
    with open(os.path.join(fwdir, 'update.3do'), 'wb') as f: f.write(u3do)
    # A versao, num arquivo ao lado: o menu mostra "Versao nova: 1.0.7" antes de gravar.
    with open(os.path.join(fwdir, 'update.ver'), 'wb') as f: f.write((FW_VERSION + '\r\n').encode('ascii'))
    # A placa escolhida, no arquivo de opcoes (a pagina web le para ja marcar o firmware certo).
    _cfg_set(root, 'ode_dir', 'LOW' if model == 'usb' else 'HIGH')
    print('   ' + t['ok3do'] % (len(u3do) // 1024))
    if cur == 'off':
        # firmware oficial nao atualiza pelo menu: deixa o .u2f e mostra o passo a passo BOOTSEL
        with open(os.path.join(fwdir, name), 'wb') as f: f.write(data)
        print('   ' + t['okuf2'] % name)
        print('   ' + t['steps']); print('   ' + t['s1']); print('   ' + t['s2']); print('   ' + t['s3'])


def wizard():
    ini = _ini_load()
    # idioma primeiro / language first
    print('=' * 66)
    print('  generate_usb')
    print('  Idioma / Language / Idioma:')
    print('     1) Portugues   2) English   3) Espanol')
    _lsel = _ask('  [1/2/3]', {'pt':'1','en':'2','es':'3'}.get(ini.get('lang','pt'), '1'))
    lang = {'1':'pt','2':'en','3':'es'}.get(_lsel.strip(), 'pt')
    T = _WIZ_T[lang]
    fw_firstrun(lang, ini.get('root', ''))
    print('=' * 66)
    print('  ' + T['hdr'])
    print('  ' + T['tip'])
    print('=' * 66)
    print('\n1) ' + T['s_folders'])
    while True:
        root = _ask('   ' + T['q_games'], ini.get('root', ''))
        if root and os.path.isdir(root): break
        print('   ' + T['notfound'])
    midias = _ask('   ' + T['q_media'], ini.get('midias', ''))
    if midias and not os.path.isdir(midias):
        print('   ' + T['media_nf']); midias = ''
    mdir = midias or root
    cov = find_dir(mdir, {'cover', 'covers', 'capa', 'capas'}, 'cover')
    sht = find_dir(mdir, {'screenshot', 'screenshots', 'tela', 'telas'}, 'screenshot')
    vid = find_dir(mdir, {'video', 'videos'}, 'video')
    ncov = len(local_images(cov)[0]) if os.path.isdir(cov) else 0
    nsht = len(local_images(sht)[0]) if os.path.isdir(sht) else 0
    nvid = len(local_videos(vid)[0]) if os.path.isdir(vid) else 0
    # Procura .dat em mdir, root E na subpasta gamelist/ (onde ele costuma ficar)
    _datdirs = [mdir] + ([root] if mdir != root else [])
    _gldir = find_dir(mdir, {'gamelist', 'gamelists'}, None)
    if _gldir and _gldir not in _datdirs:
        _datdirs.append(_gldir)
    dats = []
    for _dd in _datdirs:
        try:
            dats += [f for f in os.listdir(_dd) if f.lower().endswith('.dat')]
        except OSError:
            pass
    print('   ' + T['found'] % (ncov, nsht, nvid, (T['dat_yes'] + dats[0]) if dats else T['dat_no']))
    print('\n2) ' + T['s_fix'])
    nisos = sum(1 for dp, dn, fn in os.walk(root) for f in fn if f.lower().endswith('.iso') and f.lower() != 'boot.iso')
    iso2bin = False; iso_del = False
    if nisos:
        print('   ' + T['iso_exp'] % nisos)
        iso2bin = _yn('   ' + T['q_iso2bin'], ini.get('iso2bin', '0') == '1')
        if iso2bin:
            iso_del = _yn('   ' + T['q_isodel'], ini.get('iso_del', '0') == '1')
    # CHD -> .bin/.cue (via chdman) - o 3DO nao le CHD / CHD must be converted
    _chdmsg = {'pt': ('Ha %d arquivo(s) .chd. O 3DO nao le CHD; converto p/ .bin/.cue com o chdman (sem perda).',
                      'Converter os .chd em .bin/.cue?', 'Apagar o .chd depois de converter?'),
               'en': ('%d .chd file(s) found. The 3DO cannot read CHD; I convert to .bin/.cue with chdman (lossless).',
                      'Convert the .chd to .bin/.cue?', 'Delete the .chd after converting?'),
               'es': ('%d archivo(s) .chd. El 3DO no lee CHD; convierto a .bin/.cue con chdman (sin perdida).',
                      'Convertir los .chd a .bin/.cue?', 'Borrar el .chd despues de convertir?')}
    nchd = sum(1 for dp, dn, fn in os.walk(root) for f in fn if f.lower().endswith('.chd'))
    chd = True; chd_del = False
    if nchd:
        _cm = _chdmsg.get(lang, _chdmsg['pt'])
        print('   ' + _cm[0] % nchd)
        chd = _yn('   ' + _cm[1], True)
        if chd:
            chd_del = _yn('   ' + _cm[2], False)
    rename = _yn('   ' + T['q_rename'], ini.get('rename', '1') == '1')
    idall = False
    if rename and dats:
        idall = _yn('   ' + T['q_idall'], ini.get('idall', '1') == '1')   # Padrao SIM quando ha .dat (nomes Redump)
    flatten = _yn('   ' + T['q_flatten'], ini.get('flatten', '1') == '1')
    print('   ' + T['fold_exp'])
    organize = _pick('   ' + T['q_organize'], [('', T['org_keep']), ('raiz', T['org_root']), ('letra', T['org_letter'])], ini.get('organize', ''))
    print('\n3) ' + T['s_art'])
    _W = {'pt': ('Gerar as CAPAS?', 'Capas: gerar SO as que faltam no cartao? (N = refaz todas)', 'Gerar as TELAS (screenshots)?', 'Telas: gerar SO as que faltam no cartao? (N = refaz todas)'),
          'en': ('Generate the COVERS?', 'Covers: ONLY the ones missing on the card? (N = redo all)', 'Generate the SCREENSHOTS?', 'Screenshots: ONLY the ones missing on the card? (N = redo all)'),
          'es': ('Generar las CARATULAS?', 'Caratulas: SOLO las que faltan en la tarjeta? (N = rehace todas)', 'Generar las CAPTURAS?', 'Capturas: SOLO las que faltan en la tarjeta? (N = rehace todas)')}.get(lang, None) or \
         ('Gerar as CAPAS?', 'Capas: gerar SO as que faltam no cartao? (N = refaz todas)', 'Gerar as TELAS (screenshots)?', 'Telas: gerar SO as que faltam no cartao? (N = refaz todas)')
    do_cov = _yn('   ' + _W[0], ini.get('docov', '1') == '1')
    cov_missing = _yn('   ' + _W[1], ini.get('covmissing', '1') == '1') if do_cov else False
    do_sht = _yn('   ' + _W[2], ini.get('dosht', '1') == '1')
    sht_missing = _yn('   ' + _W[3], ini.get('shtmissing', '1') == '1') if do_sht else False
    # De onde pegar as imagens e o preparo: so se for gerar capas ou telas. / only when covers or shots are on
    _covmode = 'off'
    cprep = ini.get('cprep', 'texto')
    if do_cov or do_sht:
        _covmode = _pick('   ' + T['q_covers'], [('off', T['cov_local']), ('miss', T['cov_online']), ('all', T['cov_all'])], ini.get('covmode', 'off'))
        cprep = _pick('   ' + T['q_cprep'], [(k, T['cp_' + k]) for k in ('texto', 'nitida', 'suave', 'sempontos', 'corfiel')],
                      ini.get('cprep', 'texto'))
    cel_set_options(cprep)
    online = _covmode != 'off'
    redown = _covmode == 'all'
    # Cada tipo tem o seu "so os que faltam" (N = refaz todos daquele tipo).
    force = False
    print('\n4) ' + T['s_video'])
    video = False; vtam = 'small'; vfps = 15; vseg = 20; vmissing = False
    ffok = (vconv is not None and vconv.ffmpeg_ok())
    if nvid == 0:
        print('   ' + T['vid_none'] % os.path.basename(vid))
    elif not ffok:
        print('   ' + T['vid_noff'])
    else:
        video = _yn('   ' + T['q_vgen'] % nvid, ini.get('video', '1') == '1')
        if video and ffok:
            vtam = _pick('   ' + T['q_vsize'], [('mini', T['v_mini']), ('box', T['v_box']), ('small', T['v_small']), ('medium', T['v_med']), ('large', T['v_large'])],
                         ini.get('vtam', 'small') if ini.get('vtam', 'small') in ('mini', 'box', 'small', 'medium', 'large') else 'small')
            vfps = _pick('   ' + T['q_vfps'], [(10, '10'), (12, '12'), (15, '15'), (20, '20')], int(ini.get('vfps', '15')))
            vseg = _pick('   ' + T['q_vseg'], [(5, '5 s'), (10, '10 s'), (15, '15 s'), (20, '20 s'), (30, '30 s')], int(ini.get('vseg', '20')))
            vmissing = _yn('   ' + T['q_vmissing'], ini.get('vmissing', '1') == '1')
    # Lista de jogos (3dogamesdetails.ode) depois das imagens e dos videos.
    gen_list  = _yn('   ' + T['q_genlist'], ini.get('genlist', '1') == '1')
    print('\n5) ' + T['s_extras'])
    report = _yn('   ' + T['q_report'], ini.get('report', '0') == '1')
    dry = _yn('   ' + T['q_dry'], False)
    # 6) COPIA DO BOOT para o cartao / boot copy
    print('\n6) ' + T['s_cfg'])
    boot = None
    _bdef = find_boot_iso(root, midias or None)
    if _bdef:
        print('   ' + T['boot_found'] % _bdef)
        if _yn('   ' + T['q_boot'], ini.get('boot', '1') == '1'):
            boot = _bdef
    elif online and _yn('   ' + T['q_boot_dl'], True):
        boot = '__DL__'          # Baixa o boot.iso do repo em main()
    else:
        _bp = _ask('   ' + T['boot_path'], ini.get('bootpath', ''))
        if _bp and os.path.isfile(_bp):
            boot = _bp
        elif _bp:
            print('   ' + T['boot_none'])
    flags = []
    if midias: flags += ['--midias', '"%s"' % midias]
    if iso2bin: flags.append('--iso2bin')
    if iso_del: flags.append('--apagar-iso')
    if not chd: flags.append('--sem-chd')
    if chd_del: flags.append('--apagar-chd')
    if not rename: flags.append('--nao-renomear')
    if idall: flags.append('--identificar-tudo')
    if not flatten: flags.append('--nao-achatar')
    if organize: flags += ['--organizar', organize]
    if not online: flags.append('--offline')
    if redown: flags.append('--baixar-tudo')
    if lang != 'pt': flags += ['--idioma', lang]
    if force: flags.append('--forcar')
    if not do_cov: flags.append('--pular-capas')
    else: flags.append('--capas-faltantes' if cov_missing else '--refazer-capas')
    if not do_sht: flags.append('--pular-telas')
    else: flags.append('--telas-faltantes' if sht_missing else '--refazer-telas')
    if not video: flags.append('--sem-video')
    else:
        flags += ['--tamanho', vtam, '--video-fps', str(vfps), '--video-seg', str(vseg)]
        flags.append('--video-faltantes' if vmissing else '--refazer-videos')
    if not gen_list: flags.append('--pular-gamelist')
    if report: flags.append('--relatorio')
    if cprep != 'texto': flags += ['--capa-preparo', cprep]
    if boot: flags.append('--copiar-boot')
    if dry: flags.append('--teste')
    print('\n' + T['cmd_equiv'])
    print('   py generate_usb.py "%s" %s' % (root, ' '.join(flags)))
    if not _yn('\n' + T['q_start'], True):
        print(T['cancelled']); return
    _ini_save({'root': root, 'midias': midias, 'iso2bin': int(iso2bin), 'iso_del': int(iso_del), 'rename': int(rename),
               'idall': int(idall), 'flatten': int(flatten), 'organize': organize, 'online': int(online), 'covmode': _covmode, 'lang': lang,
               'force': int(force), 'video': int(video), 'vtam': vtam, 'vfps': vfps, 'vseg': vseg, 'report': int(report),
               'docov': int(do_cov), 'covmissing': int(cov_missing), 'dosht': int(do_sht), 'shtmissing': int(sht_missing),
               'vmissing': int(vmissing), 'boot': int(bool(boot)), 'bootpath': (boot or ''),
               'genlist': int(gen_list), 'cprep': cprep})
    print()
    main(root, dry, force, not online, report, rename, idall, flatten, midias=midias or None,
         video=video, vfps=vfps, vseg=vseg, vtam=vtam, organize=organize, iso2bin=iso2bin, iso2bin_delete=iso_del, lang=lang,
         do_cov=do_cov, do_sht=do_sht, cov_missing=cov_missing, sht_missing=sht_missing,
         cov_force=do_cov and not cov_missing, sht_force=do_sht and not sht_missing, vid_force=video and not vmissing,
         vmissing=vmissing, redown=redown, boot=boot, gen_list=gen_list,
         chd=chd, chd_delete=chd_del)
    try:
        input('\n' + T['done'])
    except EOFError:
        pass

if __name__ == '__main__':
    argv = sys.argv[1:]
    low = [a.lower() for a in argv]
    # --midias "<pasta>": onde estao cover/screenshots/gamelist (separada das ISOs)
    midias = None
    if '--midias' in low:
        i = low.index('--midias')
        if i + 1 < len(argv):
            midias = argv[i + 1]
    # opcoes de video / video options
    def valopt(name, default):
        if name in low:
            i = low.index(name)
            if i + 1 < len(argv):
                return argv[i + 1]
        return default
    vfps = int(valopt('--video-fps', '15'))
    vseg = float(valopt('--video-seg', '20'))
    vtam = valopt('--tamanho', 'small').lower()           # small 160x120 | medium 240x180 | large 320x240
    vtam = {'pequeno': 'small', 'medio': 'medium', 'grande': 'large', 'caixa': 'box'}.get(vtam, vtam)
    if vtam not in ('mini', 'box', 'small', 'medium', 'large'):
        vtam = 'small'
    try:
        vq = max(1, min(31, int(valopt('--video-q', '4'))))    # qualidade do Cinepak: 1 melhor/maior ... 31 pior/menor
    except ValueError:
        vq = 4
    consumed = set()
    for nm in ('--midias', '--video-fps', '--video-seg', '--video-q', '--tamanho', '--idioma',
               '--capa-preparo', '--cover-prep', '--capa-tamanho', '--cover-size'):
        if nm in low:
            j = low.index(nm)
            if j + 1 < len(argv):
                consumed.add(argv[j + 1])
    flags = set(a.lower() for a in argv if a.startswith('--'))
    args = [a for a in argv if not a.startswith('--') and a != midias and a not in consumed]
    lang = valopt('--idioma', None)
    if lang: lang = lang.lower()[:2]
    if ('--firmware' in low) or ('--fw' in low):
        fw_firstrun(lang or 'pt', (args[0] if args else ''), forced=True)
        sys.exit(0)
    orgmode = ''
    if flags & {'--organizar', '--organize', '--pastas-letra'}:
        v = valopt('--organizar', valopt('--organize', 'letra')).lower()
        if v.startswith('let'): orgmode = 'letra'; args = [a for a in args if a.lower() != v]
        elif v.startswith('rai') or v.startswith('root') or v.startswith('fla'): orgmode = 'raiz'; args = [a for a in args if a.lower() != v]   # tudo na raiz
        else: orgmode = 'letra'   # sem valor: letra / no value: letters
    if not argv:
        wizard(); sys.exit(0)
    _root0 = args[0] if args else '.'
    # --somente-renomear: SO renomeia pelo .dat (Redump), sem gerar nada / rename-only mode
    if flags & {'--somente-renomear', '--so-renomear', '--renomear', '--rename-only', '--only-rename'}:
        rename_only(_root0, midias)
        sys.exit(0)
    # --copiar-boot: acha o boot.iso por perto e copia p/ a raiz do cartao / auto-find boot.iso and copy to root
    cli_boot = None
    if (flags & {'--copiar-boot', '--copiar_boot', '--boot', '--copy-boot'}) and not (flags & {'--sem-boot', '--no-boot'}):
        cli_boot = find_boot_iso(_root0, midias)
        if not cli_boot and '--offline' not in flags:
            cli_boot = '__DL__'          # Baixa o boot.iso do repo em main()
        elif not cli_boot:
            print('aviso: --copiar-boot pedido, mas nenhum boot.iso foi encontrado por perto (ponha-o ao lado do script)')
    try:
        cel_set_options(valopt('--capa-preparo', valopt('--cover-prep', None)),
                        valopt('--capa-tamanho', valopt('--cover-size', None)))
    except ValueError as _e:
        print('ERRO:', _e); sys.exit(2)
    main(_root0, bool(flags & {'--teste', '--dry-run'}), bool(flags & {'--forcar', '--force'}),
         '--offline' in flags, '--relatorio' in flags,
         not bool(flags & {'--nao-renomear', '--no-rename'}), bool(flags & {'--identificar-tudo', '--id-all'}),
         not bool(flags & {'--nao-achatar', '--no-flatten'}), midias=midias,
         video=not bool(flags & {'--sem-video', '--no-video'}), vfps=vfps, vseg=vseg,
         onlyvideo=bool(flags & {'--so-video', '--apenas-video', '--only-video'}), vtam=vtam,
         organize=orgmode,
         iso2bin='--iso2bin' in flags, iso2bin_delete='--apagar-iso' in flags, lang=lang,
         vmissing=bool(flags & {'--video-faltantes', '--video-novos', '--video-missing'}),
         redown=bool(flags & {'--baixar-tudo', '--baixar-todas', '--redown', '--download-all'}),
         no_covers=bool(flags & {'--somente-lista', '--so-lista', '--sem-capas', '--apenas-lista', '--only-list', '--no-covers'}),
         gen_list=not bool(flags & {'--pular-gamelist', '--sem-gamelist', '--no-gamelist'}),
         chd=not bool(flags & {'--sem-chd', '--no-chd'}),
         chd_delete=bool(flags & {'--apagar-chd', '--delete-chd'}),
         vq=vq,
         do_cov=not bool(flags & {'--pular-capas', '--skip-covers'}), do_sht=not bool(flags & {'--pular-telas', '--skip-shots'}),
         cov_missing=bool(flags & {'--capas-faltantes', '--covers-missing'}), sht_missing=bool(flags & {'--telas-faltantes', '--shots-missing'}),
         cov_force=bool(flags & {'--refazer-capas', '--redo-covers'}), sht_force=bool(flags & {'--refazer-telas', '--redo-shots'}),
         vid_force=bool(flags & {'--refazer-videos', '--redo-videos'}),
         boot=cli_boot)
    # Capas e telas em pacote (menu 1.6 + firmware TADEU 1.0.7): --pak monta, --sem-pak apaga.
    if not bool(flags & {'--teste', '--dry-run'}):
        if '--pak' in flags: make_paks(_root0)
        elif bool(flags & {'--sem-pak', '--no-pak'}): make_paks(_root0, remove=True)
