## script lin_rls.R
##
rm(list=ls())
par(ask=TRUE)
n<-2;
sigma <- 0.05

rls<-function(x,y,t,P,mu=1){
  P.new <- (P-(P%*%x%*%x%*%P)/as.numeric(1+x%*%P%*%x))/mu
  ga <- P.new%*%x
  epsi <- y-x%*%t
  t.new<-t+ga*as.numeric(epsi)
  list(t.new,P.new)
}

data <- read.csv("./data/A2Benchmark/synthetic_2.csv")
X <- data$value
N <- length(X)
time <- c(1:N)

# y<-sin(X)+0.1*rnorm(N)
t<-numeric(3)
P<-500*diag(n+1)
mu<-0.9
variation <- 0
for (i in 3:N){
  rls.step<-rls(c(1, X[c((i-2):(i-1))]),X[i],t,P,mu)
  t<-rls.step[[1]]
  P<-rls.step[[2]]
  pred_value <- cbind(array(1,c(1,1)), t(X[c((i-1):i)]))%*%t
  variation <- (variation*(i-3)+(pred_value-X[i+1])^2)/(i-2)
  up <- qnorm((1-sigma),mean = pred_value,sd = sqrt(variation))
  down <- qnorm(sigma,mean = pred_value,sd = sqrt(variation))
  plot(time[1:i],X[1:i],
       xlim=c(0,1421),
       ylim=c(-1500,3500),
       main=paste("Forgetting factor mu<-",mu))
  
  points(time[i+1],pred_value,col="red")
  points(time[i+1],up, col="blue")
  points(time[i+1],down,col="blue")
}

