# Image GeoLocator - Geolocalização de Imagens com IA

**Descubra onde uma foto foi tirada usando metadados EXIF e Inteligência Artificial.**

Um projeto educativo em Python que combina extração de metadados, geolocalização por IA e integração com Google Maps. Perfeito para estudos de visão computacional, processamento de imagens e APIs.

---

##  Funcionalidades

- **Seleção fácil de imagem** através de janela gráfica (Tkinter)
- **Extração completa de metadados EXIF** (incluindo GPS)
- **Geolocalização por IA** usando Picarta (retorna 3 locais possíveis com confiança)
- **Geração automática de links do Google Maps**
- **Interface amigável** com mensagens claras e tratamento de erros
- **Código bem comentado** e organizado para estudos

---

---

##  Pré-requisitos

- Python 3.8 ou superior
- Conta no [Picarta.ai](https://picarta.ai) (plano gratuito disponível)

---

##  Instalação

Instale as dependências:

Bashpip install pillow geopy picarta

Configure o Token da API Picarta:
Acesse https://picarta.ai/api
Gere seu token
Cole no arquivo main.py na variável TOKEN

Como Usar

Execute o programa:

Clique em OK e selecione a foto que deseja analisar.
O programa irá:
Mostrar todos os metadados EXIF
Exibir coordenadas GPS (se existirem)
Retornar 3 locais possíveis com IA
Gerar links diretos para o Google Maps



 Tecnologias Utilizadas

PIL (Pillow) – Leitura e extração de EXIF
Tkinter – Interface gráfica nativa
Picarta AI – Geolocalização por visão computacional
Geopy – Reverse geocoding (endereços)
Google Maps – Links de visualização
