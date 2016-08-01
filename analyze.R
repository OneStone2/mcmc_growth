pkgs <- c('doMC', 'Cubist', 'caret')
lapply(pkgs, require, character.only = T)
registerDoMC(core = 7)

analyze_r05 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    } else {
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

    sum_mse = 0
    mdl <- c()
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]
      
      mdl[[i]] <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl[[i]], newdata = X2)) ^ 2)/length(Y2))
      sum_mse <- sum_mse + mse
    }
    cat(paste(sum_mse/10, '\n', sep=''))
    return(mdl)
}

analyze_r06 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    } else {
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

    sum_mse = 0
    mdl <- c()
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]
      
      mdl[[i]] <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl[[i]], newdata = X2)) ^ 2)/length(Y2))
      sum_mse <- sum_mse + mse
    }
    cat(paste(sum_mse/10, '\n', sep=''))
    return(mdl)
}

analyze_r07 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    } else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    x['human_p'] <- x['human_p'] + x['human_f']
    x['human_f'] <- pmin(1, x['human_f'])
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

    sum_mse = 0
    mdl <- c()
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]
      
      mdl[[i]] <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl[[i]], newdata = X2)) ^ 2)/length(Y2))
      sum_mse <- sum_mse + mse
    }
    cat(paste(sum_mse/10, '\n', sep=''))
    return(mdl)
}

analyze_r08 <- function(state, human) {
    if (human) {
        x <- read.csv(paste("data/", state, "_2a.csv", sep=''), as.is=T)
    } else {
        x <- read.csv(paste("data/", state, "_2b.csv", sep=''), as.is=T)
    }
    r1 <- x[["carb"]]
    r2 <- x[["py"]]
    r3 <- x[["human_p"]]
    r4 <- x[["human_n"]]
    r5 <- x[["human_f"]]
    x <- x[-c(nrow(x)),]
    r1 <- r1[-c(1)]
    r2 <- r2[-c(1)]
    r3 <- r3[-c(1)]
    r4 <- r4[-c(1)]
    r5 <- r5[-c(1)]
    x["post_py"] <- r2
    x["growth"] <- (x["carb"]-r1)/(x["py"]-x["post_py"])
    x["human_p"] <- r3
    x["human_n"] <- r4
    x["human_f"] <- r5
    x <- x[x[,"py"] %/% 10000 == x[,"post_py"] %/% 10000,]
    x <- x[, names(x) %in% grep("(growth)|(py)|(post_py)|(lat)|(lon)|(carb)|(iv[0123456789.]+)|(human_[npf])", colnames(x), value=T)]
    row.names(x) <- 1:nrow(x)

    X <- x[, !names(x) %in% c("growth","py","post_py")]
    Y <- x[,names(x) %in% "growth"]

    groups <- split(1:nrow(x), sample(1:10, nrow(x), replace=T))

    sum_mse = 0
    mdl <- c()
    for (i in 1:10) {
      rows <- groups[[i]]
      X1 <- X[-rows, ]
      X2 <- X[rows, ]
      Y1 <- Y[-rows]
      Y2 <- Y[rows]
      
      mdl[[i]] <- cubist(x = X1, y = Y1, commitees = 1, control = cubistControl(unbiased = TRUE, rules = 999, label = "growth"))
      mse <- sqrt(sum((Y2 -predict(mdl[[i]], newdata = X2)) ^ 2)/length(Y2))
      sum_mse <- sum_mse + mse
    }
    cat(paste(sum_mse/10, '\n', sep=''))
    return(mdl)
}

state <- 'PA'
#Change state to whatever you want
mdl5 <- analyze_r05(state=state, human=T)
mdl6 <- analyze_r06(state=state, human=T)
mdl7 <- analyze_r07(state=state, human=T)
mdl8 <- analyze_r08(state=state, human=T)
#The following lines are for test purposes only
#forest <- varImp(mdl8[[1]])
#forest <- data.frame(forest[order(rownames(forest)),])
#for (i in 2:10) {
#  new_df <- varImp(mdl8[[i]])
#  new_df <- data.frame(new_df[order(rownames(new_df)),])
#  forest[i] <- new_df
#}
#write.csv(forest, file=paste(state, '_cubist.csv', sep=''))
#varImp(mdl8[[2]])
