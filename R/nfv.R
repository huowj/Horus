library(zoo)
library(forecast)
library(ggplot2)
#forecast
n=2000
noise <- rnorm(n,0,10)
season <- sin(c(1:n)*0.034)*10+50
trend <- c(1:n)*0.01+1
value <- noise+season+trend
plot(noise,type = "l")
plot(season,type = "l")
plot(trend,type = "l")
plot(value,type = "l")
data <- ts(value,start=1,frequency = 365)
df <- stl(data, s.window = "periodic")
plot(df)
fit <- stlf(data)
plot(fit)
write.csv(value,"value.csv")

value <- read.csv("value.csv")
value_anomaly <- value[value$is_anomaly==1,]
p <- ggplot(value,aes(time,x1))+geom_line()+geom_point(aes(time,x1),data=value_anomaly,color=alpha("red",1))
p
data0 <- value[value$is_anomaly==0,]
data <- ts(data0$x1[1:1400],start=1,frequency = 365)
df <- stl(data, s.window = "periodic")
plot(df)
fit <- stlf(data)
plot(fit)
fit1 <- read.csv("fit1.csv")
data1 <- value[1401:2000,]
data1_anomaly <- data1[data1$is_anomaly==1,]
p1 <- ggplot(data1,aes(time,x1))+geom_line()+geom_point(aes(time,x1),data=data1_anomaly,color=alpha("blue",1))
p1

a <- read.csv("a.csv")
a_anomaly <- a[a$is_anomaly==1,]
p1 <- ggplot(a,aes(time,x1))+geom_line()+geom_point(aes(time,x1),data=a_anomaly,color=alpha("red",1))+geom_point(aes(time,x1),data=a_anomaly,sh
p1

#detection
n=1000
noise <- rnorm(n,0,5)+20
season <- sin(c(1:n)*0.034)*0.1
trend <- c(1:n)*0.01
value <- noise+season+trend
plot(value,type = "l")
value[900:930]=rnorm(21,0,5)+80
#value[]=
#value[]=
data_train=value[1:600]
data_test=value[601:1000]
plot(data_train,type="l")
plot(data_test,type="l")
data_train_ts=ts(data_train,start=1,frequency=365)
acf(data_train_ts)
auto.arima(data_train_ts)
plot(value,type="l")
arima1 <- arima(data_train_ts,order=c(2,1,2),method="ML")
arima_forecast=predict(arima1,n.ahead=400,level=c(99))
#plot test data
m=length(data_test)
flag_test=rep(0,m)
for (i in 1:400){
  if(abs(arima_forecast$pred[i]-data_test[i])>30){
    flag_test[i]=1
  }
}
detection <- as.data.frame(cbind(time,data_test,flag_test))
detection1 <- detection[detection$flag_test==1,]
p <- ggplot(detection,aes(time,data_test))+geom_line()+geom_point(aes(time,data_test),data=detection1,color=alpha("red",1))
#plot full data
flag_full <- c(rep(0,n-m),flag_test)
time_full <- c(1:n)
detection_full <- as.data.frame(cbind(time_full,value,flag_full))
detection_full1 <- detection_full[detection_full$flag_full==1,]
p_full <- ggplot(detection_full,aes(time_full,value))+geom_line()+geom_point(aes(time_full,value),data=detection_full1,color=alpha("red",1))
p_full

p_full <- ggplot(,aes(time_full,value))+geom_line()+geom_point(aes(time_full,value),data=detection_full1,color=alpha("red",1))
p_full

plot(df.residual())

plot(noise,type = "l")
plot(season,type = "l")
plot(trend,type = "l")
plot(value,type = "l")
write.csv(value,"value.csv")