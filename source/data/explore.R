library(tidyverse)
options(digits=3)

rps_data <- read.csv('data/intermediate/rps_data_long.csv')


#
## Looking at Data quality / inputs
#

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



#
## Looking at patterns in play
#

rps_data12 <- read.csv('data/intermediate/rps_data_12_past_moves.csv')

str(rps_data12)

# What are the most common throws?
# -> Rock > Paper > Scissors.
prop.table(table(rps_data12$throw))


# What are the most common first moves?
# -> Scissors is by far the least common first throw.
rps_data12 %>% filter(round == 1) %>% select(throw) %>% table() %>% prop.table()


# What is the most common move based on the last move?
prop.table(table(throw=rps_data12$throw, last_throw=rps_data12$minus1))

# Columns add up to 1 (i.e., what is the prob of each throw given you know their last)
# -> Rock is still played most commonly after both Paper and Rock.
# -> Paper is most commonly played after scissors.
# -> Players are slightly less likely to play paper after rock, or scissors after scissors.
prop.table(table(throw=rps_data12$throw, last_throw=rps_data12$minus1), margin = 2)


# Prob of each throw given their last throw AND whether they won.

# Your last throw was Rock:
# -> If you lost or drew, you are likely to throw rock again.
# -> If you drew, you are unlikely to throw paper. 
# -> If you won you are unlikely to throw Rock again.
temp <- rps_data12 %>% filter(minus1 == 1)
prop.table(table(temp %>% select(throw, won_minus1)), 2)

# Your last throw was paper:
# -> If you lost or drew, you are unlikely to throw scissors and may throw paper or rock.
# -> If you won, you are unlikely to stay Paper, however.
temp <- rps_data12 %>% filter(minus1 == 2)
prop.table(table(temp %>% select(throw, won_minus1)), 2)

# Your last throw was scissors:
# If you win you are unlikely to play scissors again.
temp <- rps_data12 %>% filter(minus1 == 3)
prop.table(table(temp %>% select(throw, won_minus1)), 2)

