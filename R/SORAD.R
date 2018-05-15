
#read data
data <- read.csv("./data/A2Benchmark/synthetic_2.csv")

#define function
rls<-function(x,y,t,P,mu=1){
  P.new <- (P-(P%*%x%*%x%*%P)/as.numeric(1+x%*%P%*%x))/mu
  ga <- P.new%*%x
  epsi <- y-x%*%t
  t.new<-t+ga*as.numeric(epsi)
  list(t.new,P.new)
}

