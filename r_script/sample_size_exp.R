library(tidyverse)
library(ggh4x)

metric_order <- c("bpb", "cpb", "mrr", "ppl", "token-nll", "sent-nll")
metric_labels <- c(
  "bpb"       = "BPB",
  "cpb"       = "BPC",
  "ppl"       = "PPL",
  "sent-nll"  = "Sentence NLL",
  "token-nll" = "Token NLL",
  "mrr"       = "MRR"
)
lang_colors <- c(
  "EN"         = "#ffca3a",
  "DE(lowest)" = "#CFEDD5",
  "DE1"        = "#40AA5F",
  "DE2"        = "#178840",
  "DE(highest)"= "#006027"
)

sample_sizes <- c(1, 10, 100, 500, 1997)
base_path <- "/Users/xiulinyang/Desktop/TODO/multilingual-eval/sample_size/"

df_all <- map_dfr(sample_sizes, function(ss) {
  read_csv(paste0(base_path, "paraphrase_results_", ss, ".csv"),
           show_col_types = FALSE) %>%
    mutate(sample_size = ss)
})


df_summary <- df_all %>%
  mutate(across(c(lang, tokenization, eval_data, metric_type), as.character)) %>%
  group_by(lang, tokenization, vocab_size, eval_data, metric_type, sample_size) %>%
  summarise(
    sd         = sd(mean_value, na.rm = TRUE),
    n          = n(),
    mean_value = mean(mean_value, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    se   = sd / sqrt(n),
    ci95 = qt(0.975, df = n - 1) * se,
    metric_type = factor(metric_type, levels = metric_order),
    sample_size = factor(sample_size, levels = sample_sizes,
                         labels = paste0("n=", sample_sizes))
  )

df_plot <- df_summary %>%
  filter(tokenization == "bpe") %>%
  filter(eval_data %in% c("de", "DE_highest", "DE_lowest", "de-p", "en")) %>%
  mutate(
    eval_data = recode(eval_data,
                       "de" = "DE1", "en" = "EN", "de-p" = "DE2",
                       "DE_highest" = "DE(highest)", "DE_lowest" = "DE(lowest)"
    ),
    eval_data = factor(eval_data,
                       levels = c("EN", "DE1", "DE2", "DE(highest)", "DE(lowest)"))
  )

x_breaks <- sort(unique(df_plot$vocab_size))

p <- ggplot(
  df_plot,
  aes(x = vocab_size, y = mean_value, color = eval_data, group = eval_data)
) +
  geom_line(linewidth = 0.75, alpha = 0.9) +
  geom_point(size = 1.8, alpha = 0.9) +
  geom_errorbar(
    aes(ymin = mean_value - ci95, ymax = mean_value + ci95),
    width = 0, linewidth = 0.5, alpha = 0.6
  ) +
  facet_grid2(
    sample_size ~ metric_type,          # 行=sample_size，列=metric
    scales = "free_y",
    independent='y',
    labeller = labeller(metric_type = metric_labels)
  ) +
  scale_x_continuous(
    breaks = x_breaks,
    labels = scales::label_number(scale = 1e-3, suffix = "k")
  ) +
  scale_color_manual(values = lang_colors, name = NULL) +
  theme_bw(base_size = 11) +
  theme(
    strip.background = element_rect(fill = "grey92", color = NA),
    strip.text = element_text(face = "bold", size = 10),
    axis.title = element_text(size = 11),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 8),
    axis.text.y = element_text(size = 8),
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.y = element_line(color = "grey88", linewidth = 0.4),
    legend.position = "bottom",
    legend.text = element_text(size = 11),
    panel.spacing = unit(0.4, "cm"),
    plot.margin = margin(4, 6, 4, 4)
  ) +
  guides(
    color = guide_legend(nrow = 1, override.aes = list(linewidth = 1.2, size = 2.2))
  ) +
  labs(x = "Vocabulary Size", y = "Metric Value")


ggsave("sample_size_grid.pdf", p, width = 18, height = 14)
p