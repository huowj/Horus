


x <- rlnorm(1000000000,meanlog = 3,sdlog = 2)
hist(x,probability = TRUE,30)
curve(dlnorm,add=TRUE)
mean(x)
sd(x)
(sd(x)^2)/(mean(x)^2)
exp(4)-1


s = seq(1,10,by=0.01)
plot(dlnorm(s,meanlog = 2,sdlog = 0.1),type="l")