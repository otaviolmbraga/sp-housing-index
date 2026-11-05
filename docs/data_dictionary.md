# Data dictionary — ITBI transaction microdata

Column reference for `itbi_compilado.csv.gz` (the transaction microdata attached to
the latest [GitHub Release](../../releases/latest)). The file is a cleaned version of
the ITBI property-transfer-tax records published by the City of São Paulo. Each row is
one reported transaction. Monetary values are in Brazilian reais (BRL); areas in square
metres (m²).

> Dicionário de dados (PT). Cada linha é uma transação reportada no ITBI. Valores
> monetários em reais (R$); áreas em metros quadrados (m²).

| # | Column | English | Português |
|---|--------|---------|-----------|
| 1 | `sql` | Cadastral property ID (Setor-Quadra-Lote), the IPTU registration code | Identificador cadastral do imóvel (Setor-Quadra-Lote), código de inscrição no IPTU |
| 2 | `logradouro` | Street name | Nome do logradouro |
| 3 | `numero` | Street number | Número |
| 4 | `complemento` | Address complement (unit/apartment) | Complemento do endereço (unidade/apartamento) |
| 5 | `bairro` | Neighbourhood | Bairro |
| 6 | `referencia` | Address reference / landmark | Referência de endereço |
| 7 | `cep` | Postal code (CEP) | CEP |
| 8 | `natureza_transacao` | Nature of the transaction (e.g. "1.Compra e venda" = purchase & sale) | Natureza da transação (ex.: "1.Compra e venda") |
| 9 | `valor_declarado` | Declared transaction value (BRL) | Valor declarado da transação (R$) |
| 10 | `data_transacao` | Transaction date | Data da transação |
| 11 | `valor_venal` | Assessed (venal) value used for tax (BRL) | Valor venal de referência (R$) |
| 12 | `proporcao_transmitida` | Share of the property transferred (%) | Proporção transmitida do imóvel (%) |
| 13 | `valor_venal_proporcional` | Assessed value of the transferred share (BRL) | Valor venal proporcional à parte transmitida (R$) |
| 14 | `base_calculo` | ITBI tax calculation base (BRL) | Base de cálculo do ITBI (R$) |
| 15 | `tipo_financiamento` | Financing type, if any | Tipo de financiamento, se houver |
| 16 | `valor_financiado` | Financed amount (BRL) | Valor financiado (R$) |
| 17 | `cartorio` | Registry office (cartório) | Cartório de registro |
| 18 | `matricula` | Property registration (matrícula) number | Número da matrícula do imóvel |
| 19 | `situacao_sql` | Status of the SQL cadastral record (e.g. "Ativo Predial") | Situação do cadastro SQL (ex.: "Ativo Predial") |
| 20 | `area_terreno` | Land / lot area (m²) | Área do terreno (m²) |
| 21 | `testada` | Lot frontage (m) | Testada do lote (m) |
| 22 | `fracao_ideal` | Ideal fraction (the unit's share of the land) | Fração ideal (participação da unidade no terreno) |
| 23 | `area_construida` | Built (constructed) area (m²) | Área construída (m²) |
| 24 | `uso_iptu` | IPTU land-use code | Código de uso do IPTU |
| 25 | `descricao_uso_iptu` | IPTU land-use description | Descrição do uso do IPTU |
| 26 | `padrao_iptu` | IPTU construction-standard code | Código do padrão construtivo do IPTU |
| 27 | `acc_iptu` | Aggregated IPTU use grouping (broad building-use category, e.g. "OFICINA, POSTO DE SERVIÇO, ARMAZÉM/DEPÓSITO, INDÚSTRIA") | Agrupamento de uso do IPTU (categoria ampla de uso do imóvel) |
| 28 | `ano_construcao` | Year of construction | Ano de construção |
| 29 | `year` | Transaction year | Ano da transação |
| 30 | `month` | Transaction month (1–12) | Mês da transação (1–12) |
| 31 | `setor` | SQL sector (first segment of `sql`) | Setor do SQL (primeiro bloco do `sql`) |
| 32 | `quadra` | SQL block | Quadra do SQL |
| 33 | `lote` | SQL lot | Lote do SQL |
| 34 | `digito_lote` | SQL lot check digit | Dígito verificador do lote |

## Notes

- **Coverage / cobertura:** the file spans 2006–2025. The repeat-sales index (IIVR-SP)
  uses only the subset of properties (`sql`) observed in at least two transactions, with
  a minimum 3-year holding period between the two sales.
- **Cleaning / tratamento:** this is a cleaned derivative of the original municipal
  records and may contain inaccuracies. Use at your own discretion.
- `acc_iptu` is an aggregated use category derived from the IPTU classification;
  treat it as indicative rather than an official field.
