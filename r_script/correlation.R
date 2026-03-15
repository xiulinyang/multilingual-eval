library(tidyverse)
library(patchwork)
library(RColorBrewer)

metric_order <- c("bpb", "cpb","mrr", "ppl", "token-nll", "sent-nll")

df <- read_csv(
  "/Users/xiulinyang/Desktop/TODO/multilingual-eval/summary_parallels.csv",
  show_col_types = FALSE
) %>%
  mutate(
    vocab_size = as.integer(vocab_size),
    metric_type = factor(metric_type, levels = metric_order)
  )

ctc <- read_tsv(
  "/Users/xiulinyang/Desktop/TODO/multilingual-tokenization/ctc/ctc_florestest.tsv",
  show_col_types = FALSE
) %>%
  rename(
    lang = LANG,
    ctc_score = CTC,
    vocab_size = VOCABSIZE,
    tokenization = TOKALG
  ) %>%
  mutate(vocab_size = as.integer(vocab_size))

lang_order <- c(
  "French", "Polish", "German", "Chinese", "Finnish",
  "Russian", "English", "Arabic", "Turkish", "Korean"
)

lang_map <- c(
  "FR" = "French", "EN" = "English", "DE" = "German", "RU" = "Russian",
  "FI" = "Finnish", "PL" = "Polish", "ZH" = "Chinese",
  "AR" = "Arabic", "TR" = "Turkish", "KO" = "Korean"
)

lang_colors <- setNames(
  brewer.pal(10, "Paired"),
  lang_order
)

df_plot <- df %>%
  filter(tokenization == "bpe") %>%
  group_by(eval_data, metric_type) %>%
  summarise(
    mean_metric = mean(mean_value, na.rm = TRUE),
    .groups = "drop"
  )

lang_cpb <- tribble(
  ~lang, ~value,
  "PL", 139483,
  "EN", 131966,
  "RU", 142096,
  "FR", 157638,
  "TR", 135761,
  "AR", 116307,
  "ZH", 43248,
  "FI", 140128,
  "KO", 65965,
  "DE", 153809
)

lang_bpb <- tribble(
  ~lang, ~value,
  "PL", 148251,
  "EN", 132096,
  "RU", 260342,
  "FR", 163927,
  "TR", 147896,
  "AR", 211263,
  "ZH", 120803,
  "FI", 145817,
  "KO", 157799,
  "DE", 156358
)

cpb_merge <- df_plot %>%
  filter(metric_type == "cpb") %>%
  rename(lang = eval_data) %>%
  left_join(lang_cpb, by = "lang") %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "BPC"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = value / 1000,
    y = mean_metric
  )

bpb_merge <- df_plot %>%
  filter(metric_type == "bpb") %>%
  rename(lang = eval_data) %>%
  left_join(lang_bpb, by = "lang") %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "BPB"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = value / 1000,
    y = mean_metric
  )

ppl_merge <- df %>%
  filter(metric_type == "ppl", tokenization == "bpe") %>%
  left_join(ctc, by = c("lang", "tokenization", "vocab_size")) %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "PPL"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = ctc_score / 1000,
    y = log10(mean_value)
  )

token_nll_merge <- df %>%
  filter(metric_type == "token-nll", tokenization == "bpe") %>%
  left_join(ctc, by = c("lang", "tokenization", "vocab_size")) %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "Token NLL"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = ctc_score / 1000,
    y = mean_value
  )

mrr_merge <- df %>%
  filter(metric_type == "mrr", tokenization == "bpe") %>%
  left_join(ctc, by = c("lang", "tokenization", "vocab_size")) %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "MRR"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = ctc_score / 1000,
    y = mean_value
  )

sent_nll_merge <- df %>%
  filter(metric_type == "sent-nll", tokenization == "bpe") %>%
  left_join(ctc, by = c("lang", "tokenization", "vocab_size")) %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "Sentence NLL"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = ctc_score / 1000,
    y = mean_value
  )

sent_nll_bpc <- df_plot %>%
  filter(metric_type == "sent-nll") %>%
  rename(lang = eval_data) %>%
  left_join(lang_cpb, by = "lang") %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "Sentence NLL"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = value / 1000,
    y = mean_metric
  )

sent_nll_bpb <- df_plot %>%
  filter(metric_type == "sent-nll") %>%
  rename(lang = eval_data) %>%
  left_join(lang_bpb, by = "lang") %>%
  mutate(
    lang_name = unname(lang_map[lang]),
    lang_name = factor(lang_name, levels = lang_order),
    title = "Sentence NLL"
  ) %>%
  transmute(
    lang,
    lang_name,
    title,
    x = value / 1000,
    y = mean_metric
  )

make_plot <- function(data, xlab, ylab) {
  test <- cor.test(data$x, data$y, method = "spearman")
  
  label_text <- paste0(
    "rho = ", round(unname(test$estimate), 2),
    "\n",
    "p = ", format.pval(test$p.value, digits = 2, eps = 0.001)
  )
  
  ggplot(data, aes(x = x, y = y)) +
    geom_point(aes(color = lang_name), size = 1.3) +
    geom_smooth(
      aes(group = 1),
      method = "lm",
      se = TRUE,
      linewidth = 0.7,
      color = "black"
    ) +
    annotate(
      "text",
      x = Inf,
      y = Inf,
      label = label_text,
      hjust = 1.05,
      vjust = 1.3,
      size = 3.0,
      fontface = "bold"
    ) +
    facet_wrap(~ title, nrow = 1) +
    scale_color_manual(
      values = lang_colors,
      breaks = lang_order,
      drop = FALSE
    ) +
    guides(
      color = guide_legend(
        nrow = 3,
        byrow = TRUE,
        override.aes = list(size = 3)
      )
    ) +
    labs(
      x = xlab,
      y = ylab,
      color = "Language"
    ) +
    theme_bw(base_size = 12) +
    theme(
      strip.background = element_rect(fill = "#E8E8E8", color = NA),
      strip.text = element_text(face = "bold", size = 12),
      axis.title = element_text(size = 10),
      axis.text = element_text(size = 9),
      legend.position = "bottom",
      legend.direction = "horizontal",
      legend.spacing.x = unit(0.15, "cm"),
      panel.spacing = unit(0.5, "lines")
    )
}

p1 <- make_plot(cpb_merge, "Character count (k)", "Mean Metric Value")
p2 <- make_plot(bpb_merge, "Byte count (k)", NULL)
p3 <- make_plot(ppl_merge, "CTC (k)", NULL)
p4 <- make_plot(token_nll_merge, "CTC (k)", NULL)
p5 <- make_plot(mrr_merge, "CTC (k)", NULL)
p6 <- make_plot(sent_nll_merge, "CTC (k)", NULL)
p7 <- make_plot(sent_nll_bpc, "Character Count (k)", NULL)
p8 <- make_plot(sent_nll_bpb, "Byte Count (k)", NULL)

design <- "
ABCDE
FGHLL
"

final_plot <- wrap_plots(
  A = p1, B = p2, C = p3, D = p4, E = p5,
  F = p6, G = p7, H = p8,
  L = guide_area(),
  design = design,
  guides = "collect"
) &
  theme(
    strip.background = element_rect(fill = "#E8E8E8", color = NA),
    strip.text = element_text(face = "bold", size = 12),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 12),
    legend.position = "bottom",
    legend.title.position = "top",
    legend.text = element_text(size = 13),
    legend.title = element_text(size = 15, face = "bold"),
    legend.key.size = unit(0.5, "cm"),
    legend.spacing.x = unit(0.15, "cm"),
    panel.spacing = unit(0.5, "lines")
  )

final_plot