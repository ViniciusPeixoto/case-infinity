# Desafio Técnico Infinity Vision
### Vaga de Desenvolvedor Visão Computacional
Este projeto compara imagens para determinar se elas representam o mesmo produto de supermercado, ou se exibem produtos diferentes. A comparação é feita através da distância cosseno das imagens processadas, e a decisão de validação é feita a partir de um valor limitante. Por fim, as duas imagens são concatenadas e salvas em disco. Todos os parâmetros necessários são lidos de um arquivo YAML de configuração.

## Requisitos
Para executar esse projeto será necessário:
1. [Python](https://www.python.org/downloads) 3.12 ou superior
2. [Poetry](https://python-poetry.org/docs/#installation)

Os arquivos `pyproject.toml` e `poetry.lock` possuem as informações necessárias para que a ferramenta Poetry instale todas as dependências relevantes ao projeto.

## Instalação
Para instalar todas as dependências e deixar a aplicação pronta para execução, basta executar o seguinte comando:
```bash
poetry install
```
## Usando a aplicação
Para a execução correta da aplicação é necessário um arquivo YAML contendo as configurações da execução. Este arquivo possui o seguinte formato:
```yaml
image_a: <path/to/first/image.jpg>
imagem_b: <path/to/second/image.jpg>
threshold: <float>
output_location: <path/to/output/image.jpg>
```
Uma vez que o arquivo existe, basta passá-lo como parâmetro para a chamada da aplicação:
```bash
python infinity.py path/to/settings.yaml
```
## Resultado
Se tudo ocorrer conforme o esperado, o terminal irá exibir a distância cosseno das duas imagens, bem como se os produtos exibidos nela são o mesmo produto ou produtos diferentes quando comparados com o limitante pré estabelecido.

Exemplo de verificação de produtos similares:
```
Distance: 0.26853978633880615
Same product.
```

Exemplo de verificação de produtos diferentes:
```
Distance: 0.33419913053512573
Different products.
```
Também será gerada uma imagem em preto e branco (*grayscale*) resultado da concatenação das duas imagens usadas na comparação. Essa imagem será salva no local indicado pelo campo `output_location` no arquivo YAML. 