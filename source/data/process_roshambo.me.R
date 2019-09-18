library(tidyverse)
library(readxl)

winner <- function(input1, input2){
  ifelse(input1 == 0, NA,
  ifelse(input2 == 0, NA,
  ifelse(input1 == 1,    
    ifelse(input2 == 1, 0,
    ifelse(input2 == 2, -1, 1)),
  ifelse(input1 == 2,    
    ifelse(input2 == 1, 1,
    ifelse(input2 == 2, 0, -1)),
  ifelse(input1 == 3,    
    ifelse(input2 == 1, -1,
    ifelse(input2 == 2, 1, 0)), NA)))))
}

setwd('../../')
rps_raw <- read_xlsx('data/raw/roshambo.me.xlsx')


# Convert throws to factors. 1 is rock, 2 is paper, 3 is scissors, 0 is forfeit.
# rps_data <- rps_raw %>% mutate(
#     player_one_throw = factor(player_one_throw),
#     player_two_throw = factor(player_two_throw)
# )

# Add row for who won.
rps_data <- rps_raw %>% mutate(
    player_one_win = winner(player_one_throw, player_two_throw),
    player_two_win = -(player_one_win)
)

# Convert game_round_id from cumulate to reset for each new game
# Also make it so that round numbers increment up even in the event of a tie
rps_data <- rps_data %>% mutate(
  round = ave(1:nrow(rps_data), game_id, FUN=function(x) 1:length(x) )    # Solution copied from SO https://stackoverflow.com/questions/16092239/r-how-to-add-row-index-to-a-data-frame-based-on-combination-of-factors
)


# Need to convert these data into wide format for learning algorithms.
# For each throw on each side, there should be columns representing the last N moves.
# A more advanced version may also look at the opponent's moves.

rps_p1 <- rps_data %>% 
  mutate(throw = player_one_throw) %>%
  select(game_id, round, throw) 
  
rps_p2 <- rps_data %>% 
  mutate(throw = player_two_throw, game_id = game_id + max(game_id)) %>%
  select(game_id, round, throw)

rps_p1_p2_rbind <- rbind(rps_p1, rps_p2)

# Not super elegant but seems to work.
rps_data_12_past_moves <- rps_p1_p2_rbind %>% 
  mutate(minus1 = ifelse(round > lag(round), lag(throw), NA),
         minus2 = ifelse(round > lag(round), lag(minus1), NA),
         minus3 = ifelse(round > lag(round), lag(minus2), NA),
         minus4 = ifelse(round > lag(round), lag(minus3), NA),
         minus5 = ifelse(round > lag(round), lag(minus4), NA),
         minus6 = ifelse(round > lag(round), lag(minus5), NA),
         minus7 = ifelse(round > lag(round), lag(minus6), NA),
         minus8 = ifelse(round > lag(round), lag(minus7), NA),
         minus9 = ifelse(round > lag(round), lag(minus8), NA),
         minus10 = ifelse(round > lag(round), lag(minus9), NA),
         minus11 = ifelse(round > lag(round), lag(minus10), NA),
         minus12 = ifelse(round > lag(round), lag(minus11), NA))


write_csv(rps_data, 'data/intermediate/rps_data_long.csv')
write_csv(rps_data_12_past_moves, 'data/final/rps_data_12_past_moves.csv')



# Look at distribution of inputs
table(rps_data$player_one_throw)
table(rps_data$player_two_throw)    # Why is the player 2 forfeit rate 8x higher?

# Are most forfeitures on the first round (would make sense if the opponent simply doesn't join the game)?
# Answer: Yes. About 1/3 of first round games are a Player 2 forfeit, vs. just 1% for Player 1.
# After round 1, the rates are similar ~1% (decreases as the # of rounds increases). 
# Round 1 forfeits have nothing to do with the game itself.
rps_forfeitures_per_game <- rps_data %>%
  group_by(round) %>%
  summarize(p1_forfeitures = sum(player_one_throw == 0),
            p2_forfeitures = sum(player_two_throw == 0),
            p1_forfeitures_percent = p1_forfeitures / length(player_one_throw),
            p2_forfeitures_percent = p2_forfeitures / length(player_one_throw))


# % of games that involve forfeits (exclude round 1 forfeits)
# Only 2 games have a forfeit from both players, so we'll ignore overlap
# Only about 1.7% of games past round 1 end in forfeiture, which is low enough to ignore.
sum(rps_forfeitures_per_game$p1_forfeitures[-1] + rps_forfeitures_per_game$p2_forfeitures[-1]) / nrow(rps_data)



# Summarize # of rounds per game
rps_rounds_per_game <- rps_data %>%
  group_by(game_id) %>%
  summarize(rounds_per_game = length(game_round_id),
            player_one_scores = sum(player_one_win, na.rm = T))

table(rps_rounds_per_game$rounds_per_game)
