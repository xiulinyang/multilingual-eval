library(tidyverse)
library(ggh4x)

metric_order <- c("bpb", "cpb","mrr", "ppl", "token-nll", "sent-nll")


lang_map <- c(
  "FR" = "French (Latin)", "EN" = "English (Latin)", "DE" = "German (Latin)",
  "RU" = "Russian (Cyrillic)", "FI" = "Finnish (Latin)", "PL" = "Polish (Latin)",
  "ZH" = "Chinese (CJK)", "AR" = "Arabic (Arabic)", "TR" = "Turkish (Latin)",
  "KO" = "Korean (Hangul)"
)

lang_order <- c(
  "Polish (Latin)",  "Arabic (Arabic)","Chinese (CJK)",  "Turkish (Latin)", "Russian (Cyrillic)","Finnish (Latin)",
  "English (Latin)",   "German (Latin)","French (Latin)", "Korean (Hangul)"
)

# script_linetypes <- c(
#   "English (Latin)"    = "solid",
#   "French (Latin)"     = "solid",
#   "German (Latin)"     = "twodash",
#   "Finnish (Latin)"    = "dotdash",
#   "Polish (Latin)"     = "solid",
#   "Turkish (Latin)"    = "longdash",
#   "Russian (Cyrillic)" = "solid",
#   "Chinese (CJK)"      = "solid",
#   "Korean (Hangul)"    = "dotted",
#   "Arabic (Arabic)"    = "dashed"
# )
# 
script_linetypes <- c(
  "English (Latin)"    = "solid",
  "French (Latin)"     = "solid",
  "German (Latin)"     = "solid",
  "Finnish (Latin)"    = "solid",
  "Polish (Latin)"     = "solid",
  "Turkish (Latin)"    = "solid",
  "Russian (Cyrillic)" = "solid",
  "Chinese (CJK)"      = "solid",
  "Korean (Hangul)"    = "solid",
  "Arabic (Arabic)"    = "solid"
)

# lang_colors <- c(
#   "English (Latin)"    = "#ffca3a",
#   "French (Latin)"     = "#6a4c93",
#   "German (Latin)"     = "#DEEDFF",
#   "Finnish (Latin)"    = "#DEEDFF",
#   "Polish (Latin)"     = "#1982c4",
#   "Turkish (Latin)"    = "#DEEDFF",
#   "Russian (Cyrillic)" = "#E31A1C",
#   "Chinese (CJK)"      = "#33A02C",
#   "Korean (Hangul)"    = "#DEEDFF",
#   "Arabic (Arabic)"    = "#DEEDFF"
# )


lang_colors <- c(
  "English (Latin)"    = "#FDBF6F",
  "French (Latin)"     = "#6a4c93",
  "German (Latin)"     = "#ffca3a",
  "Finnish (Latin)"    = "#FB9A99",
  "Polish (Latin)"     = "#1982c4",
  "Turkish (Latin)"    = "#B2DF8A",
  "Russian (Cyrillic)" = "#E31A1C",
  "Chinese (CJK)"      = "#33A02C",
  "Korean (Hangul)"    = "#CAB2D6",
  "Arabic (Arabic)"    = "#A6CEE3"
)

df <- read_csv(
  "/Users/xiulinyang/Desktop/TODO/multilingual-eval/summary_parallel10.csv",
  show_col_types = FALSE
) %>%
  mutate(
    across(c(lang, tokenization, eval_data, metric_type), as.character),
    vocab_size   = as.integer(vocab_size),
    eval_data    = recode(eval_data, !!!lang_map),
    eval_data    = factor(eval_data, levels = lang_order),
    tokenization = factor(tokenization),
    metric_type = factor(metric_type, levels = metric_order)
  )

df_plot <- df %>%
  filter(tokenization == "bpe")

x_breaks <- sort(unique(df_plot$vocab_size))

metric_labels <- c(
  "bpb"       = "BPB (↓)",
  "cpb"       = "BPC (↓)",
  "ppl"       = "PPL (↓)",
  "sent-nll"  = "Sentence NLL (↓)",
  "token-nll" = "Token NLL (↓)",
  "mrr"       = "MRR (↑)"
)

p <- ggplot(
  df_plot,
  aes(
    x        = vocab_size,
    y        = mean_value,
    color    = eval_data,
    linetype = eval_data,
    group    = eval_data
  )
) +
  geom_line(linewidth = 0.75, alpha = 0.9) +
  geom_point(size = 0.8, alpha = 0.9) +
  
  facet_wrap(
    ~ metric_type,
    nrow     = 1,
    scales   = "free_y",
    labeller = labeller(metric_type = metric_labels)
  ) +
  
  scale_x_continuous(
    trans  = "log2",
    breaks = x_breaks,
    labels = scales::label_number(scale = 1e-3, suffix = "k")
  ) +
  
  scale_y_continuous(
    breaks = scales::pretty_breaks(n = 4),
    expand = expansion(mult = c(0.05, 0.08))
  ) +
  
  # scale_color_brewer(
  #   palette = "Paired",
  #   breaks  = lang_order,
  #   name    = NULL,
  #   drop    = FALSE
  # )  +
  
  scale_color_manual(
    values = lang_colors,
    breaks = lang_order,
    name   = NULL,
    drop   = FALSE
  )+
  
  scale_linetype_manual(
    values = script_linetypes,
    breaks = lang_order,
    name   = NULL
  ) +
  
  theme_bw(base_size = 11) +
  theme(
    strip.background   = element_rect(fill = "grey92", color = NA),
    strip.text         = element_text(face = "bold", size = 11),
    axis.title         = element_text(size = 13),
    axis.text.x        = element_text(angle = 45, hjust = 1, size = 10),
    axis.text.y        = element_text(size = 12),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank(),
    panel.grid.major.y = element_line(color = "grey88", linewidth = 0.4),
    legend.position    = "bottom",
    legend.key.width   = unit(1.8, "cm"),
    legend.key.height  = unit(0.45, "cm"),
    legend.text        = element_text(size = 13),
    legend.margin      = margin(t = -4),
    legend.spacing.x   = unit(0.3, "cm"),
    panel.spacing      = unit(0.6, "cm"),
    plot.margin        = margin(4, 6, 4, 4)
  ) +
  
  guides(
    color    = guide_legend(ncol = 5, override.aes = list(linewidth = 1.2)),
    linetype = guide_legend(ncol = 5)
  ) +
  
  labs(
    x = "Vocabulary Size",
    y = "Metric Value"
  )

p