# 🚀 Jornada Espacial

**Jornada Espacial** é um jogo educativo desenvolvido com **Python** e **Pygame**, projetado para ensinar e divertir visitantes de um planetário.  
Assuma o controle de uma nave espacial, explore o sistema solar e aprenda curiosidades sobre os planetas enquanto se aventura pelo espaço!

## ✨ Recursos

-   Nave controlável com movimentação fluida e sistema de disparos.
-   Arquitetura modular com gerenciamento de estados (menu, gameplay, etc.).
-   Suporte a tela cheia para imersão total.
-   Estrutura pronta para expansão: adição de fases, planetas interativos e quizzes educativos.
-   Código limpo, organizado e preparado para futuras melhorias.

## 🛠️ Tecnologias utilizadas

-   **Python 3.11+**
-   **Pygame**
-   **Arquitetura baseada em State Pattern**
-   **Organização por módulos (config, core, screens, entities)**

## 📂 Estrutura do projeto

/jornada_espacial
├── main.py
├── config/
│ └── settings.py
├── core/
│ └── state_manager.py
├── screens/
│ ├── menu.py
│ └── gameplay.py
├── entities/
│ ├── spaceship.py
│ └── bullet.py
├── assets/
│ ├── images/
│ ├── audio/
│ └── fonts/

## 🎮 Como rodar o jogo

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/jornada-espacial.git
    cd jornada-espacial
    ```

2. Instale as dependências:

    ```bash
    pip install pygame
    ```

3. Execute o jogo:
    ```bash
    python main.py
    ```

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
