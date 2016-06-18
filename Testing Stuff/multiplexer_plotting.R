library(dplyr)
library(ggplot2)
library(plotly)

lexicase_runs <- merge(multiplexer_lexicase_log, 
                       multiplexer_lexicase_log_2, 
                       by = 'gen',
                       suffixes = c("_run1","_run2"))
lexicase_runs$selection_method <- 'lexicase'

tournament_runs <- merge(multiplexer_tournament_log, 
                         multiplexer_tournament_log_2, 
                         by = 'gen',
                         suffixes = c("_run1","_run2"))
tournament_runs$selection_method <- 'tournament'

multiplexer_runs <- rbind(lexicase_runs,
                          tournament_runs)

### Plotting ###

p <- ggplot(multiplexer_runs,
            aes(x = gen, y = avg_run1, color = selection_method)) +
  geom_line(size = 1.5) + 
  geom_line(aes(y = avg_run2), size = 1.5) +
  geom_line(aes(y = max_run1)) +
  geom_line(aes(y = max_run2)) +
  theme_bw() +
  theme(legend.position="top", legend.title=element_blank()) +
  ggtitle("Multiplexer Problem Lexicase Vs. Tournament") +
  labs(x = "Generation", y = "Percent Cases Passed")
p

#ggplotly(p)
