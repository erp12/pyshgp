library(plyr)
library(dplyr)
library(ggplot2)
library(plotly)

run_id_counter <- 0

lexicase_file_names <- list.files("/Users/mm94978/Google_Drive/Research/pysh/testing_lexicase/run_logs", pattern = "lexicase", full=TRUE)
lexicase_files <- lapply(lexicase_file_names, function(foo) {
  temp <- read.csv(foo, header = TRUE)
  temp$run_id <- run_id_counter
  run_id_counter <<- run_id_counter + 1
  temp
})
lexicase_df <- rbind.fill(lexicase_files)
lexicase_df$selection_method <- 'lexicase'

tournament_file_names <- list.files("/Users/mm94978/Google_Drive/Research/pysh/testing_lexicase/run_logs", pattern = "tournament", full=TRUE)
tournament_files <- lapply(tournament_file_names, function(foo) {
  temp <- read.csv(foo, header = TRUE)
  temp$run_id <- run_id_counter
  run_id_counter <<- run_id_counter + 1
  temp
})
tournament_df <- rbind.fill(tournament_files)
tournament_df$selection_method <- 'tournament'

multiplexer_runs_df <- rbind(lexicase_df, tournament_df)
multiplexer_runs_df<- group_by(multiplexer_runs_df, run_id)

### Plotting ###

p <- ggplot(multiplexer_runs_df,
            aes(x = gen, 
                y = avg,
                color = selection_method,
                group = run_id)) +
  geom_line() +
  #geom_smooth(size = 2) +
  theme_bw() +
  theme(legend.position="top", legend.title=element_blank()) +
  ggtitle("Multiplexer Problem Lexicase Vs. Tournament") +
  labs(x = "Generation", y = "Percent Cases Passed")
p

#ggplotly(p)

