# spotify2mp3

Ferramenta de linha de comando para obter os metadados de uma faixa, álbum ou playlist do Spotify e criar arquivos MP3 a partir de uma fonte de áudio pública.

> Use somente para conteúdo que você possui ou tem autorização para baixar.

## Pré-requisitos

O projeto foi validado no Windows com Python 3.12. Você precisa de:

- [Python 3.12](https://www.python.org/downloads/)
- [Git](https://git-scm.com/download/win)
- [FFmpeg](https://ffmpeg.org/download.html)
- Uma conta no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

No PowerShell, é possível instalar as três ferramentas de uma vez com o Windows Package Manager:

```powershell
winget install --id Python.Python.3.12 -e
winget install --id Git.Git -e
winget install --id Gyan.FFmpeg -e
```

Feche e abra um novo PowerShell. Confirme que as ferramentas estão disponíveis:

```powershell
python --version
git --version
ffmpeg -version
```

Se `python` não for encontrado mesmo após a instalação, use diretamente o executável padrão do instalador:

```powershell
& "$env:LocalAppData\Programs\Python\Python312\python.exe" --version
```

Em um computador corporativo, o `winget` pode ser bloqueado pela política da empresa. Nesse caso, peça ao TI para instalar Python, Git e FFmpeg; não tente contornar as permissões do equipamento.

## Instalação

Clone o repositório e entre na pasta do projeto:

```powershell
git clone https://github.com/lucasoalima/spotify2mp3.git
cd spotify2mp3
```

Crie um ambiente isolado e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configurar o Spotify

Na primeira execução, o programa pedirá o `Client ID` e o `Client Secret` de um aplicativo criado no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

1. Acesse o Dashboard e crie um aplicativo.
2. Em **Redirect URIs**, cadastre exatamente `http://127.0.0.1:5000/callback`.
3. Copie o `Client ID` e o `Client Secret` nas configurações do aplicativo.
4. Execute um comando do projeto e informe os dois valores quando forem solicitados.

As credenciais são gravadas apenas em `tekore_cfg.ini` neste computador. Esse arquivo já está no `.gitignore`: não o envie ao GitHub nem o compartilhe.

## Baixar uma playlist pública

Copie a URL da playlist pelo Spotify e execute:

```powershell
.\.venv\Scripts\python.exe .\spotify2mp3.py -p "https://open.spotify.com/playlist/SUA_PLAYLIST_ID"
```

Os arquivos serão gravados em `downloads\playlists\NOME_DA_PLAYLIST`.

### Outros comandos

```powershell
# Uma faixa
.\.venv\Scripts\python.exe .\spotify2mp3.py -s "https://open.spotify.com/track/SUA_FAIXA_ID"

# Um álbum
.\.venv\Scripts\python.exe .\spotify2mp3.py -a "https://open.spotify.com/album/SEU_ALBUM_ID"

# Qualidade desejada: low, medium, high ou um bitrate entre 48000 e 256000
.\.venv\Scripts\python.exe .\spotify2mp3.py -p "URL_DA_PLAYLIST" --quality high

# Ajuda de todos os parâmetros
.\.venv\Scripts\python.exe .\spotify2mp3.py --help
```

## Conteúdo privado e músicas curtidas

O acesso a playlists privadas e músicas curtidas requer login OAuth no navegador. O Spotify exige que a URL de retorno do aplicativo esteja previamente cadastrada e corresponda exatamente à URL usada pelo programa. Consulte as [regras de Redirect URI](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri) e o [fluxo de autorização](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) antes de usar `--login`.

## Solução de problemas

| Problema | Como resolver |
| --- | --- |
| `python` ou `py` não foi encontrado | Feche e reabra o PowerShell. Se necessário, use o caminho de Python mostrado em Pré-requisitos. |
| `ffmpeg` não foi encontrado | Instale o FFmpeg, feche e reabra o PowerShell e execute `ffmpeg -version`. |
| Erro de certificado ao pesquisar áudio | Mantenha as dependências atualizadas com `pip install -r requirements.txt`; o projeto usa os certificados confiáveis do Windows. |
| A empresa bloqueia instalação de programas | Solicite a instalação ao time de TI. |

## Créditos

Projeto modernizado a partir de [couldbejake/spotify2mp3](https://github.com/couldbejake/spotify2mp3).
