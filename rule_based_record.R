library(dplyr)
library(data.table)
library(ggplot2)

records <- 
  fread('new_close_ratios.csv', stringsAsFactors = F) %>% 
  .[, !c('V1'), with = F]

records %>% 
  ggplot(aes(x = cut_off, y = new_ratio)) +
  geom_line(color = "grey") +
  geom_point(shape = 21, color = "black", fill = "#69b3a2", size = 2) +
  theme_bw() +
  ggtitle("Evolution of close ratio") +
  xlab("Cut off days") +
  ylab("Close ratio, %")
