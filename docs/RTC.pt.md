# ⏰ Relógio de tempo real no 3DO — instalação do DS3231

[← Voltar ao início](../README.pt.md) · [English](RTC.md) · **Português** · [Español](RTC.es.md)

O 3DO nunca teve relógio. Com um módulo **DS3231** ligado ao Raspberry Pi Pico do ODE e o firmware **TADEU 1.0.5**, o seu console passa a saber a data, a hora e a temperatura. É o **primeiro ODE de 3DO do mundo com relógio de tempo real**.

São **4 fios**. Quem já soldou um fio consegue fazer.

---

## O que você ganha

- Data, hora e temperatura no menu principal.
- "Jogado: dd/mm/aaaa - hh:mm" no último jogo, nos Recentes e nas Estatísticas.
- Arquivos gravados no USB com a data certa (os backups da NVRAM levam a data e a hora no nome).
- Acerto do relógio pelo próprio console, em 12 ou 24 horas.
- Aviso quando a pilha do relógio acaba.

## Detecção automática

Você não precisa configurar nada. Ao ligar, o menu pergunta ao ODE se existe um relógio.

- **Com o módulo**: a data, a hora e a temperatura aparecem, e as opções do relógio entram no menu.
- **Sem o módulo**: nada aparece e nada muda. Não há relógio zerado nem mensagem de erro; o console funciona como sempre.

Ou seja: instalar o firmware TADEU 1.0.5 **sem** o módulo não tem problema nenhum.

## O que você precisa

| Item | Observação |
|---|---|
| Módulo **DS3231** | Qualquer módulo com os pinos **VCC, GND, SDA e SCL**. O mais comum é o azul, com suporte para pilha. |
| Pilha do módulo | **CR2032** (veja o aviso da pilha abaixo). |
| 4 fios finos | De preferência em 4 cores. Uns 10 a 15 cm cada. |
| Ferro de solda e estanho | Ponta fina. |
| Firmware **TADEU 1.0.5** ou mais novo | Versões anteriores não conversam com o relógio. |

---

## A ligação

<p align="center"><img src="../github/rtc-ds3231-pinos.png" width="720" alt="Ligação do DS3231 no Raspberry Pi Pico"></p>

| Pino do Pico | Nome | Vai no DS3231 |
|:---:|---|:---:|
| **1** | GP0 | **SDA** |
| **2** | GP1 | **SCL** |
| **3** | GND | **GND** |
| **36** | 3V3 (OUT) | **VCC** |

Os pinos **32K** e **SQW** do módulo ficam sem ligar.

**Como achar os pinos:** olhe o Pico de cima, com o conector USB para cima. O pino 1 é o primeiro da esquerda, de cima para baixo; o 2 e o 3 vêm logo abaixo. O pino 36 fica do lado direito: é o **quinto** de cima para baixo (40, 39, 38, 37, **36**).

> ⚠️ **Use o 3V3 (pino 36), nunca o VBUS ou o VSYS (pinos 40 e 39).** Esses dois têm 5 V e podem danificar o Pico pelos fios de dados.

> ⚠️ **Não solde nos três pontos "DEBUG"** da ponta de baixo do Pico. Eles não são usados aqui.

---

## Passo a passo

1. **Desligue o console da tomada** e abra-o até chegar na placa do ODE.
2. **Confira o firmware** antes de soldar: em *Opções → Dispositivo ODE → Informações do ODE* deve aparecer **TADEU 1.0.5** ou mais novo. Se não for, atualize primeiro.
3. **Solde os 4 fios no módulo**: VCC, GND, SDA e SCL.
4. **Solde os 4 fios no Pico**, seguindo a tabela. Solde rápido, com pouco estanho, e confira se nenhum pino encostou no vizinho. Os pinos 1, 2 e 3 ficam lado a lado: é onde mais se erra.
5. **Ponha a pilha** no módulo.
6. **Prenda o módulo** com fita dupla face num lugar onde ele não encoste em nada de metal. Isole a parte de baixo dele com fita isolante.
7. **Feche o console e ligue.**

## Conferir e acertar a hora

1. Abra *Opções → Dispositivo ODE → Recursos*. A linha **Relógio (DS3231)** deve dizer **Sim**.
2. Na primeira vez o menu avisa **"Relógio sem hora certa"** e oferece acertar. Aperte **A**.
   Ou vá em *Opções → Dispositivo ODE → Data e hora*.
3. ◄ ► escolhe o campo, ▲ ▼ muda o valor, **A** grava. Ali também se escolhe **12 ou 24 horas**.
4. Volte ao menu principal: a data, a hora e a temperatura aparecem embaixo, à direita.

Se quiser esconder alguma delas: *Opções → Aparência → Menu principal → Hora / Data / Temperatura*.

---

## ⚠️ A pilha

Muitos módulos DS3231 azuis saem de fábrica com um **circuito de recarga** (um diodo e um resistor ao lado do suporte), pensado para a pilha recarregável **LIR2032**.

- Com pilha **CR2032 comum** (não recarregável): **desative o circuito de recarga**, tirando o diodo ou o resistor ao lado do suporte da pilha. Pilha comum não pode ser recarregada.
- Com pilha **LIR2032** (recarregável): pode deixar o circuito como está.

Na dúvida, use o módulo com a recarga desativada e uma CR2032: ela dura anos.

O DS3231 não mede a carga da pilha. O que ele sabe dizer é se **o relógio parou** em algum momento. Quando isso acontece, o menu avisa ao ligar que a pilha está fraca e pede para acertar a hora. Se o aviso voltar toda vez que você liga o console, troque a pilha.

---

## Problemas comuns

| Sintoma | O que conferir |
|---|---|
| **Relógio (DS3231): Não** em Recursos | Firmware anterior ao 1.0.5; SDA e SCL trocados; solda fria; VCC no pino errado. |
| A hora volta a zerar ao desligar | Pilha fraca, ausente ou invertida. |
| Aviso "Relógio sem hora certa" toda vez | Pilha fraca: troque e acerte a hora de novo. |
| Console não liga depois da instalação | Desligue na hora. Procure pinos em curto (1, 2 e 3 ficam lado a lado) e confira se o VCC não foi parar no pino 39 ou 40. |
| Temperatura parece alta | É a temperatura **dentro do console**, medida pelo próprio DS3231. É normal ser mais alta que a do ambiente. |

## Detalhes técnicos

- Barramento **I²C 0** do RP2040, a 100 kHz: **GP0 = SDA**, **GP1 = SCL**.
- Endereço do DS3231: **0x68**.
- O firmware lê o relógio e guarda a última leitura; o menu pergunta a cada poucos segundos.
- A data e a hora também são usadas pelo sistema de arquivos do ODE: tudo o que o console grava no USB sai com a data certa.
- Ligação testada na placa com Raspberry Pi Pico comum. O firmware usa os mesmos GP0 e GP1 na placa original (RP2040-Plus); se a sua for essa, confira antes se esses dois pinos estão livres na placa.
- Sem o módulo, o firmware e o menu funcionam normalmente: o relógio simplesmente não aparece.
