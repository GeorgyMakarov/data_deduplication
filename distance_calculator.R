invisible(lapply(readLines('dependencies.txt'), library, character.only = T))
source('helpers.R')

raw_data   <- readxl::read_xlsx('raw_data.xlsx') %>% as.data.table()
base_ratio <- round(sum(raw_data[['Sale_Flag']]) / nrow(raw_data) * 100, 1)

raw_data[, DayOfYear := lubridate::yday(raw_data$FlightDate), ]

start_time <- Sys.time()
deduplicate_data(raw_data, seq(100))
end_time <- Sys.time()
duration <- end_time - start_time
sprintf("This program took %s to run", round(duration, 2))
