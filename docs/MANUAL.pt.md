# 🛠️ Gerador de USB / SD — Manual

[← Voltar ao início](../README.pt.md) · [English](MANUAL.md) · **Português** · [Español](MANUAL.es.md)

> 🌐 **A maioria das pessoas não precisa deste gerador.** O jeito mais fácil é a [página web](https://cyberrep.github.io/3doode/), que prepara o cartão pelo navegador sem instalar nada: veja o **[manual da página](SITE.pt.md)**. Use o gerador para converter jogos (`.chd`, `.iso`), converter os seus próprios vídeos, ou se o seu navegador for Firefox ou Safari.

O `generate_usb.py` prepara o seu USB (ou cartão) do 3DO ODE **sozinho**. Você baixa **só este arquivo** e ele faz o resto:

- gera as **capas** e as **telas** dos jogos, cada uma em dois tamanhos;
- converte as **prévias em vídeo** para Cinepak;
- monta os **textos dos jogos** (ano, gênero, produtora, descrição);
- converte `.chd` e `.iso` para `.bin/.cue`, renomeia e organiza os jogos;
- **copia o menu (`boot.iso`)** para o USB;
- cria o arquivo de opções do menu já no seu idioma;
- pode **baixar e preparar o firmware** da sua placa.

Ele **nunca apaga** os seus arquivos.

---

## ✅ Instalação (Windows 10 e 11)

Abra o **PowerShell** ou o **Prompt de Comando** e cole os comandos, um de cada vez.

**1. Python**

```
winget install -e --id Python.Python.3.12
```

**2. FFmpeg** (só se você for converter vídeos)

```
winget install -e --id Gyan.FFmpeg
```

**3. Feche e abra o PowerShell de novo**, para ele enxergar os programas instalados.

**4. Confira**

```
py --version
ffmpeg -version
```

Se os dois responderem com a versão, está pronto.

**As bibliotecas do Python você não precisa instalar.** Na primeira vez, o próprio `generate_usb.py` instala o Pillow e o NumPy sozinho (e o `pip`, se o seu Python veio sem ele). Só se isso falhar, por exemplo sem internet, rode à mão:

```
py -m pip install pillow numpy
```

Para jogos em `.chd` é preciso ainda o **chdman** (vem com o MAME): deixe o `chdman.exe` na mesma pasta do `generate_usb.py`.

No **Linux** e no **macOS**, instale `python3`, `ffmpeg` e rode `python3 -m pip install pillow numpy`.

## 🚀 Jeito fácil (assistente)

Rode sem opções:

```
py generate_usb.py
```

A **primeira pergunta é o idioma** (Português, English, Español). Depois vêm os passos:

1. **Pastas** — onde estão os **seus jogos** (o USB ou uma pasta do PC) e a sua pasta de **mídias** (capas, telas, vídeos e textos).
2. **Arrumar os jogos** — converter `.chd → .bin/.cue` (sem perda) e `.iso → .bin/.cue`, renomear nomes genéricos (`disc.iso`…), tirar jogos de pastas com um jogo só, e **organizar**: como está, tudo na raiz ou em pastas por letra.
3. **Capas, telas e textos** — três perguntas separadas, cada uma com a opção **"só as que faltam"**. O gerador usa as suas imagens e **baixa** as que não achar.
4. **Vídeos** — converte os vídeos da pasta `videos/` para Cinepak, no tamanho, na duração e na qualidade que você escolher.
5. **Extras** — o relatório `cover.txt`, ou só simular (mostra o que faria, sem gravar nada).
6. **Menu** — copia o **`boot.iso`** para a raiz do USB.

No fim ele mostra o **comando equivalente**, para você repetir sem perguntas da próxima vez, e executa. As respostas ficam guardadas em `generate_usb.ini`, ao lado do programa.

### Firmware (opcional)

O gerador também prepara o **firmware TADEU**: você diz qual é a sua placa e ele baixa o arquivo certo e o deixa em `firmware/` no USB, pronto para *Opções → Dispositivo ODE → Atualizar firmware*. Se o seu ODE ainda está no firmware de fábrica, a primeira instalação é pelo BOOTSEL: segure o botão, ligue o Pico no PC e arraste o `.uf2`.

---

## ⚙️ Linha de comando

```
py generate_usb.py "<pasta dos jogos>" [opções]
```

### Geral

| Opção | O que faz |
|---|---|
| `--teste` | Só simula: mostra o que faria, sem gravar. |
| `--forcar` | Refaz tudo, mesmo o que já existe. |
| `--offline` | Não baixa nada da internet. |
| `--idioma pt\|en\|es` | Idioma dos textos dos jogos. |
| `--midias "<pasta>"` | Pasta das mídias, quando ela fica separada dos jogos. |
| `--relatorio` | Gera o relatório `cover.txt`. |
| `--copiar-boot` | Copia o `boot.iso` para a raiz do USB (procura ao lado do programa e, se não achar, baixa). |
| `--firmware` | Abre direto o preparador de firmware. |

### Capas, telas e textos

| Opção | O que faz |
|---|---|
| `--pular-capas` / `--capas-faltantes` / `--refazer-capas` | Não gera capas / só as que faltam / refaz todas. |
| `--pular-telas` / `--telas-faltantes` / `--refazer-telas` | O mesmo, para as telas. |
| `--capa-preparo texto\|nitida\|suave\|sempontos\|corfiel` | O tratamento da imagem da capa. O padrão é `texto`. Trocar o preparo refaz todas as capas. |
| `--baixar-tudo` | Baixa de novo as imagens, mesmo as que já tem. |
| `--somente-lista` | Gera só os textos dos jogos, sem capas, telas nem vídeos. |
| `--pular-gamelist` | Não mexe nos textos dos jogos. |

### Vídeos

| Opção | O que faz |
|---|---|
| `--tamanho mini\|box\|small\|medium\|large` | 80×60 · 128×96 · 160×120 (padrão) · 240×180 · 320×240. |
| `--video-fps N` | Quadros por segundo. Padrão 15. |
| `--video-seg N` | Duração em segundos. Padrão 20. |
| `--video-q N` | Qualidade, de 1 (melhor, arquivo maior) a 31. Padrão 4. |
| `--video-faltantes` / `--refazer-videos` | Só os que faltam / refaz todos. |
| `--so-video` | Faz só os vídeos. |
| `--sem-video` | Pula os vídeos. |

### Jogos

| Opção | O que faz |
|---|---|
| `--iso2bin` / `--apagar-iso` | Converte `.iso → .bin/.cue` / apaga o `.iso` depois de converter. |
| `--sem-chd` / `--apagar-chd` | Não converte os `.chd` / apaga o `.chd` depois de converter. |
| `--nao-renomear` / `--identificar-tudo` | Não renomeia / confere cada jogo pela assinatura do disco. |
| `--somente-renomear` | Só renomeia os jogos, sem gerar nada. |
| `--nao-achatar` | Mantém as pastas que têm um jogo só. |
| `--organizar letra\|raiz` | Move os jogos para pastas A…Z, ou traz todos para a raiz. |

---

## 📦 O que ele grava no USB

Sempre na **raiz** do USB, com o mesmo nome do arquivo do jogo (em jogos de vários discos, o nome do disco 1):

| Onde | O que é |
|---|---|
| `covers/small/<jogo>.cel` | Capa 56 × 78, para a grade de Capas e o menu principal. |
| `covers/large/<jogo>.cel` | Capa 100 × 140, para as outras exibições e a descrição. |
| `screenshots/medium/<jogo>.cel` | Tela até 120 × 90. |
| `screenshots/large/<jogo>.cel` | Tela até 304 × 228, para a tela cheia. |
| `videos/<jogo>.cvd` | Prévia em vídeo, em Cinepak, sem som. |
| `.config/3dogamesdetails.ode` | Ano, gênero, produtora, publicadora e descrição de todos os jogos. |
| `.config/3doconfig.ode` | Opções do menu. Só é criado se ainda não existe, com o idioma escolhido. |
| `boot.iso` | O menu (se você pedir). |

O gerador **não mexe** nos seus favoritos, recentes e estatísticas.

### De onde vêm as imagens e os textos

- **Imagens**: primeiro as suas, nas pastas `cover/` e `screenshot/` das mídias. O que faltar é baixado e guardado ali, para funcionar sem internet da próxima vez.
- **Textos**: do `gamelist.pt.txt`, `gamelist.es.txt` ou `gamelist.en.txt`, conforme o idioma escolhido. Cada jogo traz ano, desenvolvedor, publicadora, gênero e descrição.
- **Vídeos**: os deste repositório já vêm convertidos (20 segundos, 15 quadros por segundo) e são só copiados. Para converter os seus, ponha os vídeos de origem na pasta `videos/` (mp4, avi, mkv…) e escolha o tamanho, os quadros por segundo e a duração.

### Como um jogo é ligado à capa e aos textos

Só o título conta: o que está entre `( )` ou `[ ]` no nome do arquivo é ignorado, assim como acentos, maiúsculas e pontuação. `Alone in the Dark (USA).iso`, `Alone in the Dark (U).iso` e `Alone in the Dark (inglês) [!].cue` acham a mesma capa, tela, vídeo e textos.

---

## 💡 Dicas

- **Vídeo lento para converter?** Use `--tamanho small`, menos segundos e `--video-faltantes`.
- **USB lento no console?** Prefira vídeos menores (`mini`, `box` ou `small`).
- **Formatos de jogo**: o ODE lê `.iso` e `.cue` + `.bin`. Outros formatos precisam ser convertidos no PC antes.
- **Capas não aparecem?** Confira se o nome do arquivo da capa é igual ao nome do arquivo do jogo.
