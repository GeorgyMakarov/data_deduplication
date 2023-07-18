assign_group <- function(dates, cut_off)
{
  group_list <- c()
  init_group <- 1
  
  if (length(dates) == 1){
    return(group_list)
  } else {
    date_diffs <- c(0, round(diff(dates) / 86400, 0))
    for (i in date_diffs){
      if (i <= cut_off){
        group_list <- c(group_list, init_group)
      } else {
        init_group <- init_group + 1
        group_list <- c(group_list, init_group)
      }
    }
  }
  return(group_list)
}


add_groups_dt <- function(usr, cut_off)
{
  return(usr[, Groups := assign_group(usr[['FlightDate']], cut_off), ])
}


assign_quote <- function(dt, i){
  tmp <- dt[Groups == i, ]
  if (1 %in% unique(tmp[['Sale_Flag']])){
    quotes <- tmp[Sale_Flag == 1, QuoteID]
  } else {
    quotes <- tmp[QuoteCreationDateTime == max(QuoteCreationDateTime), QuoteID]
  }
  return(quotes)
}


find_quotes <- function(dt)
{
  return(
    unlist(
      lapply(
        unique(dt[['Groups']]),
        function(i){assign_quote(dt, i)}
      )
    )
  )
}


iterate_users <- function(raw_data, cut_off)
{
  return(
    unlist(
      lapply(
        unique(raw_data[['UserID']]),
        function(user){
          return(
            add_groups_dt(raw_data[UserID == user, ], cut_off) %>% find_quotes(.)
          )
        }
      )
    )
  )
}


compute_close_ratio <- function(raw_data, cut_off)
{
  quotes <- iterate_users(raw_data, cut_off)
  new_dt <- raw_data[QuoteID %in% quotes, ]
  return(round(sum(new_dt[['Sale_Flag']]) / nrow(new_dt) * 100, 1))
}


deduplicate_data <- function(raw_data, cut_offs)
{
  return(
    unlist(
      lapply(
        setNames(cut_offs, cut_offs),
        function(i){return(compute_close_ratio(raw_data, i))}
      )
    )
  )
}