# Instalação dos pacotes
install.packages("dplyr")
install.packages("tidyverse")

# Aplicando as Bibliotecas
library(nycflights13)
library(tidyverse)

# Visualizando os dados em formato simples
nycflights13::flights
nycflights13::airlines
nycflights13::airports
nycflights13::planes
nycflights13::weather

# Visualizando as documentações das bases de dados
?flights
?airlines
?airports
?planes
?weather

# Visualizando os dados de forma mais elegante
View(flights)
View(airlines)
View(airports)
View(planes)
View(weather)

# Filtrando os Vôos realizados em 1 de janeiro
filter(flights, month == 1, day == 1)

# Salvando a filtragem de dados em uma variável
jan1 <- filter(flights, month == 1, day == 1)

# Imprimindo e salvando o resultado da filtragem de voos realizados em 25 de dezembro
(dec25 <- filter(flights, month == 12, day == 25))

# Erros ocorridos pelo uso de = ao invés de ==
filter(flights, month = 1)
sqrt(2) ^ 2 == 2
1 / 49 * 49 == 1

# Utilizando o Near para obter valores com número finito de dígitos
near(sqrt(2)^2, 2)
near(1 / 49 * 49, 1)

# Filtrando os voos que partiram em novembro e dezembro
filter(flights, month == 11 | month == 12)

# Filtrando os voos que partiram em novembro e dezembro e salvando em uma variavel
nov_dec <- filter(flights, month %in% c(11, 12))

# Filtrando voos que não tenham atrasado (na chegada ou na partida) por mais de duas horas
filter(flights, !(arr_delay > 120 | dep_delay > 120))
filter(flights, arr_delay <= 120, dep_delay <= 120)
