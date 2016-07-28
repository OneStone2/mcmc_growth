pkgs <- c('doMC', 'Cubist', 'caret')
lapply(pkgs, require, character.only = T)
registerDoMC(core = 7)

analyze_r05 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    }
    else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    r1 <- x[["carb"]]
    r2 <- x[["py"]]
    x <- x[-c(nrow(x)),]
    r1 <- r1[-c(1)]
    r2 <- r2[-c(1)]
    x["post_py"] <- r2
    x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
    x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
    x <- x[, names(x) %in% c("py","post_py","growth","carb","lat","lon")]
    row.names(x) <- 1:nrow(x)

    X <- x[, !names(x) %in% c("growth","py","post_py")]
    Y <- x[,names(x) %in% "growth"]

    groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

    min_mse = Inf
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]

      mdl2 <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl2, newdata = X2)) ^ 2)/length(Y2))
      if (mse < min_mse) min_mse <- mse
    }
    return(min_mse)
}

analyze_r06 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    }
    else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    r1 <- x[["carb"]]
    r2 <- x[["py"]]
    x <- x[-c(nrow(x)),]
    r1 <- r1[-c(1)]
    r2 <- r2[-c(1)]
    x["post_py"] <- r2
    x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
    x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
    x <- x[, names(x) %in% grep("(growth)|(py)|(post_py)|(lat)|(lon)|(carb)|(iv[0123456789.]+)", colnames(x), value=T)]
    row.names(x) <- 1:nrow(x)

    X <- x[, !names(x) %in% c("growth","py","post_py")]
    Y <- x[,names(x) %in% "growth"]

    groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

    min_mse = Inf
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]

      mdl2 <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl2, newdata = X2)) ^ 2)/length(Y2))
      if (mse < min_mse) min_mse <- mse
    }
    return(min_mse)
}

analyze_r07 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    }
    else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    r1 <- x[["carb"]]
    r2 <- x[["py"]]
    r3 <- x[["human_p"]]
    r4 <- x[["human_n"]]
    x <- x[-c(nrow(x)),]
    r1 <- r1[-c(1)]
    r2 <- r2[-c(1)]
    r3 <- r3[-c(1)]
    r4 <- r4[-c(1)]
    x["post_py"] <- r2
    x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
    x["human_p"] <- r3
    x["human_n"] <- r4
    x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
    x <- x[, names(x) %in% grep("(growth)|(py)|(post_py)|(lat)|(lon)|(carb)|(iv[0123456789.]+)|(human_[np])", colnames(x), value=T)]
    row.names(x) <- 1:nrow(x)

    X <- x[, !names(x) %in% c("growth","py","post_py")]
    Y <- x[,names(x) %in% "growth"]

    groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

    min_mse = Inf
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]

      mdl2 <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl2, newdata = X2)) ^ 2)/length(Y2))
      if (mse < min_mse) min_mse <- mse
    }
    return(min_mse)
}

analyze_r08 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    }
    else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    r1 <- x[["carb"]]
    r2 <- x[["py"]]
    r3 <- x[["human_p"]]
    r4 <- x[["human_n"]]
    x <- x[-c(nrow(x)),]
    r1 <- r1[-c(1)]
    r2 <- r2[-c(1)]
    r3 <- r3[-c(1)]
    r4 <- r4[-c(1)]
    x["post_py"] <- r2
    x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
    x["human_p"] <- r3
    x["human_n"] <- r4
    x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
    x <- x[, names(x) %in% grep("(growth)|(py)|(post_py)|(lat)|(lon)|(carb)|(iv[0123456789.]+)|(human_[np])|(elevation)", colnames(x), value=T)]
    row.names(x) <- 1:nrow(x)

    X <- x[, !names(x) %in% c("growth","py","post_py")]
    Y <- x[,names(x) %in% "growth"]

    groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

    min_mse = Inf
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]

      mdl2 <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl2, newdata = X2)) ^ 2)/length(Y2))
      if (mse < min_mse) min_mse <- mse
    }
    return(min_mse)
}

state <- 'ME'
#Change state for whatever you want
N_REP <- 5
print("Including human interaction:")
sum <- 0
for (i in 1:N_REP) {
    sum <- sum + analyze_r05(state=state, human=T)
}
print(paste('[5]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r06(state=state, human=T)
}
print(paste('[6]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r07(state=state, human=T)
}
print(paste('[7]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r08(state=state, human=T)
}
print(paste('[8]', sum / N_REP))
print("Excluding human interaction:")
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r05(state=state, human=F)
}
print(paste('[5]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r06(state=state, human=F)
}
print(paste('[6]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r07(state=state, human=F)
}
print(paste('[7]', sum / N_REP))
sum <- 0
for (i in 1:N_REP) {
  sum <- sum + analyze_r08(state=state, human=F)
}
print(paste('[8]', sum / N_REP))
