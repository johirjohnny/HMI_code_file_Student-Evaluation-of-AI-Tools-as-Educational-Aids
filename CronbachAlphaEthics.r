library(readxl)
library(psych)

# 1) Excel einlesen
#   Falls in der ersten Datenzeile Fragetexte stehen: setze skip=1 (oder 2) und probier es:
df <- read_excel("C:\\Users\\User\\OneDrive\\Desktop\\HMI20_08_22_Survey Results\\data_test489968_2025-08-22_11-32.xlsx", skip = 0)

# 2) Item-Spalten definieren
cols <- c("EP06_01","EP06_02","EP06_03","EP06_04","EP06_05","EP06_06")
ethic_items <- df[, cols]

# 3) Robust nach numeric parsen (ohne zusätzliche Pakete)
coerce_num <- function(v) {
  v <- as.character(v)
  v <- trimws(v)                 # Leerzeichen weg
  v[v == ""] <- NA               # leere Strings -> NA
  v <- gsub(",", ".", v)         # Komma -> Punkt
  suppressWarnings(as.numeric(v))# als Zahl parsen (Text -> NA)
}
ethic_items[] <- lapply(ethic_items, coerce_num)

# 4) Zeilen mit (fast) nur NAs raus (z.B. Fragetext-Zeilen aus Export)
ethic_items <- ethic_items[rowSums(!is.na(ethic_items)) >= 2, , drop = FALSE]

# 5) Kurze Checks
print(sapply(ethic_items, is.numeric))   # alle TRUE?
print(colSums(is.na(ethic_items)))       # NAs pro Item

# 6) Cronbach’s Alpha (spiegelt negative Items automatisch)
a <- psych::alpha(ethic_items, check.keys = TRUE)

# 7) Kernwerte
cat("\nRaw alpha:", a$total$raw_alpha,
    "\nStd alpha:", a$total$std.alpha,
    "\nAvg inter-item r:", a$total$average_r, "\n")

# 8) Item-Diagnostik
print(a$item.stats[, c("mean","sd","r.drop")])
print(a$alpha.drop)  # alpha if item deleted
