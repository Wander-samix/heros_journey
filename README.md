# Resgate Thunder

Um jogo de plataforma (platformer) desenvolvido em Python com **PgZero** como projeto de avaliação. O objetivo é resgatar o gatinho Thunder, desviando de inimigos em um cenário animado e divertido.

## Como jogar

- Use as **setas do teclado** (← →) para mover o herói.
- Use a **barra de espaço** para pular.
- Clique nos botões no topo direito da tela para pausar/despausar e ligar/desligar o som.
- Ao perder toda a vida, o jogo acaba e volta ao menu.

## Requisitos

- Python 3.x
- [PgZero](https://pygame-zero.readthedocs.io/) (instale via `pip install pgzero`)
- Imagens dos personagens e botões devem estar na pasta `images` (veja abaixo).

## Estrutura dos arquivos

- `main.py` — código principal do jogo.
- Pasta `images/` — sprites do herói, inimigos, plano de fundo e ícones (todos PNGs já no tamanho correto, ex: 120x156 px para o herói).
- Pasta `sounds/` — efeitos sonoros do jogo.
- Pasta `music/` — música de fundo.

## Como rodar

1. **Instale o PgZero**:
    ```bash
    pip install pgzero
    ```
2. **Execute o jogo**:
    ```bash
    pgzrun main.py
    ```
3. **A janela abrirá com o menu principal**. Siga as instruções na tela!

## Regras do projeto (atendidas)

- Apenas `pgzero`, `math`, `random` e `pygame.Rect` foram utilizados.
- Sem uso de `pygame` (exceto para o `Rect`).
- Não é feita nenhuma transformação dinâmica no tamanho das imagens pelo código — os sprites já vêm prontos nos tamanhos ideais.
- Todas as animações de sprites são feitas trocando imagens no Actor.
- Código 100% original, organizado e documentado.
- Todas as mecânicas implementadas: menu principal, música, sons, inimigos animados e botões visuais.
- Variáveis, funções e classes nomeadas em inglês, seguindo PEP8.

## Dicas

- Para alterar o tamanho do herói ou inimigos, **redimensione as imagens** (PNG) manualmente e salve na pasta `images/`.
- Certifique-se de que os ícones (`icon_unmuted.png`, `icon_muted.png`, `icon_pause.png`, `icon_play.png`) estão em torno de 44x44 px.

## Créditos

Desenvolvido por: Wander 

---

