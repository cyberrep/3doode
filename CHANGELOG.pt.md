# 📝 Histórico de versões

[← Voltar ao início](README.pt.md) · [English](CHANGELOG.md) · **Português** · [Español](CHANGELOG.es.md)

Tudo o que mudou no **menu** (`boot.iso`), no **firmware TADEU** e no **gerador** (`generate_usb.py`), da versão mais nova para a mais antiga.

- [Menu — 1.6](#menu--16)
- [Menu — 1.5](#menu--15)
- [Menu — 1.4](#menu--14)
- [Menu — 1.3](#menu--13)
- [Menu — 1.2](#menu--12)
- [Menu — 1.1](#menu--11)
- [Menu — 1.0](#menu--10)
- [Menu — antes da 1.0 (versões 0.x)](#menu--antes-da-10-versões-0x)
- [Firmware TADEU](#firmware-tadeu)
- [Gerador (generate_usb.py)](#gerador-generate_usbpy)

---

## Menu — 1.6

**Otimizar USB** (com o firmware TADEU 1.0.7)
- ⚡ **As capas abrem muito mais rápido em cartões cheios.** Em cartão com centenas de jogos, as pastas de capas, telas e vídeos costumam ficar gravadas depois de todos os jogos, e o ODE precisa passar por todos eles cada vez que abre uma capa. Agora o menu pede ao ODE para colocar essas pastas no começo do cartão. Nenhum jogo é copiado nem apagado: só muda a ordem das pastas.
- **Ao ligar, o menu confere sozinho** (é instantâneo). Se o cartão precisa, pergunta: *"Mídias no fim do USB: otimizar acelera a leitura. Leva até 30 s, uma vez só."* Com o sim, ele otimiza e lê a lista de jogos de novo.
- **Opções → Dispositivo ODE → Otimizar USB**: *Verificar ao ligar* (padrão) ou *Desligado*. Com microSD o menu mostra "Otimizar SD". E **Otimizar agora**, para fazer na hora.
- Só aparece com o firmware **TADEU 1.0.7 ou mais novo**. Com outros firmwares nada muda.

**Capas e telas em pacote** (com o firmware TADEU 1.0.7)
- 📦 **As capas e as telas podem ir num arquivo só por pasta**: `covers/small.pak`, `covers/large.pak` e `screenshots/medium.pak`. O menu abre o pacote e vai direto à imagem, em vez de procurar cada arquivo numa pasta com centenas deles.
- Quem gera é a **página web**: em *Mídias*, **Formato das capas e telas: PAK ou Individual**. Em PAK as imagens vão direto para o pacote, gravado de uma vez; em Individual, um arquivo por imagem, como sempre. Ao trocar de formato a página converte o que já está no cartão. Imagem fora do pacote, cartão sem pacote ou firmware mais antigo: o menu usa os arquivos soltos.
- Em *Mídias* dá para escolher **o que empacotar** (tudo, só as capas, ou só as capas pequenas), para controlar o tamanho do pacote.
- *Informações do ODE* mostra **Capas em pacote** e **Telas em pacote**: Sim ou Não.
- Memória: 8 bytes por imagem em cada pacote (cerca de 7 KB para 293 jogos nos três).

**Informações do console**
- 🔎 **Grupo "Chips"**: os registradores do **MADAM** e do **CLIO** por inteiro e o **encoder de vídeo** do seu console — *Brooktree (BT9101)* nos NTSC, *Brooktree (BT9103)* nos PAL, *ANVIL* ou *VP536 ou ANVIL*. Útil para quem pensa em mod de RGB ou 240p.
- A tela ficou mais enxuta: a versão do sistema e o estado da música saíram (continuam no relatório de diagnóstico), e "Capas na memória" foi para *Informações do ODE*.

**Página web**
- **Renomear: quando o navegador não deixa renomear direto**, a página pede a permissão de novo e, se ainda assim não der, pergunta se pode fazer copiando o arquivo com o nome novo e apagando o antigo.
- **Renomear: aviso de "já existe"** quando o cartão já tem um arquivo com o nome novo (o mesmo jogo duas vezes). Esse arquivo fica como está.
- 🔍 **Procurar o jogo** (na tela Jogos): para o jogo que ficou sem capa, tela ou textos, escolha o jogo certo na biblioteca e as mídias dele passam a valer para o seu arquivo, sem renomear nada. Ou use uma imagem sua: cole (Ctrl+V), arraste ou escolha um arquivo, e ela aparece ali na hora.
- 📦 **Baixar as minhas imagens (.zip)**: junta as capas e telas que você escolheu à mão, com o nome do jogo, para mandar para a biblioteca.
- Opção **Otimizar USB** em *Opções → Dispositivo ODE*.
- Ao gravar o firmware no cartão, a página escolhe sozinha o **mais novo** da sua placa e informa a versão ao menu.
- **Cabeçalho com a versão atual**: BOOT e FIRMWARE.
- **A página sabe o que está no cartão**: o menu grava a versão dele (`menu_ver`) e a do firmware; a página guarda a placa (`ode_dir`, DIR-HIGH ou DIR-LOW). Se o cartão já está na versão atual, *Menu* e *Firmware* começam em **Não**; se o firmware é mais antigo, já vem marcado o arquivo da sua placa.
- **Otimizar USB / SD** só aparece com firmware TADEU 1.0.7 ou mais novo.

**Atualizar firmware**
- A confirmação mostra a **versão atual** do ODE e a **versão nova** que será gravada.
- No fim da gravação a tela pede para **desligar e ligar o console**, piscando em amarelo e vermelho.

**Informações do ODE**
- Linha nova **USB** (ou **SD**): *Pastas otimizadas* ou *Não otimizado*.
- O menu guarda a versão do firmware no arquivo de opções do cartão (`ode_ver`), para a página web saber o que o seu ODE tem.

**Lista**
- **Lista com Tela ou Vídeo:** uma linha fina (1 pixel) separa a imagem das barras de cima e de baixo.
- Com capas e telas em pacote, os vídeos continuam em arquivos separados e tocam normalmente.

---

## Menu — 1.5

**Correções**
- **O controle não trava mais enquanto as capas carregam.** A leitura de cada capa passou a ser feita em passos curtos, e o controle continua respondendo durante o carregamento, em todos os modos. Um toque rápido na direção não se perde mais.
- **Faixa: o país aparecia cortado**, só com a primeira letra. Ano e país agora ficam numa faixa translúcida na base da tela do jogo (ano à esquerda, país à direita); o gênero continua no texto.
- **Faixa: o nome do jogo que não cabe na tela agora passa**, como na Lista.
- **Janelas de aviso e Ferramentas:** a faixa dos botões passava da borda arredondada da janela.
- **Vitrine:** a capa de caixa de CD ficava mais baixa que a long box; agora as duas começam na mesma altura.

**Velocidade**
- ⚡ **Capas carregam antes de você chegar nelas:** a página atual e a seguinte, no modo Capas.
- **Telas dos jogos já prontas ao navegar** (Faixa e Lista com tela): o menu guarda 5 telas e lê as vizinhas do jogo selecionado com antecedência.
- **Descrição mais rápida na Vitrine e na Faixa.** Em ODE com busca dentro do arquivo (*seek*), o menu vai direto ao texto do jogo, sem ler o arquivo de descrições desde o começo.
- **Desenho mais leve** no modo Capas enquanto as capas chegam.

**Memória**
- 🧠 **Mais capas na memória ao mesmo tempo.** As Ferramentas e o catálogo de saves só ocupam memória quando abertos, a área de pastas só existe no modo Pastas e a memória de vídeo livre passou a guardar capas.
- O espaço das capas é refeito a cada troca de modo de visualização, do tamanho que o modo precisa.

**Página web e manuais**
- 🧭 **Passo a passo na página**: uma caixa no meio da primeira tela leva pelas cinco etapas (Cartão, Nomes, Mídias, Opções, Gravar), com Voltar e Avançar.
- **Renomear mostra "de → para"** com o que muda em cada nome marcado em cores.
- 📖 **Botão "Como usar" na página**: os cinco passos para preparar o cartão, nos 3 idiomas.
- **Manual da página** ([docs/SITE.pt.md](docs/SITE.pt.md)), passo a passo e com imagens. O README passou a indicar a página primeiro; o gerador ficou como caminho avançado.

**Opções e textos**
- 🎚️ **Nova opção Opções → Aparência → Mídias → Transparência das faixas** (0%, 25%, 50%, 75%, 100%): o quanto aparece da capa por trás das faixas de ano/país e de discos/favorito. Padrão 75%.
- **Lista com Tela ou Vídeo:** saíram as linhas de divisão entre a imagem e as barras de cima e de baixo.
- **Formato Ambilight mais leve:** a montagem do brilho ficou mais rápida e é feita num passo separado da leitura, para não segurar o controle.
- **Opções → Dispositivo ODE** abre em sanfona, como Aparência (todo submenu que não cabe na tela funciona assim).
- Texto do primeiro início: **"SALVANDO A LISTA DE JOGOS — O próximo início será mais rápido"**.

---

## Menu — 1.4

**Lista de jogos**
- **O primeiro jogo do cartão não some mais no Xport com FAT32.** Em cartões com pastas por letra, o jogo da primeira pasta (ex.: `#/3D Pinball…`) ficava fora da lista.
- **Jogo sem descrição usa a do mesmo jogo de outra região.** "Battle Blues (Korea)" mostra a produtora, o gênero, o ano e a descrição de "Battle Blues (USA)" quando só um deles tem texto.
- O aviso **NÃO FOI POSSÍVEL INICIAR** mostra o código do erro inteiro (antes só o último dígito).

**Capas**
- 🖼️ **Nova opção Opções → Aparência → Formato das capas.** Long box e caixa de CD não são mais esticadas:
  - **Original** (padrão): a capa aparece na proporção dela, com a moldura em volta.
  - **Ambilight**: a capa no meio, com um brilho nas cores da própria capa preenchendo a sobra.
  - **Fundo preto**: a capa no meio, com a sobra preta.
  - **Esticada**: como era antes.
- Vale em todas as telas: Lista, Capas, Carrossel, Carrossel FX, Vitrine, Faixa, Descrição e a capinha da tela de início.
- Na **Lista**, a capa sempre começa na altura da primeira linha de jogos, e a linha dourada e as jogadas ficam encostadas embaixo dela.
- As capas precisam ser **gravadas de novo** (a página faz isso sozinha); as antigas continuam funcionando, esticadas como antes.

**Opções e Ferramentas**
- O relatório do **Testar o ODE e o USB** (`3dodiag.txt`) agora traz também o registro da leitura do USB: um arquivo só para mandar quando algo der errado.
- Cinco textos que apareciam em português no espanhol e no inglês foram traduzidos (Ler o USB de novo, backup dos saves e o aviso de ferramenta ausente).

**Página web**
- ✨ **Imagens mais nítidas e limpas.** Capas e telas passaram a ser reduzidas pela média de toda a área da imagem original, com nitidez leve e sem pontilhado: somem o serrilhado, o granulado e o contorno branco em volta das letras e dos personagens.
- **Capas na proporção real** (long box e caixa de CD), prontas para o Formato das capas.
- **As capas e telas antigas do cartão são substituídas pelas novas** na primeira gravação, mesmo com "Manter" escolhido. Só fica a antiga que não tem de onde refazer.
- **Resumo antes de gravar**: a tela Gravar no cartão mostra o que será gravado, o que já está no cartão e o total de arquivos.
- **Capa da região certa** nas suas próprias imagens: "Cannon Fodder (USA)" não pega mais a capa do "(Europe)". Sem a da região, a ordem é USA, Europe, Japan.
- Imagens em subpastas de nome desconhecido (como `cover3d`) não entram mais como capas.
- Na gravação aparece um botão por vez: Começar parado, Parar gravando.

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

### 1.0.7
- ⚠️ **Antes de instalar o TADEU pela primeira vez, faça o backup do firmware original** com o `picotool` (passo a passo no README). O TADEU ainda não foi testado nas placas dual do FZ-10, nem em GoldStar e Sanyo.
- ⚡ **Otimizar USB: as pastas de mídia vão para o começo.**
  - **O problema.** Um cartão guarda os nomes dos arquivos numa lista, na ordem em que foram gravados. Para abrir uma capa, o ODE lê essa lista desde o começo até achar a pasta `covers`. Quando você copia os jogos primeiro e as mídias depois, a pasta fica no fim, depois de centenas de jogos, e cada capa custa essa leitura inteira. Num HD com 650 itens isso dava perto de 0,2 segundo por capa só para achar a pasta.
  - **Por que o computador não resolve.** No formato exFAT, o Windows sempre grava o que é novo no fim da lista. Renomear, mover ou copiar de novo pelo PC não muda a posição.
  - **O que o firmware faz.** O próprio ODE reorganiza a lista: tira as pastas `covers`, `screenshots`, `videos` e `.config` do lugar onde estão e as recoloca nas primeiras posições. São cerca de 20 operações de troca de nome. **Nenhum jogo e nenhuma capa são copiados ou apagados.**
  - **O resultado.** Nos testes, com 650 jogos na raiz, achar a pasta de capas caiu de cerca de 290 leituras do cartão para 3, em exFAT e em FAT32.
  - **Quanto demora.** Conferir se o cartão precisa leva um instante e é feito toda vez que o console liga. Otimizar leva de 10 a 30 segundos e só precisa ser feito **uma vez por cartão** (de novo só se você formatar ou recriar as pastas).
  - **Se a energia cair no meio**, na próxima vez o firmware percebe o que ficou pela metade e termina o serviço.
  - Precisa do menu **1.6** ou mais novo, que é quem pergunta e manda otimizar.
- 🎯 **Leitura direta dentro de um arquivo (*seek*).** O firmware agora pula para qualquer ponto de um arquivo aberto, em vez de ler tudo desde o começo. Com isso o menu busca a descrição de um jogo indo direto ao texto dele, e fica aberto o caminho para guardar todas as capas num arquivo só.
- 📦 **Arquivos: `TADEU_1.0.7_DIR-HIGH` e `TADEU_1.0.7_DIR-LOW`**, um para cada tipo de placa (veja a explicação na 1.0.6).

#### ⏱️ Tempos: de fábrica, TADEU até 1.0.6 e TADEU 1.0.7

| | De fábrica | TADEU até 1.0.6 | TADEU 1.0.7 |
|---|:---:|:---:|:---:|
| Abrir um jogo do fim do USB | ~30 s | 2 a 4 s | 2 a 4 s |
| Achar a pasta de capas, a cada capa (≈650 itens na raiz, pasta no fim) | ~175 ms ¹ | ~175 ms | ~8 ms ² |
| Leituras do cartão para achar a pasta de capas | ~290 ¹ | ~290 | 3 |
| Buscar a descrição de um jogo | lê o arquivo desde o começo | lê o arquivo desde o começo | vai direto ao texto |
| Conferir se o cartão está otimizado | — | — | ~2 ms |
| Otimizar (uma vez por cartão) | — | — | 10 a 30 s |

¹ Não medido em separado: o firmware de fábrica abre arquivos do mesmo jeito que o TADEU até 1.0.6. ² Depois de otimizar; valor medido com a pasta no começo da raiz. Os tempos mudam com o cartão e com a quantidade de jogos.

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

### Novembro de 2026 (menu 1.6)
- **`--pak` / `--sem-pak`**: monta (ou apaga) os pacotes de capas e telas que o menu 1.6 lê com o firmware TADEU 1.0.7.
- **Firmware**: baixa o **TADEU 1.0.7** da sua placa (DIR-LOW ou DIR-HIGH), grava ao lado a versão que o menu mostra antes de atualizar e anota a placa no arquivo de opções.

### Novembro de 2026 (menu 1.4)
- ✨ **Imagens mais nítidas e limpas**: redução pela média de área, nitidez leve e sem pontilhado, igual à página web. Os "preparos" antigos (texto, nítida, suave…) deixaram de existir.
- **Capas na proporção real** (long box ≈ 76x140, caixa de CD ≈ 100x87), sem esticar.
- **As capas e telas antigas são refeitas sozinhas** na primeira execução (`generate_usb.py` e `converter_tudo.py`).

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
