#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def main(args):
    df = pd.read_csv(args.ocr_estimate, sep=args.sep)
    metrics = ["lev", "wer", "cer"]
    # sort for nicer lines
    df = df.sort_values("parliament_year")

    estates = df["estate"].unique()
    colors = plt.cm.tab10(range(len(estates)))
    estate_colors = dict(zip(estates, colors))
    years = df["parliament_year"].drop_duplicates().to_list()
    year_pos = {y: i for i, y in enumerate(years)}
    fig, axes = plt.subplots(
        nrows=len(metrics),
        ncols=1,
        figsize=(11, 4*len(metrics)),
        sharex=True)

    for ax, var in zip(axes, metrics):
        for estate in estates:
            subset = df[df["estate"] == estate]

            x = subset["parliament_year"].map(year_pos).to_numpy(dtype=float)
            xj = x + np.random.uniform(-args.jitter, args.jitter, size=len(x))

            ax.scatter(
                xj,
                subset[var].to_numpy(),
                color=estate_colors[estate],
                alpha=0.6,
                s=25,
                label=estate
            )

        # --- average line per estate ---
        avg_df = (
            df.groupby(["parliament_year", "estate"])[var]
            .mean()
            .reset_index()
        )

        for estate in estates:
            subset = avg_df[avg_df["estate"] == estate]
            ax.plot(
                subset["parliament_year"],
                subset[var],
                color=estate_colors[estate],
                linewidth=2
            )

        ax.set_ylabel(var)
        ax.grid(True, alpha=0.3)

    # shared x-axis
    axes[-1].set_xlabel("Year")

    # single legend (avoid duplicates)
    handles, labels = axes[0].get_legend_handles_labels()
    axes[-1].set_xticks(range(len(years)))
    axes[-1].set_xticklabels(years, rotation=90, ha="center")
    fig.legend(
        handles[:len(estates)],
        labels[:len(estates)],
        title="Estate",
        loc="upper right"
    )

    fig.suptitle("Yearly values with jittered observations and estate averages", y=1.02)
    fig.tight_layout()
    plt.savefig(f"{args.output_dir}/ocr-qe-plot.png")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ocr-estimate", default="quality/estimates/ocr-estimate.tsv")
    parser.add_argument("--sep",default="\t")
    parser.add_argument("-o", "--output-dir", default="quality/estimates")
    parser.add_argument("--jitter", default=0.12, type=float)
    main(parser.parse_args())
