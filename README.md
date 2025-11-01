# Desafio-dados

1. Objetivo
Tratar e padronizar a base "Base_Membros_Desempenho" para garantir consistência nas
colunas de senioridade, avaliações e engajamento, além de enriquecer os dados com um
score de desempenho e um status de membro.
2. Colunas alvo
- Nivel_Senioridade
- Avaliacao_Tecnica
- Avaliacao_Comportamental
- Engajamento_PIGs
3. Passo a passo do tratamento
3.1 Leitura do arquivo
O arquivo foi carregado em formato Excel (.xlsx). O script tenta mapear automaticamente os
nomes das colunas mesmo se houver pequenas variações no cabeçalho.
3.2 Padronização de Nivel_Senioridade
Problema: a coluna continha variações como "Jr", "P", "pleno", "N/D", "senior", entre outras.
Solução aplicada:
- Normalização textual (minusculizar, remover espaços).
- Mapeamento de variações para três valores padrão: "Júnior", "Pleno" e "Sênior".
- Valores não identificáveis (ex.: "N/D") foram transformados em NaN e, em seguida,
preenchidos com a moda (valor mais frequente) da coluna.
3.3 Padronização de Avaliacao_Tecnica e Avaliacao_Comportamental
Problema: as colunas continham valores com vírgula ou ponto decimal (ex.: "7,5" ou "8.5"),
strings e NaN.
Solução aplicada:
- Substituição de vírgula por ponto para conversão correta para float.
- Conversão dos valores para numérico (float).
- Preenchimento de valores nulos com a média aritmética da respectiva coluna.
- Garantia de que os valores fiquem no intervalo [0, 10] usando clipping.
3.4 Tratamento de Engajamento_PIGs
Problema: representado como texto (ex.: "90%", "75", "N/A") e mistura de formatos.
Solução aplicada:
- Remoção de espaços e conversão de vírgula para ponto.
- Se houver "%" convertemos para decimal (ex.: "90%" -> 0.9).
- Valores numéricos maiores que 1 são interpretados como percentuais e divididos por 100
(ex.: 85 -> 0.85).
- Nulos foram preenchidos com a média aritmética da coluna resultante.
- Valores foram limitados ao intervalo [0, 1].
3.5 Cálculo do Score_Desempenho
Fórmula utilizada:
Score_Desempenho = (Avaliacao_Tecnica * 0.5) + (Avaliacao_Comportamental * 0.5)
A coluna foi adicionada ao DataFrame como um float representando a média ponderada das
duas avaliações.
3.6 Criação de Status_Membro
Critério:
- "Em Destaque" se Score_Desempenho >= 7.0 e Engajamento_PIGs >= 0.8
- Caso contrário: "Padrão"
A coluna Status_Membro foi adicionada com esses rótulos.
4. Saídas geradas
Foram gerados os seguintes arquivos na pasta de trabalho:
- tratamento_base.py (script Python executável)
- Base_Membros_Desempenho_tratada.csv (CSV com vírgula decimal)
- Base_Membros_Desempenho_tratada.xlsx (Excel)
5. Estatísticas principais (após tratamento)
- Média Avaliação Técnica: 7.76
- Média Avaliação Comportamental: 7.73
- Média Engajamento: 0.816
- Membros Em Destaque: 167
- Membros Padrão: 86
