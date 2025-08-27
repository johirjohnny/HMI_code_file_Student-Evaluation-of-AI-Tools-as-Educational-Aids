# CronbachAlphaEthics_Subscales.R
library(readxl)
library(psych)

# ---- 1) Excel einlesen
# Falls direkt unter den Spaltennamen noch eine Fragetext-Zeile steht, setze skip=1 (oder 2) und probier erneut.
df <- read_excel("C:\\Users\\User\\OneDrive\\Desktop\\HMI20_08_22_Survey Results\\data_test489968_2025-08-22_11-32.xlsx", #, skip = 1
)

# ---- 2) Helfer: robust nach numeric parsen (ohne Zusatzpakete)
coerce_num <- function(v) {
  v <- as.character(v)
  v <- trimws(v)            # Leerzeichen weg
  v[v == ""] <- NA          # leere Strings -> NA
  v <- gsub(",", ".", v)    # Komma -> Punkt
  suppressWarnings(as.numeric(v))  # Text -> NA
}

make_numeric_block <- function(df, cols, min_non_na_per_row = 1) {
  X <- df[, cols, drop = FALSE]
  X[] <- lapply(X, coerce_num)
  # Zeilen, die nur NA enthalten (z. B. Fragetext-Zeilen), entfernen
  X[rowSums(!is.na(X)) >= min_non_na_per_row, , drop = FALSE]
}

# ---- 3) Subskalen definieren
cheating_cols <- c("EP06_01","EP06_02")   # Cheating / Dishonesty
moral_cols    <- c("EP06_03","EP06_04")   # Moralische Akzeptanz (reverse)
fairness_cols <- c("EP06_05","EP06_06")   # Fairness / Ungleichheit

cheating_items <- make_numeric_block(df, cheating_cols, min_non_na_per_row = 1)
moral_items    <- make_numeric_block(df, moral_cols,    min_non_na_per_row = 1)
fairness_items <- make_numeric_block(df, fairness_cols, min_non_na_per_row = 1)

# ---- 4) Kurze Checks
cat("\nNA pro Item (Cheating):\n"); print(colSums(is.na(cheating_items)))
cat("\nNA pro Item (Moral):\n");    print(colSums(is.na(moral_items)))
cat("\nNA pro Item (Fairness):\n"); print(colSums(is.na(fairness_items)))

# ---- 5) Alpha je Subskala (check.keys spiegelt negativ gepolte Items automatisch)
cat("\n--- Subskala Cheating/Dishonesty ---\n")
print(psych::alpha(cheating_items, check.keys = TRUE))

cat("\n--- Subskala Moralische Akzeptanz ---\n")
print(psych::alpha(moral_items,    check.keys = TRUE))   # EP06_03/EP06_04 werden bei Bedarf gespiegelt

cat("\n--- Subskala Fairness/Ungleichheit ---\n")
print(psych::alpha(fairness_items, check.keys = TRUE))
