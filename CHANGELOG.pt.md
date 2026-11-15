# 📝 Histórico de versões

[← Voltar ao início](README.pt.md) · [English](CHANGELOG.md) · **Português** · [Español](CHANGELOG.es.md)

Tudo o que mudou no **menu** (`boot.iso`), no **firmware TADEU** e no **gerador** (`generate_usb.py`), da versão mais nova para a mais antiga.

- [Menu — 1.0](#menu--10)
- [Menu — antes da 1.0 (versões 0.x)](#menu--antes-da-10-versões-0x)
- [Firmware TADEU](#firmware-tadeu)
- [Gerador (generate_usb.py)](#gerador-generate_usbpy)

---

## Menu — 1.0

Primeira versão pública. Reúne tudo o que foi feito nas versões de desenvolvimento (0.x), descritas abaixo, e acrescenta:

- **Publicadora de cada jogo**, mostrada na Vitrine e na Faixa (os textos dos jogos ganharam o campo `Publisher`).
- **Vídeos em 20 segundos e 15 quadros por segundo** como padrão.

O que a 1.0 tem, em resumo: 6 modos de exibição, prévia em vídeo, favoritos, recentes e estatísticas, filtro e ordenação, multi-disco, gerenciador de saves, ferramentas do console, 3 idiomas, relógio de tempo real, detecção do console e funcionamento nos dois firmwares.

---

## Menu — antes da 1.0 (versões 0.x)

As versões de desenvolvimento, da mais nova para a mais antiga.

### 0.9 — Vitrine, Faixa, fundos e opções novas

**Novos modos Vitrine e Faixa**
- **Dois modos de exibição novos**: **Vitrine** (capa grande com produtora, gênero, ano, país e a descrição inteira) e **Faixa** (a tela do jogo e a descrição em cima, fileira de capas deslizando embaixo).
- Nos dois, ◄ ► troca de jogo e ▲ ▼ rola a descrição.
- A tela e a descrição do jogo são lidas **antes** das capas vizinhas, para aparecerem logo.
- No painel do último jogo do menu principal, **A abre a descrição** e P joga direto.
- **Traduções fora do programa**: o espanhol e o inglês viraram arquivos no disco do menu, lidos só quando são usados. O programa ficou menor e sobrou memória.
- **Opções mais rápidas**: andar entre os itens e trocar valores não refaz mais a tela inteira.
- **Percentual dentro de toda barra de andamento.**
- Ao terminar uma gravação, a tela mostra **tamanho e tempo** ("6 minutos e 11 segundos").
- Teste de controle: a barra de saída fica na cor do controle que está segurando os botões.
- Backup das configurações lista o que será salvo: configurações, recentes, favoritos e estatísticas.
- O protetor de tela não entra mais logo depois de uma operação demorada.
- A capa do último jogo não some mais ao trocar de exibição.

**Fundos, ferramentas à parte e memória**
- **9 fundos de tela** (Padrão, Fibra de carbono, Aço escovado, Colmeia, Listras, Grade, Chapa, Vinheta, Pontos).
- **Ferramentas num módulo separado**, carregado só quando uma delas abre: o menu ficou mais leve.
- **Memória de capas por exibição**: a grade de Capas guarda muitas capas pequenas; as outras exibições, capas grandes.
- **Protetor de tela** com o logo do 3DO e os consoles passeando pela tela.
- Música voltando a tocar em consoles com pouca memória livre.
- Tela de sucesso da atualização do firmware com a foto do console e o aviso para desligar e ligar.
- *Sobre* mostra o firmware e a versão do ODE; *Informações do console* mostra a música e as capas na memória.
- A sanfona da Aparência abre sempre fechada.
- O relógio é consultado a cada 5 segundos, deixando o menu mais solto.

**Opções novas e som**
- **Aparência em sanfona**: Menu principal, Jogos, Mídias e Tela, um grupo aberto por vez, com animação.
- **Ordenar por** nome, ano, gênero, produtora ou mais jogados.
- **Lembrar a posição**, **Artigo na frente**, **Tela ao ligar** e **Protetor de tela**.
- **Backup e restauração das configurações**, dos favoritos, dos recentes e das estatísticas, e **Restaurar os padrões**.
- **Tocador de música próprio**, com **volume em barra** que muda na hora, e a opção **Aleatória**.

### 0.8 — Cartão do jogo, firmware de fábrica, relógio e mídias

**Cartão do jogo e ajustes**
- **Cartão do jogo ao iniciar**: capa, nome em amarelo, gênero, ano e país em azul, "N vezes jogado" e "N discos adicionados na fila".
- **Velocidade do nome** em 5 níveis.
- Capa do último jogo corrigida na grade de Capas; ajustes nas linhas da lista.
- Jogos voltando a abrir no firmware de fábrica depois de navegar em pastas.

**Firmware de fábrica e relógio**
- **Compatibilidade completa com o firmware de fábrica**: o menu não usa mais comandos que ele não tem, e a gravação no USB ganhou novas tentativas.
- **Recursos por versão do firmware**: cada opção só aparece se o firmware instalado a tem.
- **Aviso de relógio sem hora** (pilha fraca), sem travar o menu, com atalho para acertar.
- Ao acertar o relógio, o ano já começa no ano atual.
- Entrar e sair do painel do último jogo ficou instantâneo.
- No ODE da porta de expansão, os textos dizem **SD** quando a mídia é um cartão microSD.
- Medição dos tempos de partida.

**Lista, estatísticas e sons**
- **Vídeo na lista**: a prévia toca na caixa ao lado da lista.
- **Efeito da estrela** ao favoritar e desfavoritar, com som próprio.
- **Estatísticas em ranking**, com a quantidade de partidas de cada jogo.
- Sons guardados no disco do menu.
- **Ler o USB de novo** ao vivo e opções gravadas na hora.
- Página de **Agradecimentos** com rolagem.
- Entrada "Último" no topo da lista de jogos.
- Leitura da lista feita uma vez só e diagnóstico completo.
- Lista corrigida no ODE da porta de expansão.

**Mídias em dois tamanhos**
- **Capas e telas em dois tamanhos**: pequenas para as grades, grandes para o destaque e a tela cheia.
- Capas lidas com menos comandos; grade de Capas com 3 páginas na memória.
- Vídeo em vários tamanhos, com imagem parada quando o vídeo é pesado.
- **Formatos por idioma** (data, hora, temperatura, números).
- **Gerenciador de armazenamento** e tela de **Data e hora**.

### 0.7 — Vídeo e som
- **Vídeo em Cinepak** com decodificador próprio: na descrição, em tela cheia (X) e depois na lista.
- **Efeitos sonoros e música de fundo**, com 10 faixas.
- Botões definitivos da tela de descrição.

### 0.6 — Visual novo e ferramentas
- **Visual novo**: faixas finas em todas as telas, brilho passando na caixa selecionada do menu principal.
- **Teste de controle** com a foto do controle, para até 8 controles.
- **Ajuste de imagem**.
- **Lista guardada** (*Ler ao ligar*) para ligar mais rápido.
- **Idioma trocado na hora** (Português, Español, English).
- Imagens do menu fora do programa, no disco.
- **Teste do ODE e do USB**.
- Páginas de informação separadas: console, ODE e USB.
- Janela de "jogo iniciando".

### 0.5 — Jogar em qualquer firmware
- Lançamento de jogos acertado nos dois firmwares e nas duas placas.
- **Multi-disco**: todos os discos entram na fila ao jogar.
- Menos memória usada; lista sem falhas em coleções grandes.

### 0.4 — Opções, descrição e saves
- **Opções gravadas no USB** (`.config/3doconfig.ode`).
- **Tela de descrição do jogo**: capa, tela, dados e o texto com rolagem.
- **Favoritos, Recentes e Estatísticas**, com data e hora.
- **Filtro** por gênero e país.
- **Armazenamento**: gerenciador de saves, backup, restauração e diagnóstico da NVRAM.
- **Extração de ROMs e da RAM** do console.
- **Backup e atualização do firmware** pelo menu.
- Letras em maiúsculas, minúsculas ou primeira maiúscula.

### 0.3 — Tela principal e identidade
- **Menu principal** com as caixas Favoritos, Jogos, Estatísticas, Recentes e Opções.
- **Painel do último jogo.**
- **Detecção do console pela BIOS**, com a foto do aparelho no topo.
- **Relógio, data e temperatura** na tela.
- **Uma capa por jogo**, e os textos de todos os jogos num arquivo só, lido uma vez.
- Contagem de discos, região tirada do nome do arquivo, faixa translúcida com os discos na capa.
- Ícone de CD no lugar da capa que falta.

### 0.2 — Reescrito do zero

Em 10 de novembro de 2026 o menu foi **reescrito do zero**, com código novo, mais rápido e mais simples de manter.
- **Lista alfabética** com a capa ao lado, memória de capas e leitura antecipada.
- **Quatro exibições**: Lista, Capas, Carrossel e Carrossel FX (em perspectiva, com reflexo).
- **NTSC e PAL** automáticos.
- **Um único `boot.iso`** para o ODE interno e o da porta de expansão.
- Jogos em subpastas (até 3 níveis) numa lista só.
- Pulo por letra, rolagem do nome longo, aceleração ao segurar o direcional.

### 0.1 — Primeira geração

De 10 de outubro a 9 de novembro de 2026.

- **Última etapa** — abas trocadas por L / R; 4 modos de exibição; tela de detalhes redesenhada; Ferramentas e Opções reorganizadas; **backup do firmware** pelo console; extrações na pasta `roms/` e a NVRAM na `saves/`; protetor de tela com o logo e os consoles do 3DO; 10 trilhas de música.
- Leitura por caminho, ordem alfabética garantida, descrição instantânea, prévia pequena mais suave, "Limpar" nos Recentes.
- Pastas por letra juntadas numa lista única; base estável.
- Detecção do firmware em tempo real, grade de Capas pelo motor gráfico do console, troca de gênero mais rápida, prévia em vídeo, atualização de firmware.
- Menu base: lista alfabética, favoritos e recentes, filtro por gênero, memória de capas, multi-disco, telas cheias, configurações salvas no USB.

---

## Firmware TADEU

### 1.0.5
- **Relógio de tempo real (DS3231)**: data, hora, temperatura e estado da pilha.
- **Arquivos gravados com data e hora** certas.
- Acerto do relógio pelo console.

### 1.0.4
- **Espaço do USB**: tamanho total e espaço livre informados ao menu.

### 1.0.3
- **Uma só base de código para as duas placas** (a original e a clone com Pico comum), escolhida na compilação.

### 1.0.2
- **Marcador de versão** dentro do firmware, que o menu lê e mostra.

### 1.0 e 1.0.1
- **Lista rápida por extensão**: os jogos são reconhecidos por `.cue` e `.iso` sem abrir cada arquivo. Lançar um jogo do fim do USB caiu de cerca de 30 s para 2 a 4 s.
- **Paginação incremental** da lista.
- **Criação de pastas** pelo console.
- **Backup do firmware** pelo console, conferido byte a byte.
- **Atualização pelo menu**, com área de espera, conferência por CRC e verificação de cada bloco gravado. O firmware em uso nunca é sobrescrito antes da conferência.
- **Atualização à prova de erro ao ligar**: confere antes e depois de copiar; se algo falhar, entra em modo de recuperação em vez de ligar quebrado.
- **Número de série do chip.**
- Abertura de arquivos corrigida: ler um arquivo que não existe não cria mais um arquivo vazio.
- Mapa da memória flash ajustado para chips de 2 MB.
- Recuperação sempre possível pelo BOOTSEL.

---

## Gerador (`generate_usb.py`)

### Novembro de 2026
- **Publicadora** (`Publisher=`) nos textos dos jogos, em português, espanhol e inglês.
- Padrão dos vídeos: 20 segundos, 15 quadros por segundo.
- **Vídeos em Cinepak** (`.cvd`), em 5 tamanhos, com quadros por segundo, duração e qualidade à escolha.
- **Conversão de vídeo mais rápida**, com um vídeo por núcleo do PC ao mesmo tempo.
- **Capas e telas em dois tamanhos** cada.
- Perguntas separadas para capas, telas e vídeos, cada uma com "só as que faltam".
- Aproveita um USB gerado por versões antigas, sem precisar das imagens originais.
- Cria o arquivo de opções do menu só com o idioma, se ele ainda não existe.
- Código antigo removido: ficou um arquivo só, menor e mais simples.
- Respostas do assistente guardadas em `generate_usb.ini`.

### Outubro de 2026
- Assistente passo a passo em 3 idiomas.
- Download das capas e telas que faltam.
- Textos dos jogos (ano, gênero, produtora, descrição).
- Conversão de `.chd` e de `.iso` para `.bin/.cue`.
- Renomeação de discos com nome genérico e organização em pastas.
- Cópia do `boot.iso` e preparo do firmware.
