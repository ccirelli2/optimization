https://rdrr.io/cran/GPareto/man/easyGParetoptim.html

library(GPareto)




# Not run: 
set.seed(25468)
n_var <- 2 
fname <- GPareto::ZDT3
lower <- rep(0, n_var)
upper <- rep(1, n_var)

#---------------------------------------------------------------------------
# 1- Expected Hypervolume Improvement optimization, using pso
#---------------------------------------------------------------------------
res <- GPareto::easyGParetoptim(fn=fname, lower=lower, upper=upper, budget=15, 
                       control=list(method="EHI", inneroptim="pso", maxit=20))
par(mfrow=c(1,2))
plotGPareto(res)
title("Pareto Front")
plot(res$history$X, main="Pareto set", col = "red", pch = 20)
points(res$par, col="blue", pch = 17)