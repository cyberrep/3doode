# 📝 Histórico de versões

[← Voltar ao início](README.pt.md) · [English](CHANGELOG.md) · **Português** · [Español](CHANGELOG.es.md)

Tudo o que mudou no **menu** (`boot.iso`), no **firmware TADEU** e no **gerador** (`generate_usb.py`), da versão mais nova para a mais antiga.

- [Menu — 1.3](#menu--13)
- [Menu — 1.2](#menu--12)
- [Menu — 1.1](#menu--11)
- [Menu — 1.0](#menu--10)
- [Menu — antes da 1.0 (versões 0.x)](#menu--antes-da-10-versões-0x)
- [Firmware TADEU](#firmware-tadeu)
- [Gerador (generate_usb.py)](#gerador-generate_usbpy)

---

## Menu — 1.3

**Lista de jogos**
- 🏷️ **Nova opção Opções → Jogos → Nome dos jogos: Título ou Arquivo.** Em **Arquivo** aparece o nome do arquivo sem a extensão (ex.: `Doom (USA)`); em **Título**, o nome limpo de sempre (`Doom`).
- **Jogo gravado como `.cue` + `.iso` com o mesmo nome aparece uma vez só** (antes virava dois). Quem usa a lista guardada precisa fazer **Ler o USB de novo** uma vez.
- **Favoritos e Recentes vazios**: mensagens novas ("Nenhum jogo em Favoritos." / "Nada jogado recentemente.") e a janela fecha no primeiro botão.

**Janelas de aviso e confirmação (pop-up padrão)**
- 🪟 **Todas as confirmações e avisos passaram a usar a mesma janela**, no menu e nas Ferramentas: título em amarelo, linha dourada, texto e uma faixa embaixo com os botões (Ⓐ SIM / Ⓑ NÃO, Ⓑ VOLTAR, Ⓑ CANCELAR). Antes várias abriam em tela cheia.
- **Uma janela só do começo ao fim.** Em backup, restauração, extração e gravação de firmware, a mesma janela mostra a pergunta, o andamento e o resultado.
- **RESUMO dentro da janela** ao terminar: "Gravado com sucesso", tamanho e tempo; no gerenciador de saves, a contagem de copiados, iguais e erros.
- Limpar recentes e limpar estatísticas perguntam na janela, com a descrição do que será apagado.

**Andamento das gravações**
- 📊 **Novo andamento "GRAVANDO"**: mostra o que está sendo gravado (ROM do sistema, firmware, NVRAM…), o **nome do arquivo**, a barra com a porcentagem e a **velocidade em KB/s**.
- **Ⓑ cancela o backup e a gravação do firmware.** Na gravação, o cancelamento acontece antes de aplicar: o firmware atual continua.
- Gravar firmware pede **uma confirmação só** (eram duas).
- Ao terminar de gravar o firmware: "O ODE está reiniciando o 3DO. Se não voltar, desligue e ligue."

**Opções e Ferramentas**
- **Ler o USB de novo acontece dentro da janela**, com a contagem de jogos e a barra, sem trocar para a tela de início.
- Setas de rolagem de verdade nas telas de informação (antes eram as letras `^` e `v`).
- Restaurar o backup das opções: texto mais direto ("Todos os itens serão restaurados do USB.").
- A janela **JOGO SENDO INICIADO** ganhou o título em amarelo, no padrão das outras.

**Página web**
- Novas opções **Mostrar jogos (Lista / Pastas)** e **Nome dos jogos (Título / Arquivo)**.
- Ao preparar o cartão, **cria as pastas `.config`, `saves`, `firmware` e `roms`**, para o menu já encontrar tudo no lugar.
- A escolha do firmware passou a ser **DIR-HIGH** ou **DIR-LOW**, com a explicação de qual é o de cada placa.

**Em investigação**
- No Xport com cartão FAT32, um jogo pode não aparecer na lista. Ainda sem causa confirmada.

---

## Menu — 1.2

**Navegação por pastas**
- 📁 **Nova opção Opções → Aparência → Mostrar jogos: Lista ou Pastas.** No modo **Pastas**, as pastas do cartão viram itens em que você **entra** (A) e **volta** (B). Pasta com 2 jogos ou mais vira pasta; **pasta com 1 jogo só vira o próprio jogo**. Pastas de sistema (capas, vídeos, saves, roms…) continuam ignoradas.
- 🎨 **As pastas têm a cara do menu**: ícone de pasta amarelo com a **letra grande no meio**, no formato de capa nos modos grandes (Capas, Carrossel, Vitrine, Faixa). A pasta fica **transparente**, sem moldura — só a selecionada ganha o destaque.
- Mensagem de **"nenhum jogo encontrado"** mais clara (nos 3 idiomas), avisando dos nomes de pasta reservados.

**Gerenciador de saves**
- 🌎 **Traduzido por completo** (espanhol e inglês): faltavam telas que estavam só em português.

**Correções**
- A lista de pastas aparece **na hora**, sem precisar reler o USB.
- Corrigida uma troca de cores nas bordas das capas (apareciam vermelhas onde deviam ser azuis) em alguns modos.

---

## Menu — 1.1

**Gerenciador de saves**
- 🎮 **Mostra de qual jogo é cada save.** Uma faixa embaixo da lista traz o nome do jogo do save selecionado (ex.: `alone1.save` → Alone in the Dark). A tabela tem 240 nomes, não diferencia maiúsculas de minúsculas e reconhece saves numerados (`TE_Devils_1`, `EA_RR3`...). Save que não está na tabela aparece com o nome do arquivo.
- **Copiar com o nome do jogo ou com o nome original**: ao copiar para o USB o menu pergunta. Com o nome do jogo o arquivo fica `Jogo (nome do save).sav`. **Na volta para o console o save sempre recebe o nome original**, que é o que o jogo procura.
- **Tabela de nomes atualizável sem trocar o menu**: a página web grava a tabela em `.config/3dogamessaves.ode`. Sem esse arquivo, o menu usa a tabela que vem dentro dele. Dá para criar o arquivo à mão só com correções (`=nome<TAB>jogo` ou `*prefixo<TAB>jogo`).
- **Bem mais rápido para navegar**: o fundo da tela não é mais redesenhado a cada movimento.
- **Telas padronizadas**: título, faixa dourada e textos. O **RESUMO** de copiar e restaurar mostra uma contagem por linha, em cores (verde copiados/restaurados, amarelo iguais, vermelho erros), e diz o motivo do último erro.
- **Lista do USB em ordem alfabética.**
- **Saves copiados para a pasta `saves/` pelo computador** passam a aparecer e restaurar depois de preparar o cartão na página web (ela registra cada arquivo no catálogo `saves/3dosaves.ode`). Linha do catálogo sem CRC restaura sem conferência; com CRC, o arquivo alterado continua recusado.
- Backups feitos na 1.0 continuam restaurando.

**Vitrine e Faixa**
- ⚡ **Vitrine e Faixa bem mais rápidas para navegar.** Na 1.0, a cada troca de jogo o menu esperava e lia o arquivo de textos de novo, mesmo para um jogo que tinha acabado de mostrar; em listas grandes a descrição demorava perto de 1 segundo.
- **Descrição na hora ao voltar ou avançar**: as últimas 8 descrições ficam na memória, então ir e voltar entre jogos vizinhos não lê mais o cartão.
- **Leitura adiantada dos vizinhos**: com o controle parado e as capas já na tela, o menu lê as descrições dos 2 jogos de cada lado e do destino do pulo de letra (anterior e próxima). A leitura para assim que o controle mexe, então não atrasa as capas nem a navegação.

**Opções**
- O menu grava nas opções **qual ODE detectou** (firmware, tipo e se há relógio). A página web lê isso e já marca as escolhas certas.

**Página web**
- **Marca sozinha o ODE, o firmware TADEU e o relógio** a partir do que o menu detectou.
- **Grava a tabela de nomes dos saves** no cartão.
- **Registra os saves da pasta `saves/`** no catálogo e corrige tamanho e CRC de linhas antigas.
- Correção: com **Manter** marcado, capas, telas e vídeos seus que já estão no cartão não são mais copiados de novo.

---

## Menu — 1.0

Primeira versão pública. Reúne tudo o que foi feito nas versões de desenvolvimento (0.x), descritas abaixo, e acrescenta:

- 💿🔥 **CD DE VERDADE NO XPORT, SEM TIRAR A PLACA (exclusivo).** Com a placa de expansão ligada, a tela principal ganha a caixa **CD** (cinza escura sem disco, azul clara com disco). **A** tira o Xport da porta, pede para abrir e fechar a tampa (FZ-10) ou abre e fecha a bandeja (outros modelos), e o console reinicia sozinho no disco. **B** cancela. O menu de fábrica do Xport não tem essa função. Confirmado em console real no FZ-10; a bandeja automática dos outros modelos está em teste. A rotina fica num arquivo à parte do disco (`XportCD`), carregado só nessa hora.
- **Tela de descrição nova**: o nome do jogo foi para a faixa de cima e a ficha ficou organizada ("Jogado: 2x - Última data", **desenvolvedora**, **produtora**, gênero, ano, país, discos com ícones). Com uma imagem, a ficha fica ao lado dela; com duas, as imagens vão para a esquerda e a ficha e o texto para a direita; com três, as imagens ficam em cima. Nome, desenvolvedora e produtora longos rolam devagar; rolar o texto não para mais o vídeo; o efeito do favorito aparece em cima da capa.
- **Você escolhe o que a ficha mostra**: *Opções > Aparência > Descrição* liga ou esconde cada dado.
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

### 1.0.6
- 🕒 **O relógio se protege sozinho.** Ao ligar, o firmware procura o chip do relógio (DS3231). Se ele não existe na placa, os dois pinos do relógio são liberados e as funções de data e hora ficam desligadas, em vez de atrapalhar o resto.
- 📦 **Dois arquivos, um para cada tipo de placa: `TADEU_1.0.6_DIR-HIGH` e `TADEU_1.0.6_DIR-LOW`.**

**Qual arquivo usar: DIR-HIGH ou DIR-LOW?**

As placas do ODE têm um chip que controla o sentido dos dados entre o ODE e o console. Existem dois modelos desse chip, e eles funcionam com o sinal de direção invertido um em relação ao outro. O firmware precisa ser o da sua placa.

- **`TADEU_1.0.6_DIR-LOW`**: placa original Waveshare (chip 74HC245).
- **`TADEU_1.0.6_DIR-HIGH`**: placas clone, como tzmwx e TaiHu (chip 74LVC4245).

**Se gravar o errado:** o console mostra o logo do 3DO e depois a tela fica preta. Não estraga nada: ponha o Pico em modo BOOTSEL (segure o botão ao ligar no computador) e grave o outro arquivo.

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
