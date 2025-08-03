# ROGUELIKE LUAN PYTHON 

Este projeto foi desenvolvido como solução para o teste técnico do processo seletivo de tutores de Python, 
conforme especificado no arquivo.

# SOBRE O JOGO

Um jogo roguelike simples, baseado em grade (grid), com visão de cima, animação de sprites para o jogador e
inimigos, música de fundo e efeitos sonoros. Inclui um menu principal interativo e mecânica de movimentação
clássica por células.

# REQUISITOS ATENDIDOS

Uso apenas das bibliotecas permitidas: pgzrun, random e pgzero.rect (Rect do Pygame permitido).
Gênero roguelike com movimentação em grade.
Menu principal com botões clicáveis: Iniciar, Som On/Off, Sair.
Música de fundo e efeito sonoro para o movimento do personagem.
Múltiplos inimigos com movimentação aleatória.
Animação de sprites para todos os personagens (andar/parado).
Classes e nomes claros, seguindo PEP8.
Código original e autoral.
Jogo funcional e sem bugs conhecidos.


# COMO RODAR O JOGO

REQUISITOS

    Python 3.7+ instalado.
    Instale o PgZero:
     bash
     pip install pgzero
    
 
ESTRUTURA

Roguelike Luan Python/
├── images/
│ └── (sprites dos personagens, inimigos e background)
├── music/
│ └── bg_music.ogg # música de fundo do menu e do jogo
├── sounds/
│ └── move.wav # efeito sonoro dos passos do personagem
├── main.py
└── README.md


EXECUTANDO

No terminal, navegue até a pasta do projeto e execute:
  bash
  pgzrun main.py

 O menu principal aparecerá; use o mouse para clicar nos botões.


# CONTROLES 

Setas do teclado: Mover o personagem nas 4 direções.
Mouse: Navega e seleciona opções do menu.


# ASSETS 

 Sprites dos personagens, inimigos: (https://craftpix.net/)
 Backgroud: (Usuario do reddit "marculino u/Unfair_Land7732")
 Música de fundo: (https://www.youtube.com/watch?v=ggz7feykOGo&list=RDggz7feykOGo&start_radio=1)
 Efeito sonoro dos passos: (https://www.youtube.com/watch?v=uzOuZVy1nmg)

# OBSERVAÇÃO

 O efeito sonoro de passos só toca enquanto o personagem estiver se movendo e para imediatamente ao parar.
 A música de fundo pode ser pausada/retomada no menu principal.
 Inimigos se movem aleatoriamente pelo grid do mapa.
 Animações de sprite são feitas alternando frames de imagem para movimento e idle.


# AUTOR

 Luan Maciel(https://www.linkedin.com/in/95luanmaciel)  
 Email: 95luanmaciel@gmail.com


# LICENÇA

Este projeto foi desenvolvido exclusivamente para fins de avaliação técnica, 
não devendo ser publicado ou utilizado comercialmente sem permissão.
