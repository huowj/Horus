# file information

# "./data/A1Benchmark/real_[1-67].csv"
# "./data/A2Benchmark/synthetic_[1-100].csv"
# [1] "timestamp"  "value"      "is_anomaly"

# "./data/A3Benchmark/A3Benchmark-TS[1-100].csv"
# "./data/A4Benchmark/A4Benchmark-TS1[1-100].csv
# [1] "timestamps"   "value"        "anomaly"      "changepoint"  "trend"       
# [6] "noise"        "seasonality1" "seasonality2" "seasonality3"

# plot
library(quantmod)
library(ggplot2)
library(Cairo)

data1 <- read.csv("./data/A1Benchmark/real_1.csv")
head(data1)
# for data A1Benchmark
plot1 <- function(n){
  data1 <- read.csv(paste("./data/A1Benchmark/real_",as.character(n),".csv",sep=""))
  data2 <- data1[data1$is_anomaly==1,]
  p1 <- ggplot(data1,aes(timestamp,value))
  p1+geom_line()+geom_point(aes(timestamp,value),data=data2,color=alpha("red",1))
}
plot1(5)

for (i in 1:67){
  data1 <- read.csv(paste("./data/A1Benchmark/real_",as.character(i),".csv",sep=""))
  data2 <- data1[data1$is_anomaly==1,]
  p1 <- ggplot(data1,aes(timestamp,value))+labs(title=paste("real_",i,sep=""))+geom_line()+geom_point(aes(timestamp,value),data=data2,color=alpha("red",1))
  ggsave(paste("./plot/A1plot/plot",i,".jpg",sep=""),p1)
}

# for data A2Benchmark
plot2 <- function(n){
  data1 <- read.csv(paste("./data/A2Benchmark/synthetic_",as.character(n),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$is_anomaly==1,]
  p1 <- ggplot(data1,aes(time,value))
  p1+geom_line()+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))
}
plot2(2)

for (i in 1:100){
  data1 <- read.csv(paste("./data/A2Benchmark/synthetic_",as.character(i),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$is_anomaly==1,]
  p1 <- ggplot(data1,aes(time,value))+labs(title=paste("synthetic_",i,sep=""))+geom_line()+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))
  ggsave(paste("./plot/A2plot/plot",i,".jpg",sep=""),p1)
}

# for data A3Benchmark
plot3 <- function(n){
  data1 <- read.csv(paste("./data/A3Benchmark/A3Benchmark-TS",as.character(n),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$anomaly==1,]
  p1 <- ggplot(data1,aes(time,value))
  p1+geom_line(aes(time,value),data=data1,color=alpha("black",0.5))+geom_line(aes(time,trend),data=data1,color=alpha("white",0.5))+geom_line(aes(time,noise),data=data1,color=alpha("green",0.5))+geom_line(aes(time,seasonality1),data=data1,color=alpha("yellow",0.5))+geom_line(aes(time,seasonality2),data=data1,color=alpha("blue",0.5))+geom_line(aes(time,seasonality3),data=data1,color=alpha("purple",0.5))+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))
}
plot3(3)

for (i in 1:100){
  data1 <- read.csv(paste("./data/A3Benchmark/A3Benchmark-TS",as.character(i),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$anomaly==1,]
  p1 <- ggplot(data1,aes(time,value))+labs(title=paste("A3TS_",i,sep=""))+geom_line(aes(time,value),data=data1,color=alpha("black",0.5))+geom_line(aes(time,trend),data=data1,color=alpha("white",0.5))+geom_line(aes(time,noise),data=data1,color=alpha("green",0.5))+geom_line(aes(time,seasonality1),data=data1,color=alpha("yellow",0.5))+geom_line(aes(time,seasonality2),data=data1,color=alpha("blue",0.5))+geom_line(aes(time,seasonality3),data=data1,color=alpha("purple",0.5))+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))
  ggsave(paste("./plot/A3plot/plot",i,".jpg",sep=""),p1)
}

# for data A4Benchmark
plot4 <- function(n){
  data1 <- read.csv(paste("./data/A4Benchmark/A4Benchmark-TS",as.character(n),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$anomaly==1,]
  data3 <- data1[data1$changepoint==1,]
  p1 <- ggplot(data1,aes(time,value))
  p1+geom_line(aes(time,value),data=data1,color=alpha("black",0.5))+geom_line(aes(time,trend),data=data1,color=alpha("white",0.5))+geom_line(aes(time,noise),data=data1,color=alpha("green",0.5))+geom_line(aes(time,seasonality1),data=data1,color=alpha("yellow",0.5))+geom_line(aes(time,seasonality2),data=data1,color=alpha("blue",0.5))+geom_line(aes(time,seasonality3),data=data1,color=alpha("purple",0.5))+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))+geom_point(aes(time,value),data=data3,color=alpha("pink",0.5))
}
plot4(4)


for (i in 1:100){
  data1 <- read.csv(paste("./data/A4Benchmark/A4Benchmark-TS",as.character(i),".csv",sep=""))
  time <- index(data1)
  data1 <- cbind(time,data1)
  data2 <- data1[data1$anomaly==1,]
  data3 <- data1[data1$changepoint==1,]
  p1 <- ggplot(data1,aes(time,value))+labs(title=paste("A4TS_",i,sep=""))+geom_line(aes(time,value),data=data1,color=alpha("black",0.5))+geom_line(aes(time,trend),data=data1,color=alpha("white",0.5))+geom_line(aes(time,noise),data=data1,color=alpha("green",0.5))+geom_line(aes(time,seasonality1),data=data1,color=alpha("yellow",0.5))+geom_line(aes(time,seasonality2),data=data1,color=alpha("blue",0.5))+geom_line(aes(time,seasonality3),data=data1,color=alpha("purple",0.5))+geom_point(aes(time,value),data=data2,color=alpha("red",0.5))+geom_point(aes(time,value),data=data3,color=alpha("pink",0.5))
  ggsave(paste("./plot/A4plot/plot",i,".jpg",sep=""),p1)
}