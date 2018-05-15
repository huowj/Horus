# file information

# "./data/A1Benchmark/real_[1-67].csv"
# "./data/A2Benchmark/synthetic_[1-100].csv"
# [1] "timestamp"  "value"      "is_anomaly"

# "./data/A3Benchmark/A3Benchmark-TS[1-100].csv"
# "./data/A4Benchmark/A4Benchmark-TS1[1-100].csv
# [1] "timestamps"   "value"        "anomaly"      "changepoint"  "trend"       
# [6] "noise"        "seasonality1" "seasonality2" "seasonality3"

#example
install.packages("devtools")
devtools::install_github("twitter/AnomalyDetection")
library(AnomalyDetection)

help(AnomalyDetectionTs)
help(AnomalyDetectionVec)

data(raw_data)
res = AnomalyDetectionTs(raw_data, max_anoms=0.02, direction='both', plot=TRUE)
res$plot

AnomalyDetectionVec(raw_data[,2], max_anoms=0.02, period=100, direction='both',
                    only_last=TRUE, plot=TRUE)

AnomalyDetectionTs(data, max_anoms=0.02, period=1420, plot=TRUE)

#yahoo
real_data <- read.csv("./data/A1Benchmark/real_2.csv")
AnomalyDetectionVec(real_data[,2],max_anoms = 0.01, period = 14, direction = 'both',plot = TRUE)