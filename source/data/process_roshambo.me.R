library(tidyverse)
library(readxl)

winner <- function(input1, input2){
    if(input1 == 0) return(NA)
    if(input2 == 0) return(NA)

    if(input1 == 1){    
        ifelse(input2 == 1, return(0),
        ifelse(input2 == 2, return(-1),
        ifelse(input2 == 3, return(1))))
    } else if(input1 == 2){
        ifelse(input2 == 1, return(1),
        ifelse(input2 == 2, return(0),
        ifelse(input2 == 3, return(-1))))
    } else if(input1 == 3){
        ifelse(input2 == 1, return(-1),
        ifelse(input2 == 2, return(1),
        ifelse(input2 == 3, return(0))))
    }
}

winner <- function(input1, input2){
    outcome = c(1:length(input1))
    ifelse(input1 == 0, return(NA),
    ifelse(input2 == 0, return(NA),
    ifelse(input1 == 1,    
        ifelse(input2 == 1, return(0),
        ifelse(input2 == 2, return(-1),
        ifelse(input2 == 3, return(1),
    ifelse(input1 == 2,    
        ifelse(input2 == 1, return(1),
        ifelse(input2 == 2, return(0),
        ifelse(input2 == 3, return(-1),
    ifelse(input1 == 2,    
        ifelse(input2 == 1, return(-1),
        ifelse(input2 == 2, return(1),
        ifelse(input2 == 3, return(0)))))))))))))))
}



rps_data <- read_xlsx('../../data/raw/roshambo.me.xlsx')

str(rps_data)
rps_data <- rps_data %>% mutate_all(
    player_one_throw = factor(player_one_throw),
    player_two_throw = factor(player_two_throw)
    )

# Add row for who won.
rps_data <- rps_data %>% mutate(
    player_one_win = apply( winner(player_one_throw, player_two_throw),
    player_two_throw = -(player_one_win)
)


summary(rps_data$player_one_throw)
summary(rps_data$player_two_throw)    # Why is the player 2 forfeit rate 8x higher?


# Summarize by game
rps_game_data <- rps_data %>%
    group_by(game_id) %>%
    summarize(rounds_per_game = length(game_round_id))
              
              
tapply(rps_data, FUN=summary)
